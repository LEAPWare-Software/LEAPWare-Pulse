#!/usr/bin/env python3
"""CI check `lwp-proof`: every proof/*.json record is well-formed.

Owner directive (LWP-R10): Proof of Completion on every deliverable. This
script validates every `proof/*.json` file against one of TWO shapes,
routed by which fields the record itself carries (see proof/README.md,
"routes by filename" there really means "routes by record shape" -- a
gate record and a phase record are told apart by their own fields, not by
a naming convention this script would otherwise have to hard-code):

  - A PHASE record (has a `gate` field: no; has `deliverable`: yes) is
    validated against the shape `proof/schema.json` documents --
    `proof/LWP-D0.json` etc. Structural checks a JSON Schema alone cannot
    express:
      - `checked_by` must differ from `author` (no self-certified proof).
      - every `commands[]` entry's `exit` must equal its `expect_exit`.
      - `sha256` must look like a real sha256 hex digest (64 hex chars).
      - `commit` must look like a real git SHA (7-40 hex chars).

  - A GATE record (has a `gate` field, e.g. `proof/LWP-GPUB-scan.json`) is
    validated against `proof/gate-schema.json` -- a gate is an owner
    action with an entry condition, not a build deliverable, so it has no
    author/checked_by/commands triple. Structural check a JSON Schema
    alone cannot express: no record with any `checks[].result == "fail"`
    may carry `verdict == "publishable"`.

A record matching neither shape (no `gate` and no `deliverable` field) is
reported as not fitting either known proof schema -- not silently skipped.

Two schema files, `schema.json` and `gate-schema.json`, live in `proof/`
alongside the records; both are skipped when scanning for records to
validate.

Usage:
    python scripts/lwp_check_proof.py

Stdlib only. Exits 0 and prints "lwp-proof check passed" (or a skipped
message if proof/ has no records) on success; otherwise prints every
failure found (not just the first) and exits 1.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROOF_DIR = REPO_ROOT / "proof"

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")
GATE_ID_RE = re.compile(r"^G-[A-Z0-9-]+$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

# Values that name nobody. A `checked_by` matching one of these (case- and
# punctuation-insensitive) is treated as "the independent check has not
# happened", not as a valid identity.
_PLACEHOLDER_IDENTITIES = frozenset(
    {
        "pending",
        "todo",
        "tbd",
        "tba",
        "none",
        "n/a",
        "na",
        "unknown",
        "unchecked",
        "xxx",
        "-",
        "?",
        "someone",
        "self",
        "me",
    }
)


# Markers of "the check has not happened yet", matched as SUBSTRINGS. The
# exact-word list above only catches a value that is nothing but the word;
# the independent check walked straight past it with `AWAITING-VERIFIER`,
# and `PLACEHOLDER`, `REDACTED`, `REVIEW-PENDING`, `not-yet-assigned` and
# `TO BE DETERMINED` passed just as easily.
#
# This is a heuristic and it is honest about that: it catches an unfilled
# field, not a dishonest one. Nothing here can tell a real identity from a
# plausible invention -- that guarantee comes from a different identity
# actually running the check, not from this function. Disclosed as such in
# proof/LWP-D0.json's `unproven` list.
_PLACEHOLDER_MARKERS = (
    "pending",
    "await",
    "placeholder",
    "redacted",
    "unassigned",
    "not-yet",
    "not yet",
    "notyet",
    "tbd",
    "tba",
    "todo",
    "fixme",
    "unchecked",
    "unknown",
    "to be determined",
    "to be assigned",
    "xxx",
)


def _is_placeholder(value: str) -> bool:
    """True when `value` reads as an unfilled field rather than an identity."""
    cleaned = value.strip().strip(".!<>[]() ")
    if cleaned.casefold() in _PLACEHOLDER_IDENTITIES:
        return True
    lowered = cleaned.casefold()
    return any(marker in lowered for marker in _PLACEHOLDER_MARKERS)


REQUIRED_TOP = ("deliverable", "author", "checked_by", "commit", "commands", "mutations", "unproven")
REQUIRED_COMMAND = ("argv", "exit", "expect_exit", "tail", "sha256")

REQUIRED_GATE_TOP = ("gate", "item", "date", "verifier", "checks", "verdict")
REQUIRED_GATE_CHECK = ("id", "result", "detail")

# proof/*.json files that are schemas, not records, and so are never
# themselves validated as a record.
_SCHEMA_FILENAMES = {"schema.json", "gate-schema.json"}


def _rel(path: Path) -> Path:
    try:
        return path.relative_to(REPO_ROOT)
    except ValueError:
        # Not under REPO_ROOT (e.g. a test's own tmp_path proof/ directory,
        # or lwp_handoff.py's PROOF_DIR monkeypatched for a test) -- fall
        # back to the path as given rather than raising; this function's
        # job is validating shape, not enforcing where the file lives.
        return path


def _validate_gate_record(path: Path, data: dict) -> list[str]:
    errors: list[str] = []
    rel = _rel(path)

    for field in REQUIRED_GATE_TOP:
        if field not in data:
            errors.append(f"{rel}: missing required field '{field}'")
    if errors:
        return errors

    gate = data["gate"]
    if not isinstance(gate, str) or not GATE_ID_RE.match(gate):
        errors.append(f"{rel}: 'gate' does not look like a gate id (e.g. 'G-PUB'): {gate!r}")
    if not isinstance(data["item"], str) or not data["item"]:
        errors.append(f"{rel}: 'item' must be a non-empty string")
    date = data["date"]
    if not isinstance(date, str) or not DATE_RE.match(date):
        errors.append(f"{rel}: 'date' does not look like an ISO date (YYYY-MM-DD): {date!r}")
    if not isinstance(data["verifier"], str) or not data["verifier"]:
        errors.append(f"{rel}: 'verifier' must be a non-empty string")

    checks = data["checks"]
    any_fail = False
    if not isinstance(checks, list) or not checks:
        errors.append(f"{rel}: 'checks' must be a non-empty list")
    else:
        for i, chk in enumerate(checks):
            prefix = f"{rel}: checks[{i}]"
            if not isinstance(chk, dict):
                errors.append(f"{prefix}: must be an object")
                continue
            for field in REQUIRED_GATE_CHECK:
                if field not in chk:
                    errors.append(f"{prefix}: missing required field '{field}'")
            result = chk.get("result")
            if result not in ("pass", "fail"):
                errors.append(f"{prefix}: 'result' must be 'pass' or 'fail', got {result!r}")
            elif result == "fail":
                any_fail = True
            if not isinstance(chk.get("detail"), str) or not chk.get("detail"):
                errors.append(f"{prefix}: 'detail' must be a non-empty string")

    verdict = data["verdict"]
    if not isinstance(verdict, str) or not verdict:
        errors.append(f"{rel}: 'verdict' must be a non-empty string")
    elif any_fail and verdict == "publishable":
        errors.append(
            f"{rel}: verdict is 'publishable' but at least one checks[].result is 'fail' -- "
            "a gate record with any failing check cannot be publishable"
        )

    return errors


def _validate_phase_record(path: Path, data: dict) -> list[str]:
    errors: list[str] = []
    rel = _rel(path)

    for field in REQUIRED_TOP:
        if field not in data:
            errors.append(f"{rel}: missing required field '{field}'")
    if errors:
        return errors  # further checks assume these fields exist

    if not isinstance(data["deliverable"], str) or not data["deliverable"]:
        errors.append(f"{rel}: 'deliverable' must be a non-empty string")
    if not isinstance(data["author"], str) or not data["author"]:
        errors.append(f"{rel}: 'author' must be a non-empty string")
    if not isinstance(data["checked_by"], str) or not data["checked_by"]:
        errors.append(f"{rel}: 'checked_by' must be a non-empty string")
    elif data["checked_by"].strip().casefold() == str(data.get("author", "")).strip().casefold():
        errors.append(f"{rel}: 'checked_by' equals 'author' -- proof cannot be self-certified")
    elif _is_placeholder(data["checked_by"]):
        # String inequality alone is a cosmetic guard: "PENDING", "TODO" or
        # "" with a trailing space all differ from the author and would pass
        # while naming nobody. A proof record whose independent check has not
        # happened yet is not a proof record.
        errors.append(
            f"{rel}: 'checked_by' is the placeholder {data['checked_by']!r} -- "
            "name the identity that actually ran the check"
        )

    commit = data["commit"]
    if not isinstance(commit, str) or not COMMIT_RE.match(commit):
        errors.append(f"{rel}: 'commit' does not look like a git SHA: {commit!r}")

    commands = data["commands"]
    if not isinstance(commands, list):
        errors.append(f"{rel}: 'commands' must be a list")
    else:
        for i, cmd in enumerate(commands):
            prefix = f"{rel}: commands[{i}]"
            if not isinstance(cmd, dict):
                errors.append(f"{prefix}: must be an object")
                continue
            for field in REQUIRED_COMMAND:
                if field not in cmd:
                    errors.append(f"{prefix}: missing required field '{field}'")
            if not isinstance(cmd.get("argv"), list) or not cmd.get("argv"):
                errors.append(f"{prefix}: 'argv' must be a non-empty list")
            if not isinstance(cmd.get("exit"), int) or not isinstance(cmd.get("expect_exit"), int):
                errors.append(f"{prefix}: 'exit' and 'expect_exit' must be integers")
            elif cmd["exit"] != cmd["expect_exit"]:
                errors.append(
                    f"{prefix}: exit {cmd['exit']} != expect_exit {cmd['expect_exit']} -- "
                    "a proof record cannot record its own failure as proof"
                )
            tail = cmd.get("tail")
            if not isinstance(tail, list) or len(tail) > 10 or not all(isinstance(t, str) for t in tail):
                errors.append(f"{prefix}: 'tail' must be a list of at most 10 strings")
            sha256 = cmd.get("sha256")
            if not isinstance(sha256, str) or not SHA256_RE.match(sha256):
                errors.append(f"{prefix}: 'sha256' does not look like a sha256 hex digest: {sha256!r}")

    if not isinstance(data["mutations"], list) or not all(isinstance(m, str) for m in data["mutations"]):
        errors.append(f"{rel}: 'mutations' must be a list of strings")
    if not isinstance(data["unproven"], list) or not all(isinstance(u, str) for u in data["unproven"]):
        errors.append(f"{rel}: 'unproven' must be a list of strings")

    return errors


def _validate_record(path: Path, data: object) -> list[str]:
    """Route `data` to the gate or phase validator by which fields it
    carries (see module docstring), or report that it matches neither.
    """
    rel = _rel(path)
    if not isinstance(data, dict):
        return [f"{rel}: top-level JSON must be an object"]
    if "gate" in data:
        return _validate_gate_record(path, data)
    if "deliverable" in data:
        return _validate_phase_record(path, data)
    return [
        f"{rel}: record matches neither the phase proof schema (needs 'deliverable') "
        "nor the gate proof schema (needs 'gate') -- proof/schema.json vs. "
        "proof/gate-schema.json, see proof/README.md"
    ]


def validate_all() -> tuple[list[str], int]:
    errors: list[str] = []
    count = 0
    if PROOF_DIR.is_dir():
        for path in sorted(PROOF_DIR.glob("*.json")):
            if path.name in _SCHEMA_FILENAMES:
                continue
            count += 1
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{path.relative_to(REPO_ROOT)}: invalid JSON: {exc}")
                continue
            errors.extend(_validate_record(path, data))
    return errors, count


def main() -> int:
    errors, count = validate_all()
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    if count == 0:
        print("lwp-proof check skipped (no proof/*.json records yet)")
    else:
        print(f"lwp-proof check passed ({count} record(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
