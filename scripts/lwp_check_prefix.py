#!/usr/bin/env python3
"""CI check `lwp-prefix`: every user-facing entrypoint starts with `lwp`.

Checks (stdlib only):
  - Every `skills/<name>/SKILL.md` directory name under `plugins/**` starts
    with `lwp-`, and its front-matter `name:` field matches the directory.
  - Every `command`, `bin/`, or `scripts/` script a user or plugin manifest
    can invoke directly -- `plugins/*/*/bin/*.py` and `scripts/*.py` -- starts
    with `lwp`, except this script's own module (checked by name) and
    non-entrypoint helpers explicitly allow-listed below.
  - Both plugin manifests' `"name"` field is exactly `lwp`.

Exits 0 and prints "lwp-prefix check passed" on success; otherwise prints
every failure found (not just the first) and exits 1.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Files under scripts/ and plugins/*/*/bin/ that are not themselves a
# user-facing entrypoint (helpers, __init__, dunder files) and so are
# exempt from the `lwp` prefix.
_NON_ENTRYPOINT_EXEMPT = {"__init__.py"}

# The pre-recast Codex package. plan.md keeps it working until D2 replaces
# it (`plugins/codex/lwp`, `scripts/lwp_validate_codex_plugin.py`, the
# marketplace repointed), so these two names cannot satisfy the rule yet.
# D0's job is "the R1 check exists"; D2/D4 is where it applies to the real
# plugins.
LEGACY_PACKAGE_RELPATH = ("plugins", "LEAPWare-Pulse")
_LEGACY_EXEMPT_SCRIPTS = {"validate_pulse_plugin.py"}
_LEGACY_EXEMPT_MARKETPLACE_IDS = {"LEAPWare-Pulse"}


def legacy_exemption_active() -> bool:
    """True while the pre-recast package is still in the tree.

    Self-retiring on purpose: the exemption is keyed to the legacy
    directory's existence, not to a date or a flag someone has to remember
    to remove. The moment D2 deletes plugins/LEAPWare-Pulse/, both
    exemptions vanish and the check enforces the rule in full. See
    tests/test_lwp_check_prefix.py::test_legacy_exemption_is_keyed_to_the_legacy_package.

    Resolved against REPO_ROOT at call time, never bound at import: the
    tests swap REPO_ROOT to a fixture tree, and an import-time constant
    would keep pointing at this repo and silently exempt fixtures too.
    """
    return REPO_ROOT.joinpath(*LEGACY_PACKAGE_RELPATH).is_dir()


def _rel(path: Path) -> str:
    """Repo-relative POSIX path, never absolute.

    Failure output is captured verbatim into proof records
    (proof/LWP-D*.json, `commands[].tail`); an absolute path there would
    plant a drive-letter or /home/<user> path in a committed file and trip
    LWP-R3's own env-leak check.
    """
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.name


def _check_skills(errors: list[str]) -> None:
    for skill_md in sorted(REPO_ROOT.glob("plugins/*/*/skills/*/SKILL.md")):
        dir_name = skill_md.parent.name
        if not dir_name.startswith("lwp-"):
            errors.append(f"skill directory does not start with 'lwp-': {_rel(skill_md.parent)}")
            continue
        text = skill_md.read_text(encoding="utf-8")
        m = re.search(r"^name:\s*(\S+)\s*$", text, re.MULTILINE)
        if not m or m.group(1) != dir_name:
            errors.append(
                f"{_rel(skill_md)}: front-matter 'name:' does not match directory name '{dir_name}'"
            )


def _check_scripts(errors: list[str]) -> None:
    for py in sorted(REPO_ROOT.glob("scripts/*.py")):
        if py.name in _NON_ENTRYPOINT_EXEMPT:
            continue
        if py.name in _LEGACY_EXEMPT_SCRIPTS and legacy_exemption_active():
            continue
        if not py.name.startswith("lwp"):
            errors.append(f"scripts/ entrypoint does not start with 'lwp': {_rel(py)}")

    for py in sorted(REPO_ROOT.glob("plugins/*/*/bin/*.py")):
        if py.name in _NON_ENTRYPOINT_EXEMPT:
            continue
        if not py.name.startswith("lwp"):
            errors.append(f"plugin bin/ entrypoint does not start with 'lwp': {_rel(py)}")


def _check_manifests(errors: list[str]) -> None:
    for manifest_path in sorted(REPO_ROOT.glob("plugins/*/*/.claude-plugin/plugin.json")) + sorted(
        REPO_ROOT.glob("plugins/*/*/.codex-plugin/plugin.json")
    ):
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON in {_rel(manifest_path)}: {exc}")
            continue
        if data.get("name") != "lwp":
            errors.append(f"{_rel(manifest_path)}: plugin id is '{data.get('name')}', want 'lwp'")

    for marketplace_path in (
        REPO_ROOT / ".claude-plugin" / "marketplace.json",
        REPO_ROOT / ".agents" / "plugins" / "marketplace.json",
    ):
        if not marketplace_path.is_file():
            # Not every marketplace file exists at every phase (e.g. the
            # Claude marketplace lands in D4); a missing file is not itself
            # a prefix violation, so skip rather than fail the whole check.
            continue
        try:
            data = json.loads(marketplace_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON in {_rel(marketplace_path)}: {exc}")
            continue
        for entry in data.get("plugins", []):
            if not isinstance(entry, dict):
                continue
            if entry.get("name") in _LEGACY_EXEMPT_MARKETPLACE_IDS and legacy_exemption_active():
                continue
            if entry.get("name") != "lwp":
                errors.append(
                    f"{_rel(marketplace_path)}: plugin entry id is '{entry.get('name')}', want 'lwp'"
                )


def check() -> list[str]:
    errors: list[str] = []
    _check_skills(errors)
    _check_scripts(errors)
    _check_manifests(errors)
    return errors


def main() -> int:
    errors = check()
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    if legacy_exemption_active():
        print(
            "lwp-prefix check passed "
            "(pre-recast exemption ACTIVE: plugins/LEAPWare-Pulse/ still in "
            "the tree; it retires itself when D2 removes that directory)"
        )
    else:
        print("lwp-prefix check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
