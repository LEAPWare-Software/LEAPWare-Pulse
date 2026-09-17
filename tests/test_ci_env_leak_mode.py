"""The env-leak CI step must run in the mode the tree can actually pass.

`scripts/lwp_check_env_leak.py --range A..B` ADDS a range scan to the
full-tree scan; it does not replace it. `--range-only` skips the full-tree
scan. For D0 and D1 the full-tree scan cannot pass -- `docs/evidence/*.md`
carries absolute local paths on purpose until D2 drops it (plan.md,
"Dispositions") -- so CI must pass `--range-only` or every PR fails.

This test is deliberately self-retiring: the day `docs/evidence/` leaves
the tree (D2), it flips and starts REQUIRING that `--range-only` be
removed, so the full-tree scan goes back to gating every PR instead of
quietly staying disabled forever.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CI = REPO_ROOT / ".github" / "workflows" / "ci.yml"
EVIDENCE = REPO_ROOT / "docs" / "evidence"


def _env_leak_step() -> str:
    """The ci.yml text from the env-leak step up to the next step."""
    text = CI.read_text(encoding="utf-8")
    marker = "lwp_check_env_leak.py"
    assert marker in text, "ci.yml no longer runs the env-leak check at all"
    start = text.index("- name: lwp-env-leak")
    rest = text[start + 1 :]
    end = rest.find("\n      - name: ")
    return rest if end == -1 else rest[:end]


def test_env_leak_step_runs_in_range_mode() -> None:
    step = _env_leak_step()
    assert "--range " in step or "--range\n" in step or "--range$" in step or "--range" in step
    assert "github.event.pull_request.base.sha" in step
    assert "github.event.pull_request.head.sha" in step


def test_env_leak_mode_matches_what_the_tree_can_pass() -> None:
    step = _env_leak_step()
    if EVIDENCE.exists():
        assert "--range-only" in step, (
            "docs/evidence/ still carries absolute local paths, so the "
            "full-tree env-leak scan cannot pass. ci.yml must use "
            "--range-only until D2 drops that directory."
        )
    else:
        assert "--range-only" not in step, (
            "docs/evidence/ is gone (D2), so the full-tree env-leak scan "
            "must gate every PR again: drop --range-only from ci.yml and "
            "add the full-tree step back."
        )
