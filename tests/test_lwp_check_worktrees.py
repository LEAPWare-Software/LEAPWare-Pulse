"""Tests for scripts/lwp_check_worktrees.py (LWP-R9).

Every case builds a throwaway fixture repository under pytest's ``tmp_path``
via ``git init`` + subprocess. The real leapware-pulse repository is never
touched, and nothing is ever pushed anywhere.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "lwp_check_worktrees.py"

RULE_SENTENCE = "Worktrees live only under .worktrees/<branch>, never as sibling folders.\n"


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, f"git {args} failed: {result.stderr}"
    return result


def _make_fixture_repo(root: Path) -> Path:
    repo = root / "fixture-repo"
    repo.mkdir()
    _git(repo.parent, "init", str(repo))
    _git(repo, "config", "user.name", "Fixture User")
    _git(repo, "config", "user.email", "fixture@example.invalid")

    (repo / ".gitignore").write_text(".worktrees/\n", encoding="utf-8")
    (repo / "CLAUDE.md").write_text(f"# Fixture\n\n- {RULE_SENTENCE}", encoding="utf-8")
    (repo / "AGENTS.md").write_text(f"# Fixture\n\n- {RULE_SENTENCE}", encoding="utf-8")
    (repo / "README.md").write_text("fixture\n", encoding="utf-8")

    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "initial commit")
    return repo


def _run_check(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(repo)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_passing_case(tmp_path: Path) -> None:
    repo = _make_fixture_repo(tmp_path)
    result = _run_check(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "lwp-worktrees check passed" in result.stdout


def test_sibling_worktree_outside_dot_worktrees_fails(tmp_path: Path) -> None:
    repo = _make_fixture_repo(tmp_path)
    sibling_wt = repo.parent / "sibling-wt"
    _git(repo, "worktree", "add", str(sibling_wt), "-b", "sibling-branch")

    result = _run_check(repo)
    assert result.returncode == 1
    assert str(sibling_wt) in result.stderr or "sibling-wt" in result.stderr


def test_sibling_clone_of_same_origin_fails(tmp_path: Path) -> None:
    repo = _make_fixture_repo(tmp_path)
    origin_url = "https://example.invalid/leapware-pulse.git"
    _git(repo, "remote", "add", "origin", origin_url)

    sibling_clone = repo.parent / "sibling-clone"
    _git(repo.parent, "clone", str(repo), str(sibling_clone))
    _git(sibling_clone, "remote", "set-url", "origin", origin_url)

    result = _run_check(repo)
    assert result.returncode == 1
    assert "sibling-clone" in result.stderr
    assert "origin" in result.stderr


def test_gitignore_missing_worktrees_entry_fails(tmp_path: Path) -> None:
    repo = _make_fixture_repo(tmp_path)
    (repo / ".gitignore").write_text("node_modules/\n", encoding="utf-8")

    result = _run_check(repo)
    assert result.returncode == 1
    assert ".gitignore" in result.stderr


def test_missing_rule_sentence_in_claude_md_fails(tmp_path: Path) -> None:
    repo = _make_fixture_repo(tmp_path)
    (repo / "CLAUDE.md").write_text("# Fixture\n\nNothing about worktrees here.\n", encoding="utf-8")

    result = _run_check(repo)
    assert result.returncode == 1
    assert "CLAUDE.md" in result.stderr
