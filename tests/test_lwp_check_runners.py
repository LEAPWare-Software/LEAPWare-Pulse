"""Tests for scripts/lwp_check_runners.py (LWP-R39).

Every case builds a throwaway fixture repository (just a
``.github/workflows`` directory, no git needed) under pytest's ``tmp_path``.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "lwp_check_runners.py"

PASSING_WORKFLOW = """\
name: CI

on:
  push:
    branches: [main]

jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [windows-latest, macos-latest, ubuntu-latest]
        python-version: ["3.10", "3.12"]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v7

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
"""

SELF_HOSTED_WORKFLOW = """\
name: CI

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v7
"""

SELF_HOSTED_IN_MATRIX_WORKFLOW = """\
name: CI

on:
  push:
    branches: [main]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, self-hosted]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v7
"""

GROUP_MAPPING_WORKFLOW = """\
name: CI

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on:
      group: my-custom-group
      labels: [ubuntu-latest]
    steps:
      - uses: actions/checkout@v7
"""


def _write_workflow(repo: Path, content: str, name: str = "ci.yml") -> None:
    workflows = repo / ".github" / "workflows"
    workflows.mkdir(parents=True, exist_ok=True)
    (workflows / name).write_text(content, encoding="utf-8")


def _run_check(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(repo)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_passing_case(tmp_path: Path) -> None:
    _write_workflow(tmp_path, PASSING_WORKFLOW)
    result = _run_check(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "lwp-runners check passed" in result.stdout


def test_self_hosted_runs_on_fails_and_names_file_and_job(tmp_path: Path) -> None:
    _write_workflow(tmp_path, SELF_HOSTED_WORKFLOW)
    result = _run_check(tmp_path)
    assert result.returncode == 1
    assert "ci.yml" in result.stderr
    assert "test" in result.stderr
    assert "self-hosted" in result.stderr


def test_self_hosted_in_matrix_os_list_fails(tmp_path: Path) -> None:
    _write_workflow(tmp_path, SELF_HOSTED_IN_MATRIX_WORKFLOW)
    result = _run_check(tmp_path)
    assert result.returncode == 1
    assert "self-hosted" in result.stderr
    assert "test" in result.stderr


def test_runner_group_mapping_fails(tmp_path: Path) -> None:
    _write_workflow(tmp_path, GROUP_MAPPING_WORKFLOW)
    result = _run_check(tmp_path)
    assert result.returncode == 1
    assert "group" in result.stderr
    assert "test" in result.stderr


def test_self_hosted_reached_through_matrix_include_fails(tmp_path):
    """`include:` can add a matrix leg with its own `os:`.

    Found by the independent D0 check: reading only `matrix.os` let a job
    route to a self-hosted runner while the listed `os` values were all
    GitHub-hosted, and LWP-R39's check passed it.
    """
    wf = tmp_path / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "sneaky.yml").write_text(
        "name: Sneaky\n"
        "on: [push]\n"
        "jobs:\n"
        "  build:\n"
        "    strategy:\n"
        "      matrix:\n"
        "        os: [ubuntu-latest]\n"
        "        include:\n"
        "          - os: self-hosted\n"
        "    runs-on: ${{ matrix.os }}\n"
        "    steps:\n"
        "      - run: echo hi\n",
        encoding="utf-8",
    )
    result = _run_check(tmp_path)
    out = result.stdout + result.stderr
    assert result.returncode == 1, "a self-hosted leg added via matrix.include must fail LWP-R39"
    assert "self-hosted" in out
    assert "sneaky.yml" in out
    assert "build" in out


def test_github_hosted_matrix_include_still_passes(tmp_path):
    wf = tmp_path / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "fine.yml").write_text(
        "name: Fine\n"
        "on: [push]\n"
        "jobs:\n"
        "  build:\n"
        "    strategy:\n"
        "      matrix:\n"
        "        os: [ubuntu-latest]\n"
        "        include:\n"
        "          - os: macos-latest\n"
        "    runs-on: ${{ matrix.os }}\n"
        "    steps:\n"
        "      - run: echo hi\n",
        encoding="utf-8",
    )
    proc = _run_check(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
