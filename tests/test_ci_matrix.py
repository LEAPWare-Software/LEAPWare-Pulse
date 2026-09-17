"""Shape checks for .github/workflows/ci.yml's test matrix (LWP-R6).

Not a YAML parse -- stdlib-only per LWP-R7, and the file's shape is simple
and fixed, so a small targeted parser (the same approach tokenwise's own
tests use for its rulesets) is enough to pull out the `os:` and
`python-version:` matrix lists without a third-party YAML dependency.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CI_YML = REPO_ROOT / ".github" / "workflows" / "ci.yml"

EXPECTED_OS = {"windows-latest", "macos-latest", "ubuntu-latest"}
EXPECTED_PYTHON_VERSIONS = {"3.10", "3.12"}


def _test_job_text() -> str:
    text = CI_YML.read_text(encoding="utf-8")
    # Isolate the `test:` job block: from its header to the next
    # top-level (2-space-indented) job key, or end of file.
    match = re.search(r"^  test:\n(.*?)(?=^  [A-Za-z_-]+:\n|\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, f"no 'test:' job found in {CI_YML}"
    return match.group(1)


def _matrix_list(job_text: str, key: str) -> list[str]:
    match = re.search(rf"^\s*{re.escape(key)}:\s*\[([^\]]*)\]", job_text, re.MULTILINE)
    assert match, f"no '{key}:' matrix list found in the test job"
    items = [item.strip().strip('"').strip("'") for item in match.group(1).split(",")]
    return [item for item in items if item]


def test_ci_yml_exists():
    assert CI_YML.is_file(), f"missing {CI_YML}"


def test_test_job_matrix_os_covers_all_three_platforms():
    os_list = _matrix_list(_test_job_text(), "os")
    assert set(os_list) == EXPECTED_OS, f"expected {EXPECTED_OS}, got {set(os_list)}"


def test_test_job_matrix_python_versions():
    python_versions = _matrix_list(_test_job_text(), "python-version")
    assert set(python_versions) == EXPECTED_PYTHON_VERSIONS, (
        f"expected {EXPECTED_PYTHON_VERSIONS}, got {set(python_versions)}"
    )


def test_test_job_produces_exactly_six_combinations():
    job_text = _test_job_text()
    os_list = _matrix_list(job_text, "os")
    python_versions = _matrix_list(job_text, "python-version")
    combinations = {(os, version) for os in os_list for version in python_versions}
    assert len(combinations) == 6, (
        f"expected 6 os x python-version combinations, got {len(combinations)}: {combinations}"
    )


def test_test_job_runs_on_the_matrix():
    job_text = _test_job_text()
    assert "runs-on: ${{ matrix.os }}" in job_text, (
        "the test job must run on the matrix os, not a fixed runner"
    )
