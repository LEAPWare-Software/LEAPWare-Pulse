"""Tests for scripts/lwp_check_commit_identity.py (LWP-R2): allow-list
logic, range mode, and full-history mode with the legacy boundary.

Uses synthetic name/email pairs and a throwaway fixture git repo (never
this repo's own history), so these tests do not depend on this repo's own
history staying a particular shape.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import lwp_check_commit_identity as check_mod  # noqa: E402


def _run(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=str(cwd), capture_output=True, text=True, check=True)


def _init_repo(cwd: Path) -> None:
    _run(["git", "init", "-q"], cwd)
    _run(["git", "config", "user.name", "Fixture"], cwd)
    _run(["git", "config", "user.email", "fixture@example.com"], cwd)


def _commit(repo: Path, filename: str, content: str, message: str, name: str, email: str) -> str:
    target = repo / filename
    target.write_text(content, encoding="utf-8")
    _run(["git", "add", filename], repo)
    _run(
        [
            "git",
            "-c",
            f"user.name={name}",
            "-c",
            f"user.email={email}",
            "commit",
            "-q",
            "-m",
            message,
        ],
        repo,
    )
    return _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()


# ---- _is_allowed unit checks -------------------------------------------------


def test_leapware_identity_allowed():
    assert check_mod._is_allowed("LEAPWare", "leapware@outlook.com")


def test_dependabot_bot_identity_allowed():
    assert check_mod._is_allowed(
        "dependabot[bot]", "49699333+dependabot[bot]@users.noreply.github.com"
    )


def test_random_human_identity_flagged():
    assert not check_mod._is_allowed("Someone Else", "someone@example.com")


def test_bot_name_without_bot_email_flagged():
    assert not check_mod._is_allowed("dependabot[bot]", "attacker@example.com")


# ---- range mode ---------------------------------------------------------------


def test_range_mode_leapware_commits_pass(tmp_path):
    repo = tmp_path / "range-ok"
    repo.mkdir()
    _init_repo(repo)
    _commit(repo, "a.txt", "1", "base", "LEAPWare", "leapware@outlook.com")
    base = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
    _commit(repo, "a.txt", "2", "second", "LEAPWare", "leapware@outlook.com")
    head = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()

    assert check_mod.check(f"{base}..{head}", cwd=repo) == []


def test_range_mode_wrong_author_fails(tmp_path):
    repo = tmp_path / "range-bad"
    repo.mkdir()
    _init_repo(repo)
    _commit(repo, "a.txt", "1", "base", "LEAPWare", "leapware@outlook.com")
    base = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
    _commit(repo, "a.txt", "2", "second", "Someone Else", "someone@example.com")
    head = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()

    findings = check_mod.check(f"{base}..{head}", cwd=repo)
    assert any("Someone Else" in f for f in findings)


# ---- full-history mode with legacy boundary -----------------------------------


def test_full_history_legacy_commits_below_boundary_are_not_failures(tmp_path):
    repo = tmp_path / "history-ok"
    repo.mkdir()
    _init_repo(repo)
    # Legacy commit, foreign identity -- this becomes the boundary.
    _commit(repo, "a.txt", "1", "legacy work", "Old Contributor", "old@example.com")
    boundary = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
    # Post-boundary commit, correct identity.
    _commit(repo, "a.txt", "2", "post-boundary work", "LEAPWare", "leapware@outlook.com")
    head = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()

    findings, legacy_count = check_mod.check_full_history(head, boundary, cwd=repo)
    assert findings == []
    assert legacy_count == 1


def test_full_history_legacy_identity_above_boundary_fails(tmp_path):
    repo = tmp_path / "history-bad"
    repo.mkdir()
    _init_repo(repo)
    _commit(repo, "a.txt", "1", "legacy work", "Old Contributor", "old@example.com")
    boundary = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
    # Break: a legacy-identity commit AFTER the boundary must still fail.
    _commit(repo, "a.txt", "2", "should not happen", "Old Contributor", "old@example.com")
    head = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()

    findings, legacy_count = check_mod.check_full_history(head, boundary, cwd=repo)
    assert legacy_count == 1
    assert any("Old Contributor" in f for f in findings)


def test_main_full_history_against_real_boundary_constant_type():
    # The shipped default boundary is a plausible 40-hex sha, not a magic
    # literal accidentally left as a placeholder.
    assert len(check_mod.LEGACY_BOUNDARY_SHA) == 40
    assert all(c in "0123456789abcdef" for c in check_mod.LEGACY_BOUNDARY_SHA)
