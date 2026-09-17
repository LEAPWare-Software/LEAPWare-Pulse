"""Tests for scripts/lwp_check_trace.py (LWP-R12).

Every case builds a throwaway fixture directory (a minimal
``docs/requirements/requirements.md`` + ``docs/requirements/traceability.md``
+ a real test file to resolve against) under pytest's ``tmp_path``. Git is
not needed for this check -- it only reads files -- so no ``git init`` here.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "lwp_check_trace.py"

REQUIREMENTS = """\
# lwp requirements (fixture)

### LWP-R1 -- First rule
- **Rule:** something.
- **Test:** `tests/test_fixture.py` (`test_something`).
- **Break:** break it; fail.
- **Phase:** D0.

### LWP-R2 -- Second rule
- **Rule:** something else, proven in a later phase.
- **Test:** `tests/test_future.py` (`test_not_written_yet`).
- **Break:** break it; fail.
- **Phase:** D1.
"""

TRACEABILITY = """\
# Traceability matrix (fixture)

| ID | Rule summary | Phase | Status | Test node(s) | Break |
|---|---|---|---|---|---|
| LWP-R1 | First rule | D0 | proven | `tests/test_fixture.py::test_something` | break it; fail |
| LWP-R2 | Second rule | D1 | planned | `tests/test_future.py::test_not_written_yet` | break it; fail |
"""

FIXTURE_TEST_FILE = """\
def test_something():
    assert True
"""


def _write_fixture(root: Path, requirements: str = REQUIREMENTS, traceability: str = TRACEABILITY) -> Path:
    (root / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "requirements" / "requirements.md").write_text(requirements, encoding="utf-8")
    (root / "docs" / "requirements" / "traceability.md").write_text(traceability, encoding="utf-8")
    (root / "tests").mkdir(parents=True, exist_ok=True)
    (root / "tests" / "test_fixture.py").write_text(FIXTURE_TEST_FILE, encoding="utf-8")
    return root


def _run_check(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(repo)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_passing_case(tmp_path: Path) -> None:
    _write_fixture(tmp_path)
    result = _run_check(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "lwp-trace check passed" in result.stdout


def test_proven_row_with_deleted_test_function_fails(tmp_path: Path) -> None:
    _write_fixture(tmp_path)
    # Delete the test function the 'proven' row for LWP-R1 names.
    (tmp_path / "tests" / "test_fixture.py").write_text("# no tests here\n", encoding="utf-8")

    result = _run_check(tmp_path)
    assert result.returncode == 1
    assert "LWP-R1" in result.stderr


def test_id_with_no_row_fails(tmp_path: Path) -> None:
    requirements_with_extra_heading = REQUIREMENTS + (
        "\n### LWP-R99 -- Undefined example heading\n"
        "- **Rule:** example only.\n"
        "- **Test:** none yet.\n"
        "- **Break:** n/a.\n"
        "- **Phase:** D0.\n"
    )
    _write_fixture(tmp_path, requirements=requirements_with_extra_heading)

    result = _run_check(tmp_path)
    assert result.returncode == 1
    assert "LWP-R99" in result.stderr
