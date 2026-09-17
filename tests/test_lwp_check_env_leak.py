"""Tests for scripts/lwp_check_env_leak.py, working tree AND `--range` history scan.

A working-tree-only scan misses a leak that was committed and then removed
again within the same PR -- it is still sitting in the branch's history,
which a clone or marketplace pull carries in full. These tests build a
throwaway fixture git repo (never this repo's own history) to prove the
`--range` scan catches exactly that case.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import lwp_check_env_leak as check_mod


def _run(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=str(cwd), capture_output=True, text=True, check=True)


def _init_repo(cwd: Path) -> None:
    _run(["git", "init", "-q"], cwd)
    _run(["git", "config", "user.name", "Fixture"], cwd)
    _run(["git", "config", "user.email", "fixture@example.com"], cwd)


def test_findings_for_line_catches_drive_letter_and_private_name():
    findings = check_mod._findings_for_line(
        "some/file.py", 3, r'path = "C:\Users\someone\example-private-project"'
    )
    assert any("Windows drive letter" in f for f in findings)
    assert any("private-project name leak" in f and "example-private-project" in f for f in findings)


def test_findings_for_line_clean_line_has_no_findings():
    assert check_mod._findings_for_line("some/file.py", 1, "print('hello world')") == []


def test_range_scan_catches_leak_committed_then_reverted(tmp_path):
    repo = tmp_path / "fixture-repo"
    repo.mkdir()
    _init_repo(repo)

    target = repo / "notes.md"
    target.write_text("nothing interesting here\n", encoding="utf-8")
    _run(["git", "add", "notes.md"], repo)
    _run(["git", "commit", "-q", "-m", "base"], repo)
    base_sha = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()

    # Commit 1: add a leak.
    target.write_text(
        "nothing interesting here\nsee C:\\Users\\someone\\example-private-project\\notes\n",
        encoding="utf-8",
    )
    _run(["git", "add", "notes.md"], repo)
    _run(["git", "commit", "-q", "-m", "add a note"], repo)

    # Commit 2: remove it again -- gone from the working tree and from the
    # base..head net diff of an unrelated line-count check, but NOT gone
    # from the range's own commit history.
    target.write_text("nothing interesting here\n", encoding="utf-8")
    _run(["git", "add", "notes.md"], repo)
    _run(["git", "commit", "-q", "-m", "revert the note"], repo)
    head_sha = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()

    original_root = check_mod.REPO_ROOT
    try:
        check_mod.REPO_ROOT = repo
        # Working tree is clean: the leak was reverted before HEAD.
        assert check_mod.check() == []
        # But the range scan still finds it in the intermediate commit.
        findings = check_mod.check_range(f"{base_sha}..{head_sha}")
    finally:
        check_mod.REPO_ROOT = original_root

    assert any("private-project name leak" in f and "example-private-project" in f for f in findings)
    assert any("Windows drive letter" in f for f in findings)


def test_range_scan_clean_history_has_no_findings(tmp_path):
    repo = tmp_path / "fixture-repo-clean"
    repo.mkdir()
    _init_repo(repo)

    target = repo / "notes.md"
    target.write_text("first\n", encoding="utf-8")
    _run(["git", "add", "notes.md"], repo)
    _run(["git", "commit", "-q", "-m", "base"], repo)
    base_sha = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()

    target.write_text("first\nsecond, nothing sensitive\n", encoding="utf-8")
    _run(["git", "add", "notes.md"], repo)
    _run(["git", "commit", "-q", "-m", "add a clean line"], repo)
    head_sha = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()

    original_root = check_mod.REPO_ROOT
    try:
        check_mod.REPO_ROOT = repo
        findings = check_mod.check_range(f"{base_sha}..{head_sha}")
    finally:
        check_mod.REPO_ROOT = original_root

    assert findings == []


def test_range_scan_skips_exempt_fixture_paths(tmp_path):
    repo = tmp_path / "fixture-repo-exempt"
    repo.mkdir()
    _init_repo(repo)

    fixture_dir = repo / "tests" / "fixtures"
    fixture_dir.mkdir(parents=True)
    target = fixture_dir / "sample.json"
    target.write_text("{}\n", encoding="utf-8")
    _run(["git", "add", "."], repo)
    _run(["git", "commit", "-q", "-m", "base"], repo)
    base_sha = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()

    target.write_text('{"path": "C:\\\\Users\\\\someone\\\\example-private-project"}\n', encoding="utf-8")
    _run(["git", "add", "."], repo)
    _run(["git", "commit", "-q", "-m", "edit fixture"], repo)
    head_sha = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()

    original_root = check_mod.REPO_ROOT
    try:
        check_mod.REPO_ROOT = repo
        findings = check_mod.check_range(f"{base_sha}..{head_sha}")
    finally:
        check_mod.REPO_ROOT = original_root

    assert findings == []


def test_private_name_substrings_default_only_when_file_absent(tmp_path):
    original_root = check_mod.REPO_ROOT
    try:
        check_mod.REPO_ROOT = tmp_path
        assert check_mod._private_name_substrings() == check_mod.DEFAULT_PRIVATE_NAME_SUBSTRINGS
    finally:
        check_mod.REPO_ROOT = original_root


def test_private_name_substrings_reads_local_gitignored_file(tmp_path):
    (tmp_path / check_mod.PRIVATE_NAMES_FILE).write_text(
        "# comment, ignored\n\nAdoptersSecretProject\n", encoding="utf-8"
    )
    original_root = check_mod.REPO_ROOT
    try:
        check_mod.REPO_ROOT = tmp_path
        names = check_mod._private_name_substrings()
        assert names == check_mod.DEFAULT_PRIVATE_NAME_SUBSTRINGS + ["adopterssecretproject"]
        findings = check_mod._findings_for_line("some/file.py", 1, "path = AdoptersSecretProject/thing")
        assert any("adopterssecretproject" in f for f in findings)
    finally:
        check_mod.REPO_ROOT = original_root


def test_range_only_flag_skips_full_tree_scan(tmp_path):
    """--range-only: a leaky file already sitting in the tree (unrelated to
    the range) must NOT fail the check -- only the range's added lines are
    scanned. This is what LWP-D0/D1 CI relies on: docs/evidence/*.md
    intentionally carries absolute paths until D2 (see plan.md), so a
    full-tree scan cannot gate D0/D1 PRs; --range-only can.
    """
    repo = tmp_path / "fixture-range-only"
    repo.mkdir()
    _init_repo(repo)

    # A pre-existing leaky file, present at both base and head -- not part
    # of the range's added lines, so --range-only must ignore it even
    # though a full-tree scan would catch it.
    leaky = repo / "pre-existing.md"
    leaky.write_text("see C:\\Users\\someone\\notes for details\n", encoding="utf-8")
    _run(["git", "add", "."], repo)
    _run(["git", "commit", "-q", "-m", "base with pre-existing leak"], repo)
    base_sha = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()

    clean = repo / "clean.md"
    clean.write_text("nothing sensitive here\n", encoding="utf-8")
    _run(["git", "add", "."], repo)
    _run(["git", "commit", "-q", "-m", "add a clean file"], repo)
    head_sha = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()

    # main() derives REPO_ROOT from the script's own file location, not
    # cwd, so exercise it in-process with REPO_ROOT monkeypatched (a
    # subprocess launch of the script would always scan the REAL repo,
    # not this fixture, regardless of cwd).
    original_root = check_mod.REPO_ROOT
    original_argv = sys.argv
    try:
        check_mod.REPO_ROOT = repo
        sys.argv = ["lwp_check_env_leak.py", "--range", f"{base_sha}..{head_sha}", "--range-only"]
        exit_code = check_mod.main()
    finally:
        check_mod.REPO_ROOT = original_root
        sys.argv = original_argv
    assert exit_code == 0

    # Without --range-only, the same repo's full-tree scan DOES catch it.
    try:
        check_mod.REPO_ROOT = repo
        sys.argv = ["lwp_check_env_leak.py"]
        exit_code_full = check_mod.main()
    finally:
        check_mod.REPO_ROOT = original_root
        sys.argv = original_argv
    assert exit_code_full == 1


def test_full_tree_scan_of_fixture_tree_catches_absolute_path(tmp_path):
    """Full-tree mode (no --range) against a synthetic tree -- NEVER the
    real repo. The real repo's docs/evidence/*.md intentionally carries
    absolute local paths until D2 (see plan.md dispositions) and is
    expected to fail a full-tree scan today; that is not exercised here.
    """
    repo = tmp_path / "fixture-full-tree"
    repo.mkdir()
    _init_repo(repo)
    leaky = repo / "leaky.md"
    leaky.write_text("see C:\\Users\\someone\\notes for details\n", encoding="utf-8")
    _run(["git", "add", "leaky.md"], repo)
    _run(["git", "commit", "-q", "-m", "base"], repo)

    original_root = check_mod.REPO_ROOT
    try:
        check_mod.REPO_ROOT = repo
        findings = check_mod.check()
    finally:
        check_mod.REPO_ROOT = original_root

    assert any("Windows drive letter" in f for f in findings)


def test_fixture_exemption_is_scoped_to_the_tests_tree():
    """A path outside tests/ cannot buy an exemption by having 'fixture'
    in its name.

    Caught by the D0 break/restore run: a planted leak in a root-level
    `leak_fixture.md` was waved through, because the exemption was a bare
    `"fixture" in path` over the whole repo while the docstring claimed it
    was scoped to tests/**/fixtures/**.
    """
    assert check_mod._is_exempt_posix("tests/fixtures/proof/sample.json") is True
    assert check_mod._is_exempt_posix("tests/test_lwp_check_prefix_fixture.py") is True

    assert check_mod._is_exempt_posix("leak_fixture.md") is False
    assert check_mod._is_exempt_posix("docs/fixture-notes.md") is False
    assert check_mod._is_exempt_posix("plugins/LEAPWare-Pulse/fixtures/thing.json") is False


def test_range_scan_catches_a_leak_only_in_a_commit_message(tmp_path):
    """A clone carries commit messages in full.

    Found by the independent D0 check: an empty commit whose message held a
    drive-letter path passed the range scan, because only diff hunks were
    ever read.
    """
    repo = tmp_path / "fixture-repo"
    repo.mkdir()
    run = lambda *a: subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True)
    run("init", "-q")
    run("config", "user.name", "Fixture")
    run("config", "user.email", "fixture@example.invalid")
    (repo / "README.md").write_text("clean\n", encoding="utf-8")
    run("add", "README.md")
    run("commit", "-q", "-m", "base commit, nothing to see")
    base = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True
    ).stdout.strip()
    run(
        "commit",
        "-q",
        "--allow-empty",
        "-m",
        "notes: built from " + "C:" + chr(92) + "Users" + chr(92) + "realperson, no file change",
    )

    original_root = check_mod.REPO_ROOT
    try:
        check_mod.REPO_ROOT = repo
        findings = check_mod.check_range_messages(f"{base}..HEAD")
    finally:
        check_mod.REPO_ROOT = original_root

    assert findings, "a drive-letter path in a commit message must be caught"
    assert any("commit message" in f for f in findings)


BACKSLASH = chr(92)


def test_a_path_wrapped_across_two_lines_is_caught():
    """Detection is per-line, so a path that merely wraps was invisible.

    Found by the independent D0 check against the commit-message scanner;
    the file and diff scanners had the same blind spot from the start. The
    path is fully present and usable in the file -- it is just split.
    """
    lines = [
        "built from C:",
        BACKSLASH + "Users" + BACKSLASH + "realperson" + BACKSLASH + "proj.txt",
    ]
    findings = check_mod._findings_for_text("(test)", lines)
    assert findings, "a drive-letter path split across two lines must be caught"
    assert any("wrapped across lines" in f for f in findings)


def test_wrapping_does_not_invent_findings_from_unrelated_lines():
    assert check_mod._findings_for_text("(test)", ["see the docs", "for details"]) == []
    assert check_mod._findings_for_text("(test)", ["nothing here", "or here either"]) == []


def test_a_wrapped_hit_is_not_double_counted():
    """A leak fully on one line is reported once, not again as 'wrapped'."""
    lines = ["a C:" + BACKSLASH + "Users" + BACKSLASH + "bob here", "next line"]
    findings = check_mod._findings_for_text("(test)", lines)
    assert len(findings) == 1
    assert "wrapped" not in findings[0]


def test_a_leak_on_the_second_line_of_a_pair_is_not_double_reported():
    """Dedup must compare finding KIND, not the line-tagged string.

    Round three of the independent check found 42 spurious "wrapped"
    duplicates on this repo's own tree: the joined text is always tagged
    with the pair's FIRST line number, so a real leak living entirely on
    the SECOND line produced two differently-tagged strings that could
    never compare equal.
    """
    lines = ["a harmless first line", "leak here C:" + BACKSLASH + "Users" + BACKSLASH + "bob x"]
    findings = check_mod._findings_for_text("(test)", lines)
    assert len(findings) == 1, f"expected one finding, got {findings}"
    assert "wrapped" not in findings[0]


def test_the_real_tree_reports_no_wrapped_duplicates():
    """Regression guard on the actual repository, not a fixture."""
    findings = check_mod.check()
    wrapped = [f for f in findings if "wrapped across lines" in f]
    assert wrapped == [], f"wrapped duplicates reappeared: {wrapped[:5]}"
