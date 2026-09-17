# HANDOFF

One page. Read this before any other file when starting a new session on
this repo. The full handoff protocol (`docs/handoff-protocol.md`) lands in
D0; until then this file follows the sibling repos' protocol by hand.

## Start of session

- [ ] Read this whole file.
- [ ] Run the commands in "Re-derive state" below — trust their output,
      not this file's prose (except the "In flight" narrative, which is
      the current plan of record).
- [ ] Confirm which CLI you are (Claude Code or Codex). Lanes start in D0
      (`AGENTS.md` / `CLAUDE.md`); until then touch only the phase's files.
- [ ] If nothing below is in flight, ENTER PLAN MODE and pick up the next
      unchecked step.

## In flight

The plan of record is `docs/requirements/plan.md` (phases D0–D5 and gate
G-PUB), proven against `docs/requirements/requirements.md` (LWP-R1…R39)
and traced to `docs/requirements/owner-directives.md`. Do not start phase
*n+1* before phase *n* is merged and its proof record is checked.

1. Work from this repo only. Clone fresh on any machine; no dependence on
   the local environment.
2. The recast requirements and plan are merged. Decisions Q1, Q3–Q5 are
   recorded in `plan.md` (CTO, 2026-09-17). Q2 (learning subsystem
   publication) is OPEN, OWNER-RESERVED: it gates G-PUB, not D0; D0 may
   proceed while the repo is private.
3. Pre-publication history scan runs separately. Gate G-PUB (owner: flip to
   public, apply rulesets and merge queue, create the `lwp-claude` and
   `lwp-codex` Apps) must pass before D1 or later merges.
4. D0 — skeleton parity and governance, including the worktree rule
   (LWP-R9) and hosted-runners-only check (LWP-R39).
5. D1 core extraction, D2 Codex plugin, D3 Codex migration, D4 Claude port,
   D5 rehearsal and independent proof, release 1.0.0.
6. Every phase: proof record `proof/LWP-Dn.json`, pushed, CI green, alert
   line `LWP - Alert: LWP-Dn DONE ...`.

<!-- lwp-handoff:begin -->

Generated: by hand (no generator yet; `scripts/lwp_handoff.py` lands in D0)
Branch of record: main
Open PRs: read `gh pr list`, not this line.

Deliverable proof state (from proof/):
(none yet; `proof/` lands in D0)

<!-- lwp-handoff:end -->

## Re-derive state

```
git fetch origin
git status --short --branch
git log --oneline -10
git worktree list
gh pr list --state open
gh run list --limit 10
gh repo view LEAPWare-Software/LEAPWare-Pulse --json visibility
gh api repos/LEAPWare-Software/LEAPWare-Pulse/rulesets
```

`gh` and `git` are the state of record. This file's "In flight" list is
the plan; the commands above are the facts.

## Hard rules

- Python 3.10+ standard library only in anything shipped.
- The plugin never reads or depends on `CLAUDE.md` or `AGENTS.md` at
  runtime.
- Commit identity `LEAPWare <leapware@outlook.com>` from now on. Existing
  history is never rewritten.
- Worktrees only under `<repo>/.worktrees/<branch>` (gitignored). Never a
  worktree or clone as a sibling folder next to the repo.
- CI on GitHub-hosted runners only (`ubuntu-*`, `windows-*`, `macos-*`).
- Nothing copied from any private project into this repo.
- No visibility or settings change, no force-push, no history rewrite
  without the owner.

## Traps

- `gh pr list --jq` without `--json` exits 1; use `--json` with `--jq`.
- A linked worktree's `.git` is a file, not a directory.
- `git diff` omits untracked files; check
  `git ls-files --others --exclude-standard` too.
- The existing `docs/evidence/*` files contain absolute local paths; they
  are dropped from the tree in D2 and will fail the D0 env-leak check on a
  full-tree scan until then — run that check in range mode for D0/D1 PRs.
- The learning data key stays `leapware-pulse` through the rename
  (LWP-R27); changing it orphans existing registries.
