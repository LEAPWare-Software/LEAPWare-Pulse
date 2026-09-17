#!/usr/bin/env python3
"""lwp-trace: enforce LWP-R12 (traceability).

Rule (LWP-R12): every ``LWP-R`` ID heading in
``docs/requirements/requirements.md`` has a row in
``docs/requirements/traceability.md``; no row names an ID absent from
``requirements.md``.

Design point (documented again in ``docs/requirements/traceability.md``):
only D0's requirements have tests today (R2-R6, R8-R12, R39); R7 and
R13-R38 are proven in D1-D5 and their test nodes do not exist yet. So each
traceability row carries a ``status`` column of either ``proven`` or
``planned``:

- ``proven`` rows MUST name at least one test node that actually resolves
  (the file exists, and -- when the node names a specific test function
  with ``path::function`` -- that file contains a ``def function`` line).
- ``planned`` rows name the future test node from ``requirements.md`` and
  are NOT required to resolve; they are the plan, not yet the proof.

The check fails when:

- a row claims ``proven`` but its test node(s) do not resolve;
- a requirement ID from ``requirements.md`` has no row in the matrix;
- a row names an ID that does not exist in ``requirements.md``.

Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^###\s+(LWP-R\d+)\b")
ID_IN_TEXT_RE = re.compile(r"\bLWP-R\d+\b")


def _requirement_ids(requirements_text: str) -> set[str]:
    ids: set[str] = set()
    for line in requirements_text.splitlines():
        match = HEADING_RE.match(line.strip())
        if match:
            ids.add(match.group(1))
    return ids


def _parse_table_rows(traceability_text: str) -> list[dict[str, str]]:
    """Parse the single markdown table in traceability.md into row dicts."""
    lines = traceability_text.splitlines()
    header: list[str] | None = None
    rows: list[dict[str, str]] = []

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if header is None:
            header = [cell.lower() for cell in cells]
            continue
        # Separator row, e.g. |---|---|---|
        if all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))

    return rows


def _extract_id(cell: str) -> str | None:
    match = ID_IN_TEXT_RE.search(cell)
    return match.group(0) if match else None


def _test_nodes(cell: str) -> list[str]:
    cell = cell.replace("`", "")
    parts = re.split(r"[;,]", cell)
    return [p.strip() for p in parts if p.strip()]


def _resolve_node(repo: Path, node: str) -> bool:
    if "::" in node:
        file_part, func_part = node.split("::", 1)
    else:
        file_part, func_part = node, None

    path = repo / file_part
    if not path.is_file():
        return False
    if func_part is None:
        return True
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return False
    pattern = re.compile(r"^\s*def\s+" + re.escape(func_part) + r"\s*\(", re.MULTILINE)
    return bool(pattern.search(content))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Enforce LWP-R12 traceability.")
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to the repository to check (default: current directory).",
    )
    args = parser.parse_args(argv)

    repo = Path(args.repo)
    requirements_path = repo / "docs" / "requirements" / "requirements.md"
    traceability_path = repo / "docs" / "requirements" / "traceability.md"

    if not requirements_path.is_file():
        print(f"lwp-trace: missing {requirements_path}", file=sys.stderr)
        return 1
    if not traceability_path.is_file():
        print(f"lwp-trace: missing {traceability_path}", file=sys.stderr)
        return 1

    requirement_ids = _requirement_ids(requirements_path.read_text(encoding="utf-8"))
    rows = _parse_table_rows(traceability_path.read_text(encoding="utf-8"))

    errors: list[str] = []
    seen_ids: set[str] = set()

    id_key = None
    status_key = None
    test_key = None
    for row in rows:
        if id_key is None:
            for key in row:
                if key in ("id", "requirement", "requirement id"):
                    id_key = key
                if key in ("status",):
                    status_key = key
                if "test" in key:
                    test_key = key
        break

    if not rows:
        errors.append("traceability.md has no table rows")
    else:
        if id_key is None or status_key is None or test_key is None:
            errors.append(
                "traceability.md table is missing an id, status, or test-node column"
            )
        else:
            for row in rows:
                row_id = _extract_id(row.get(id_key, ""))
                if row_id is None:
                    errors.append(f"row has no recognizable LWP-R id: {row}")
                    continue
                if row_id not in requirement_ids:
                    errors.append(
                        f"traceability row names unknown id {row_id} "
                        "(not a heading in requirements.md)"
                    )
                    continue
                seen_ids.add(row_id)

                status = row.get(status_key, "").strip().lower()
                nodes = _test_nodes(row.get(test_key, ""))
                if status == "proven":
                    if not nodes:
                        errors.append(f"{row_id}: status 'proven' names no test node")
                        continue
                    if not any(_resolve_node(repo, node) for node in nodes):
                        errors.append(
                            f"{row_id}: status 'proven' but no named test node "
                            f"resolves ({', '.join(nodes)})"
                        )
                elif status == "planned":
                    pass
                else:
                    errors.append(f"{row_id}: unrecognized status '{status}'")

    missing = sorted(requirement_ids - seen_ids, key=lambda s: int(s[len("LWP-R"):]))
    for missing_id in missing:
        errors.append(f"{missing_id} has no row in traceability.md")

    if errors:
        print("lwp-trace check failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("lwp-trace check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
