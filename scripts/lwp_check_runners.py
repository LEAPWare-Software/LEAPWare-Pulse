#!/usr/bin/env python3
"""lwp-runners: enforce LWP-R39 (GitHub-hosted runners only).

Rule (LWP-R39): every ``runs-on`` in every ``.github/workflows/*.yml``,
including each value a matrix expression can expand to, is a GitHub-hosted
label matching ``ubuntu-*``, ``windows-*`` or ``macos-*``. Never
``self-hosted``, a custom label, a runner group, or a local runner.

This is a small, targeted parser for the narrow YAML subset GitHub Actions
workflow files actually use for ``jobs.<id>.runs-on`` and
``jobs.<id>.strategy.matrix.<key>`` -- not a general YAML parser. Standard
library only (no PyYAML).

Exits 0 and prints ``lwp-runners check passed`` when every ``runs-on`` in
every workflow resolves to an allowed hosted label. Otherwise exits 1 and
names the offending file and job.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ALLOWED_PATTERN = re.compile(r"^(ubuntu|windows|macos)-.+$")


def _strip_comment(line: str) -> str:
    """Strip a trailing ``# ...`` comment (best-effort, no quoting awareness)."""
    idx = line.find("#")
    if idx == -1:
        return line
    return line[:idx]


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _parse_flow_list(value: str) -> list[str]:
    inner = value.strip()
    if inner.startswith("[") and inner.endswith("]"):
        inner = inner[1:-1]
    items = [_unquote(item) for item in inner.split(",") if item.strip()]
    return items


class WorkflowError(Exception):
    def __init__(self, job: str, reason: str) -> None:
        self.job = job
        self.reason = reason
        super().__init__(f"{job}: {reason}")


def _read_lines(text: str) -> list[tuple[int, str]]:
    """Return (indent, stripped-content) for every non-blank, non-comment line."""
    result = []
    for raw in text.splitlines():
        stripped = _strip_comment(raw).rstrip()
        if not stripped.strip():
            continue
        result.append((_indent(stripped), stripped.strip()))
    return result


def _collect_block_list(lines: list[tuple[int, str]], start: int, parent_indent: int) -> tuple[list, int]:
    """Collect a ``- item`` block sequence starting at ``start``.

    An item that is itself a ``key: value`` mapping comes back as a dict,
    with any deeper continuation lines folded into the same mapping, so

        include:
          - os: self-hosted
            python-version: "3.12"

    yields ``[{"os": "self-hosted", "python-version": "3.12"}]`` rather than
    the string ``"os: self-hosted"`` with the second key dropped. A plain
    scalar item still comes back as a string. Found by the independent D0
    check: `matrix.include:` legs were being read as opaque strings, so a
    self-hosted leg declared there was invisible to LWP-R39.
    """
    items: list = []
    idx = start
    while idx < len(lines):
        indent, content = lines[idx]
        if indent <= parent_indent or not content.startswith("-"):
            break
        item = content[1:].strip()
        idx += 1
        if not item:
            continue
        if ":" in item:
            key, _, value = item.partition(":")
            mapping: dict[str, object] = {key.strip(): _unquote(value.strip())}
            # Fold in continuation keys of this same list item: deeper than
            # the dash, and not themselves a new item.
            while idx < len(lines):
                cont_indent, cont_content = lines[idx]
                if cont_indent <= indent or cont_content.startswith("-"):
                    break
                if ":" in cont_content:
                    ckey, _, cvalue = cont_content.partition(":")
                    mapping[ckey.strip()] = _unquote(cvalue.strip())
                idx += 1
            items.append(mapping)
        else:
            items.append(_unquote(item))
    return items, idx


def _collect_mapping_keys(lines: list[tuple[int, str]], start: int, parent_indent: int) -> tuple[dict, int]:
    """Collect ``key: value`` (and nested block-list) entries deeper than ``parent_indent``."""
    mapping: dict[str, object] = {}
    idx = start
    while idx < len(lines):
        indent, content = lines[idx]
        if indent <= parent_indent:
            break
        if ":" not in content:
            idx += 1
            continue
        key, _, value = content.partition(":")
        key = key.strip()
        value = value.strip()
        if value:
            mapping[key] = value
            idx += 1
        else:
            # Nested block: either a list or a sub-mapping.
            next_idx = idx + 1
            if next_idx < len(lines) and lines[next_idx][0] > indent and lines[next_idx][1].startswith("-"):
                items, next_idx = _collect_block_list(lines, next_idx, indent)
                mapping[key] = items
            elif next_idx < len(lines) and lines[next_idx][0] > indent:
                sub, next_idx = _collect_mapping_keys(lines, next_idx, indent)
                mapping[key] = sub
            else:
                mapping[key] = None
            idx = next_idx
    return mapping, idx


def _matrix_include_os_values(matrix: dict) -> list[str]:
    """Runner labels added through `matrix.include:`.

    `include:` is a real GitHub Actions mechanism for adding a matrix leg,
    and a leg added there can carry its own `os:`. Reading only
    `matrix.os` misses it entirely:

        strategy:
          matrix:
            os: [ubuntu-latest]
            include:
              - os: self-hosted
          runs-on: ${{ matrix.os }}

    That job runs on a self-hosted runner while `matrix.os` lists nothing
    but `ubuntu-latest`. Found by the independent D0 check (LWP-R39).
    """
    include = matrix.get("include")
    values: list[str] = []
    if isinstance(include, list):
        for leg in include:
            if isinstance(leg, dict):
                leg_os = leg.get("os")
                if isinstance(leg_os, str):
                    values.append(leg_os)
                elif isinstance(leg_os, list):
                    values.extend(v for v in leg_os if isinstance(v, str))
    return values


def _matrix_os_values(job: dict) -> list[str]:
    strategy = job.get("strategy")
    if not isinstance(strategy, dict):
        return []
    matrix = strategy.get("matrix")
    if not isinstance(matrix, dict):
        return []
    included = _matrix_include_os_values(matrix)
    os_value = matrix.get("os")
    if os_value is None:
        return included
    if isinstance(os_value, list):
        values: list[str] = list(included)
        for item in os_value:
            if isinstance(item, dict):
                # A mapping inside an `os:` list is not a runner label; the
                # include-leg reader above already handled those.
                continue
            if isinstance(item, str) and item.strip().startswith("["):
                values.extend(_parse_flow_list(item))
            elif isinstance(item, str):
                values.append(item)
        return values
    if isinstance(os_value, str):
        return included + _parse_flow_list(os_value)
    return included


def _check_runs_on(job_name: str, job: dict) -> list[str]:
    errors: list[str] = []
    runs_on = job.get("runs-on")

    if isinstance(runs_on, dict):
        if "group" in runs_on:
            errors.append(f"job '{job_name}' uses a runner group mapping (runs-on.group)")
        else:
            errors.append(f"job '{job_name}' uses a runs-on mapping instead of a hosted label")
        return errors

    if runs_on is None:
        errors.append(f"job '{job_name}' has no runs-on")
        return errors

    raw = str(runs_on)
    if "matrix." in raw:
        os_values = _matrix_os_values(job)
        if not os_values:
            errors.append(
                f"job '{job_name}' runs-on references a matrix expression "
                f"('{raw}') but no strategy.matrix.os values could be resolved"
            )
            return errors
        candidates = os_values
    else:
        candidates = [_unquote(raw)]

    for candidate in candidates:
        if candidate == "self-hosted":
            errors.append(f"job '{job_name}' uses self-hosted runner label '{candidate}'")
        elif not ALLOWED_PATTERN.match(candidate):
            errors.append(
                f"job '{job_name}' uses runner label '{candidate}' "
                "(must match ubuntu-*, windows-*, or macos-*)"
            )

    # Also check every declared matrix.os value even when runs-on itself is a
    # literal (a matrix os list can still be self-hosted even if unused by
    # runs-on today -- LWP-R39 requires every value a matrix expression CAN
    # expand to, so check the matrix definition regardless).
    for candidate in _matrix_os_values(job):
        if candidate == "self-hosted":
            msg = f"job '{job_name}' has self-hosted in its matrix os list"
            if msg not in errors:
                errors.append(msg)
        elif not ALLOWED_PATTERN.match(candidate):
            msg = (
                f"job '{job_name}' has matrix os value '{candidate}' "
                "(must match ubuntu-*, windows-*, or macos-*)"
            )
            if msg not in errors:
                errors.append(msg)

    return errors


def check_workflow_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = _read_lines(text)

    jobs_start = None
    jobs_indent = None
    for idx, (indent, content) in enumerate(lines):
        if content == "jobs:" and indent == 0:
            jobs_start = idx + 1
            jobs_indent = indent
            break
    if jobs_start is None:
        return [f"{path}: no top-level 'jobs:' key found"]

    errors: list[str] = []
    idx = jobs_start
    while idx < len(lines):
        indent, content = lines[idx]
        if indent <= jobs_indent:
            break
        # A job id line: one level deeper than 'jobs:', ends with ':'.
        job_indent = indent
        if not content.endswith(":"):
            idx += 1
            continue
        job_name = content[:-1].strip()
        job_map, next_idx = _collect_mapping_keys(lines, idx + 1, job_indent)
        for err in _check_runs_on(job_name, job_map):
            errors.append(f"{path}: {err}")
        idx = next_idx

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Enforce LWP-R39 hosted-runner-only workflows.")
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to the repository to check (default: current directory).",
    )
    args = parser.parse_args(argv)

    repo = Path(args.repo)
    workflows_dir = repo / ".github" / "workflows"
    if not workflows_dir.is_dir():
        print("lwp-runners: no .github/workflows directory found", file=sys.stderr)
        return 1

    workflow_files = sorted(workflows_dir.glob("*.yml")) + sorted(workflows_dir.glob("*.yaml"))
    if not workflow_files:
        print("lwp-runners: no workflow files found", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for workflow_file in workflow_files:
        all_errors.extend(check_workflow_file(workflow_file))

    if all_errors:
        print("lwp-runners check failed:", file=sys.stderr)
        for error in all_errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("lwp-runners check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
