"""Tests for scripts/lwp_lanes.py: path classification, trailer parsing,
the bootstrap exception, and the review-record cross-check."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import lwp_lanes  # noqa: E402


def test_classify_claude_prefixes():
    assert lwp_lanes.classify_path("plugins/claude/lwp/bin/lwp_hook.py") == "claude"
    assert lwp_lanes.classify_path("adapters/claude/hook_io.py") == "claude"


def test_classify_codex_prefixes():
    assert lwp_lanes.classify_path("plugins/codex/lwp/bin/lwp_hook.py") == "codex"
    assert lwp_lanes.classify_path("adapters/codex/hook_io.py") == "codex"


def test_classify_shared_prefixes_and_files():
    for path in ("core/lwp_core/engine.py", "scripts/lwp_lanes.py", ".github/workflows/ci.yml",
                 "docs/architecture.md", "proof/schema.json", "reviews/README.md",
                 "HANDOFF.md", "AGENTS.md", "CLAUDE.md", "README.md"):
        assert lwp_lanes.classify_path(path) == "shared", path


def test_classify_tests_subdirectory():
    assert lwp_lanes.classify_path("tests/adapters/fixtures/claude/pretooluse_read.json") == "claude"
    assert lwp_lanes.classify_path("tests/adapters/fixtures/codex/pretooluse_read.json") == "codex"


def test_classify_named_test_module_extension():
    assert lwp_lanes.classify_path("tests/adapters/test_claude_hook_io.py") == "claude"
    assert lwp_lanes.classify_path("tests/adapters/test_codex_hook_io.py") == "codex"


def test_classify_other_for_unrelated_path():
    assert lwp_lanes.classify_path("examples/policies/example-routing.json") == "other"


def test_bootstrap_exception_skips_pr_4():
    # rev_range irrelevant since pr_number gate short-circuits before any git call
    assert lwp_lanes.check_lanes("HEAD~1..HEAD", 4) == []
    assert lwp_lanes.check_lanes("HEAD~1..HEAD", 1) == []


def test_commit_agent_parses_trailer(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    (repo / "f.txt").write_text("x", encoding="utf-8")
    subprocess.run(["git", "add", "f.txt"], cwd=repo, check=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", "msg\n\nLWP-Agent: claude"],
        cwd=repo,
        check=True,
    )
    sha = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()

    original_root = lwp_lanes.REPO_ROOT
    try:
        lwp_lanes.REPO_ROOT = repo
        assert lwp_lanes.commit_agent(sha) == "claude"
        assert lwp_lanes.commit_files(sha) == ["f.txt"]
    finally:
        lwp_lanes.REPO_ROOT = original_root


def test_check_lanes_flags_out_of_lane_commit(tmp_path):
    repo = tmp_path / "repo-out-of-lane"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)

    (repo / "README.md").write_text("base\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "base"], cwd=repo, check=True)
    base = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()

    claude_dir = repo / "plugins" / "claude" / "lwp"
    claude_dir.mkdir(parents=True)
    (claude_dir / "f.txt").write_text("x", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", "codex touches claude lane\n\nLWP-Agent: codex"],
        cwd=repo,
        check=True,
    )
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()

    original_root = lwp_lanes.REPO_ROOT
    try:
        lwp_lanes.REPO_ROOT = repo
        errors = lwp_lanes.check_lanes(f"{base}..{head}", 9)
    finally:
        lwp_lanes.REPO_ROOT = original_root

    assert any("outside the codex lane" in e for e in errors)


def test_review_ok_requires_distinct_reviewer_and_author_identity(tmp_path):
    reviews_dir = tmp_path / "reviews" / "9"
    reviews_dir.mkdir(parents=True)
    (reviews_dir / "claude-cto.json").write_text(
        json.dumps(
            {
                "pr": 9,
                "reviewer_agent": "claude",
                "reviewer_id": "same-session",
                "commit_author_agent": "codex",
                "commit_author_id": "same-session",
                "verdict": "AGREE",
            }
        ),
        encoding="utf-8",
    )

    original_root = lwp_lanes.REPO_ROOT
    try:
        lwp_lanes.REPO_ROOT = tmp_path
        errors: list[str] = []
        ok = lwp_lanes._review_ok(9, "claude", "deadbeef", errors)
    finally:
        lwp_lanes.REPO_ROOT = original_root

    assert ok is False
    assert any("equals" in e for e in errors)


def test_review_ok_missing_review_record_fails(tmp_path):
    original_root = lwp_lanes.REPO_ROOT
    try:
        lwp_lanes.REPO_ROOT = tmp_path
        errors: list[str] = []
        ok = lwp_lanes._review_ok(42, "codex", "cafef00d", errors)
    finally:
        lwp_lanes.REPO_ROOT = original_root

    assert ok is False
    assert any("missing required review" in e for e in errors)
