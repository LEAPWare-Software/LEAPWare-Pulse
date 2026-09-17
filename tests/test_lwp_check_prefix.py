"""Tests for scripts/lwp_check_prefix.py (LWP-R1).

Uses a throwaway fixture tree in tmp_path so this never depends on this
repo's own pre-recast layout (`plugins/LEAPWare-Pulse/`), which does not
yet satisfy the lwp- prefix rule -- that is expected until D2/D4 (see
plan.md) and is proven separately by running the script against the real
repo (recorded in the dispatch report, not asserted here).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import lwp_check_prefix as check_mod  # noqa: E402


def _write_valid_tree(root: Path) -> None:
    skill_dir = root / "plugins" / "claude" / "lwp" / "skills" / "lwp-status"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: lwp-status\ndescription: status\n---\nbody\n", encoding="utf-8"
    )

    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "scripts" / "lwp_something.py").write_text("# entrypoint\n", encoding="utf-8")

    bin_dir = root / "plugins" / "claude" / "lwp" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    (bin_dir / "lwp_hook.py").write_text("# entrypoint\n", encoding="utf-8")

    manifest_dir = root / "plugins" / "claude" / "lwp" / ".claude-plugin"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    (manifest_dir / "plugin.json").write_text(json.dumps({"name": "lwp"}), encoding="utf-8")

    codex_manifest_dir = root / "plugins" / "codex" / "lwp" / ".codex-plugin"
    codex_manifest_dir.mkdir(parents=True, exist_ok=True)
    (codex_manifest_dir / "plugin.json").write_text(json.dumps({"name": "lwp"}), encoding="utf-8")

    claude_plugin_dir = root / ".claude-plugin"
    claude_plugin_dir.mkdir(parents=True, exist_ok=True)
    (claude_plugin_dir / "marketplace.json").write_text(
        json.dumps({"plugins": [{"name": "lwp"}]}), encoding="utf-8"
    )
    agents_dir = root / ".agents" / "plugins"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / "marketplace.json").write_text(
        json.dumps({"plugins": [{"name": "lwp"}]}), encoding="utf-8"
    )


def _run_check(root: Path) -> list[str]:
    original_root = check_mod.REPO_ROOT
    try:
        check_mod.REPO_ROOT = root
        return check_mod.check()
    finally:
        check_mod.REPO_ROOT = original_root


def test_valid_tree_passes(tmp_path):
    _write_valid_tree(tmp_path)
    assert _run_check(tmp_path) == []


def test_break_renamed_skill_dir_and_wrong_manifest_name(tmp_path):
    _write_valid_tree(tmp_path)

    # Break: rename a skill directory to 'pulse-status' (no lwp- prefix).
    old_skill_dir = tmp_path / "plugins" / "claude" / "lwp" / "skills" / "lwp-status"
    new_skill_dir = tmp_path / "plugins" / "claude" / "lwp" / "skills" / "pulse-status"
    old_skill_dir.rename(new_skill_dir)
    (new_skill_dir / "SKILL.md").write_text(
        "---\nname: pulse-status\ndescription: status\n---\nbody\n", encoding="utf-8"
    )

    # Break: set one manifest name to 'LEAPWare-Pulse'.
    manifest_path = tmp_path / "plugins" / "claude" / "lwp" / ".claude-plugin" / "plugin.json"
    manifest_path.write_text(json.dumps({"name": "LEAPWare-Pulse"}), encoding="utf-8")

    errors = _run_check(tmp_path)
    assert any("skill directory does not start with 'lwp-'" in e for e in errors)
    assert any("plugin id is 'LEAPWare-Pulse'" in e for e in errors)


def test_scripts_entrypoint_without_prefix_fails(tmp_path):
    _write_valid_tree(tmp_path)
    (tmp_path / "scripts" / "other_tool.py").write_text("# not lwp-prefixed\n", encoding="utf-8")
    errors = _run_check(tmp_path)
    assert any("scripts/ entrypoint does not start with 'lwp'" in e for e in errors)


def test_missing_marketplace_file_is_skipped_not_a_crash(tmp_path):
    # LWP-D0: .claude-plugin/marketplace.json does not exist until later
    # phases (D4). A missing marketplace file is not itself a violation,
    # and must not raise -- it is skipped.
    _write_valid_tree(tmp_path)
    (tmp_path / ".claude-plugin" / "marketplace.json").unlink()
    assert _run_check(tmp_path) == []


def test_main_prints_pass_message_and_exits_zero(tmp_path, capsys):
    _write_valid_tree(tmp_path)
    original_root = check_mod.REPO_ROOT
    try:
        check_mod.REPO_ROOT = tmp_path
        exit_code = check_mod.main()
    finally:
        check_mod.REPO_ROOT = original_root
    assert exit_code == 0
    assert "lwp-prefix check passed" in capsys.readouterr().out


def _write_legacy_offenders(root: Path) -> None:
    """The two pre-recast names D2 renames: the validator script and the
    Codex marketplace entry id."""
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "scripts" / "validate_pulse_plugin.py").write_text("# legacy\n", encoding="utf-8")
    agents_dir = root / ".agents" / "plugins"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / "marketplace.json").write_text(
        json.dumps({"plugins": [{"name": "LEAPWare-Pulse"}]}), encoding="utf-8"
    )


def test_legacy_exemption_is_keyed_to_the_legacy_package(tmp_path):
    """Both directions, so the exemption cannot outlive the thing it excuses.

    With plugins/LEAPWare-Pulse/ present (pre-D2) the two legacy names are
    excused; the moment that directory is gone (D2 removes it) they are
    failures again. Nothing here is date- or flag-based.
    """
    _write_valid_tree(tmp_path)
    _write_legacy_offenders(tmp_path)

    legacy_dir = tmp_path / "plugins" / "LEAPWare-Pulse"
    legacy_dir.mkdir(parents=True, exist_ok=True)
    assert _run_check(tmp_path) == [], "pre-D2 tree: the two legacy names must be excused"

    import shutil

    shutil.rmtree(legacy_dir)
    errors = _run_check(tmp_path)
    joined = "\n".join(errors)
    assert "validate_pulse_plugin.py" in joined, (
        "post-D2 tree: the legacy validator script must fail the prefix rule again"
    )
    assert "LEAPWare-Pulse" in joined, (
        "post-D2 tree: the legacy marketplace entry id must fail the prefix rule again"
    )


def test_failure_output_carries_no_absolute_path(tmp_path):
    """Failure text lands verbatim in proof records (LWP-R10), which the
    env-leak check (LWP-R3) then scans. An absolute path here would make
    the proof of a clean tree the thing that dirties it."""
    _write_valid_tree(tmp_path)
    (tmp_path / "scripts" / "not_prefixed.py").write_text("# entrypoint\n", encoding="utf-8")
    errors = _run_check(tmp_path)
    assert errors
    joined = "\n".join(errors)
    assert ":\\" not in joined and "/Users/" not in joined and "/home/" not in joined
    assert str(tmp_path) not in joined
