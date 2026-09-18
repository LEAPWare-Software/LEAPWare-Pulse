# Handoff protocol

`HANDOFF.md`, at the repo root, is the single re-derivable state file a
new session reads first. This document is the protocol that keeps it
true. It has no runtime role — the lwp plugin never reads it.

## When to write a handoff

Write (or update) `HANDOFF.md` at each of these points:

1. Before ending any session, whatever the reason.
2. At any rate-limit or context warning from the host CLI.
3. After each deliverable lands (its own Proof of Completion, see below,
   plus an updated "next step" in the "In flight" section).

A handoff is cheap and mechanical (`scripts/lwp_handoff.py --write`); the
cost of skipping one is a session that starts from guesswork instead of
fact.

## What the generated block contains

Between `<!-- lwp-handoff:begin -->` and `<!-- lwp-handoff:end -->` in
`HANDOFF.md`, `scripts/lwp_handoff.py --write` regenerates:

- UTC timestamp of generation.
- CLI name and session id (when the caller supplies them; omitted rather
  than guessed otherwise).
- `main`'s current SHA.
- Open PRs with their CI state.
- Deliverables in flight with their proof state.
- The next step to take.

## Only the block is regenerated

Everything in `HANDOFF.md` outside the begin/end markers — the "In
flight" narrative, "Hard rules", "Traps", the checklist — is prose a
session wrote by hand. `--write` never touches it. If the narrative plan
changes (a step finishes, a new one starts), edit that prose by hand in
the same commit that regenerates the block.

## Size cap

LWP-R11 sets `HANDOFF.md`'s enforced cap at **6000 bytes**:
`scripts/lwp_handoff.py --check` fails the build over it, and this is not
a soft target within that check.

The operative cap for this file is tighter than that, though. The
repository owner's global cross-project instructions cap every project's
`HANDOFF.md` at **3000 bytes**, and an owner ruling governs regardless of
what any one repo's own requirement says. Where the two disagree, the
owner's 3000-byte cap is the one to write to; `scripts/lwp_handoff.py
--check` enforcing 6000 is a backstop, not the target. A one-page handoff
that nobody reads in full is worse than no handoff; trim prose before
growing toward either cap.

## Done means committed and pushed

A handoff is DONE only when it is committed to the branch and pushed to
`origin`. A regenerated `HANDOFF.md` sitting only in a working tree is not
a handoff — the next session (possibly on a different machine) cannot see
it.

## The next session re-derives state, never trusts prose

Every session, CLI, or machine starts by running the commands in
`HANDOFF.md`'s "Re-derive state" section — `git`, `gh` — and treats their
output as fact. The "In flight" narrative is the *plan*; the command
output is the *state*. Where they disagree, the commands win, and the
narrative gets corrected in the same session.

## Proof of Completion

A deliverable is DONE only when: committed, pushed, CI is green on that
push, and a proof record exists (what changed, why, how it was verified —
commit message and/or PR description is sufficient; no separate proof
file is required). Every proven delivery is announced with a line
starting `LWP - Alert: <id> DONE ...` so it is grep-able across a long
session.

## Traps

Kept here, not in `HANDOFF.md`: the handoff is a transition, not an
archive, and it is capped at 3000 bytes (see "Size cap" above).

- `gh pr list --jq` without `--json` exits 1; use `--json` with `--jq`.
- A linked worktree's `.git` is a file, not a directory.
- `git diff` omits untracked files; check
  `git ls-files --others --exclude-standard` too.
- `scripts/lwp_check_env_leak.py --range A..B` *adds* a range scan to the
  full-tree scan; it does not replace it. `docs/evidence/*` (which carried
  absolute local paths on purpose) is gone from the tree, brought forward
  from D2 ahead of publication, so the full-tree scan now gates CI without
  `--range-only`. `tests/test_ci_env_leak_mode.py` is self-retiring: it
  required `--range-only` while `docs/evidence/` existed, and now requires
  its absence, so the full-tree scan cannot stay disabled by accident.
- `scripts/lwp_check_prefix.py` exits 1 on the pre-recast tree: the Codex
  package is still `plugins/LEAPWare-Pulse/` until D2/D4 renames it to
  `lwp`. Expected, and recorded as such in `proof/LWP-D0.json`.
- Lane enforcement (`scripts/lwp_lanes.py`) is a no-op for PRs 1-5; the PR
  that introduced the lane system could not satisfy it. PR 6 onward is
  enforced, and every commit needs an `LWP-Agent:` trailer.
