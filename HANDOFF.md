# HANDOFF

Read this before any other file. Protocol: `docs/handoff-protocol.md`.

## Start of session

- [ ] Read this file, run "Re-derive state", trust its output over prose.
- [ ] Confirm your CLI lane (`AGENTS.md` / `CLAUDE.md`, LWP-R8).
- [ ] Nothing in flight? Enter plan mode, take the next unchecked step.

## In flight

Plan of record: `docs/requirements/plan.md` (D0-D5, gate G-PUB), proven
against `docs/requirements/requirements.md` (LWP-R1-R39) and traced in
`docs/requirements/traceability.md`. Never start phase *n+1* before phase
*n* is merged with a proof record checked by a different identity.

1. D0 is MERGED (PR #2, squashed as `8071687`): root meta, `.github/`,
   the `lwp_check_*` suite, `proof/` and `reviews/` schemas, the
   traceability matrix. CI green on all six jobs. Proof record
   `proof/LWP-D0.json`, checked by an identity that did not author it.
2. NEXT, and owner-only: gate G-PUB. Flip visibility to public, apply
   `.github/rulesets/main.json` with `scripts/lwp_apply_rulesets.py`,
   enable merge queue and auto-merge, create the `lwp-claude` and
   `lwp-codex` Apps from `.github/apps/`. G-PUB blocks D1 and every later
   merge. The ruleset has never been applied: `gh api .../rulesets`
   returns 403 while the repo is private.
3. Pre-publication history scan passed: `proof/LWP-GPUB-scan.json`.
4. Then D1 core extraction, D2 Codex plugin, D3 migration, D4 Claude
   port, D5 rehearsal and release 1.0.0. D1 may be worked on a branch
   before G-PUB, but not merged.

## Re-derive state

```
git fetch origin && git status --short --branch
git log --oneline -10 && git worktree list
gh pr list --state open --json number,title
gh run list --limit 10
gh repo view LEAPWare-Software/LEAPWare-Pulse --json visibility
```

<!-- lwp-handoff:begin -->

Generated: 2026-09-17 23:39 UTC
main SHA: 8071687f07e38bbb98e07029f15b7c0aae3c354c
CLI: claude
Session: d0-skeleton-parity

Open PRs:
(unavailable: no `gh` auth in this environment, or no open PRs)

Deliverable proof state (from proof/):
- LWP-D0: PROVEN (commit 78eba219e21e8f57c66b31378fbe9df37364070f)
- G-PUB: PROVEN (gate record, verdict 'publishable')

<!-- lwp-handoff:end -->

## Hard rules

Full list in `CLAUDE.md` / `AGENTS.md`. Standard library only in shipped
code; the plugin never reads `CLAUDE.md` or `AGENTS.md` at runtime;
commit identity `LEAPWare <leapware@outlook.com>`; worktrees only under
`.worktrees/`; GitHub-hosted runners only; no force-push, no history
rewrite, no visibility change without the owner.

## Traps

Listed in `docs/handoff-protocol.md`, "Traps". The one that bites first:
`lwp_check_env_leak.py --range` still scans the full tree, which cannot
pass until D2 drops `docs/evidence/*` -- CI passes `--range-only`.
