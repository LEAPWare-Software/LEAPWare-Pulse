#!/usr/bin/env python3
"""CI check: every commit author is LEAPWare, or an allow-listed GitHub bot.

This repo's commit identity is `LEAPWare <leapware@outlook.com>` (owner
directive 8, LWP-R2). A GitHub-managed bot (Dependabot today; more may be
added by GitHub itself later) commits under its own `<name>[bot]` account
and a `@users.noreply.github.com` email -- that is GitHub's own identity,
not a human's, and is explicitly allowed here. Any OTHER author name/email
is flagged: it is either a real, non-LEAPWare human identity (which does
not belong in this repo's history from LWP-D0 forward) or a bot this list
has not reviewed yet.

Two modes:

  --base B --head H    Range mode. Every commit in `base..head` must be
                        LEAPWare or an allow-listed bot. No legacy
                        exemption -- a PR range is assumed to sit entirely
                        after the legacy boundary.

  (no --base)           Full-history mode. Walks commits reachable from
                        `--head` (default HEAD), bounded to the last 500.
                        Commits at or before LEGACY_BOUNDARY_SHA (that
                        commit and all of its ancestors) are reported as
                        "legacy" and never fail the check -- this repo's
                        history before LWP-D0 used other author identities
                        (LEAPWare-HQ, individual contributor identities,
                        the D0 merge-base commit's own GitHub-attributed
                        identity) and owner directive 8 does not rewrite
                        history to fix that. Commits AFTER the boundary
                        must satisfy the same identity rule as range mode.

LEGACY_BOUNDARY_SHA is a named constant, not a magic literal buried in
logic: it is the LWP-D0 merge base (`git merge-base main HEAD` at the
point the D0 branch was cut -- see docs/requirements/plan.md, "Commit
identity: from this phase on..."). It can be overridden with
`--legacy-boundary <sha>` for testing or if the owner ever needs to move
it (e.g. a later phase cuts a new boundary); the default is this repo's
real one so a plain `--head` run against the real repo needs no flag.

Usage:
    python scripts/lwp_check_commit_identity.py --base <ref> --head <ref>
    python scripts/lwp_check_commit_identity.py [--head <ref>] [--legacy-boundary <sha>]

Stdlib only. Exits 0 and prints "lwp-commit-identity check passed" on
success; otherwise prints every offending author and exits 1. Never
rewrites history.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ALLOWED_HUMAN = ("LEAPWare", "leapware@outlook.com")

# A GitHub bot commits as "<name>[bot] <NNNNNNN+name[bot]@users.noreply.github.com>"
# (Dependabot's own shape) or the plainer "<name>[bot] <name@users.noreply.github.com>"
# some other GitHub bots use.
BOT_NAME = re.compile(r"^[\w.\-]+\[bot\]$")
BOT_EMAIL = re.compile(r"^(?:\d+\+)?[\w.\-]+\[bot\]@users\.noreply\.github\.com$")

# The LWP-D0 merge base: `git merge-base main HEAD`, recorded once the D0
# branch was cut. Every commit at or before this one (inclusive) predates
# owner directive 8's commit-identity rule and is reported as legacy, not
# a failure. See the module docstring for how this is set and why it is a
# named constant rather than a literal inline below.
LEGACY_BOUNDARY_SHA = "8bccb1c7c1be6bbbb652c5e88ee7a0138c78479a"

_REV_LIST_LIMIT = 500


def _git(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd or REPO_ROOT,
        capture_output=True,
        text=True,
        # Explicit: text=True alone decodes with the locale default, which is
        # cp1252 on a Windows runner and raises UnicodeDecodeError on any
        # non-ASCII byte in a diff, filename or commit message.
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    return result.stdout


def _authors(rev_range: str, cwd: Path | None = None) -> list[tuple[str, str]]:
    stdout = _git(["log", "--format=%an\t%ae", rev_range], cwd=cwd)
    seen: list[tuple[str, str]] = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        name, _, email = line.partition("\t")
        pair = (name, email)
        if pair not in seen:
            seen.append(pair)
    return seen


def _author_for_sha(sha: str, cwd: Path | None = None) -> tuple[str, str]:
    stdout = _git(["log", "-1", "--format=%an\t%ae", sha], cwd=cwd)
    name, _, email = stdout.strip().partition("\t")
    return name, email


def _rev_list(rev: str, limit: int = _REV_LIST_LIMIT, cwd: Path | None = None) -> list[str]:
    stdout = _git(["rev-list", f"--max-count={limit}", rev], cwd=cwd)
    return [line for line in stdout.splitlines() if line.strip()]


def _is_allowed(name: str, email: str) -> bool:
    if (name, email) == ALLOWED_HUMAN:
        return True
    if BOT_NAME.match(name) and BOT_EMAIL.match(email):
        return True
    return False


def check(rev_range: str, cwd: Path | None = None) -> list[str]:
    """Range mode: every commit in `rev_range` must be allowed. No legacy exemption."""
    findings = []
    for name, email in _authors(rev_range, cwd=cwd):
        if not _is_allowed(name, email):
            findings.append(f"{name} <{email}>")
    return findings


def check_full_history(
    head: str = "HEAD",
    legacy_boundary: str = LEGACY_BOUNDARY_SHA,
    limit: int = _REV_LIST_LIMIT,
    cwd: Path | None = None,
) -> tuple[list[str], int]:
    """Full-history mode. Returns (findings, legacy_commit_count).

    A commit at or before `legacy_boundary` (i.e. `legacy_boundary` itself
    or one of its ancestors) is legacy and never produces a finding, even
    if its author identity would otherwise fail. Every other commit
    reachable from `head` must pass `_is_allowed`.
    """
    head_commits = _rev_list(head, limit=limit, cwd=cwd)
    try:
        legacy_set = set(_rev_list(legacy_boundary, limit=limit, cwd=cwd))
    except subprocess.CalledProcessError:
        # legacy_boundary not reachable/known in this repo (e.g. a fixture
        # repo in a test with no such commit) -- nothing is legacy.
        legacy_set = set()

    findings: list[str] = []
    legacy_count = 0
    for sha in head_commits:
        if sha in legacy_set:
            legacy_count += 1
            continue
        name, email = _author_for_sha(sha, cwd=cwd)
        if not _is_allowed(name, email):
            findings.append(f"{sha[:12]} {name} <{email}>")
    return findings, legacy_count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=None, help="base ref, e.g. origin/main")
    parser.add_argument("--head", default="HEAD", help="head ref (default HEAD)")
    parser.add_argument(
        "--legacy-boundary",
        default=LEGACY_BOUNDARY_SHA,
        help="full-history mode only: sha at/before which commits are legacy",
    )
    args = parser.parse_args()

    if args.base:
        findings = check(f"{args.base}..{args.head}")
        legacy_count = None
    else:
        findings, legacy_count = check_full_history(args.head, args.legacy_boundary)

    if findings:
        for f in findings:
            print(f"FAIL: commit author not LEAPWare or an allow-listed bot: {f}")
        return 1
    if legacy_count:
        print(f"lwp-commit-identity check passed ({legacy_count} legacy commit(s) at/before boundary)")
    else:
        print("lwp-commit-identity check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
