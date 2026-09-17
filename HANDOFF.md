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

1. D0 (skeleton parity and governance) is in flight on
   `d0/skeleton-parity`: root meta, `.github/`, the `lwp_check_*` suite,
   `proof/` and `reviews/` schemas, traceability matrix.
2. G-PUB is owner-only and runs after D0 merges: flip to public, apply
   `.github/rulesets/main.json`, enable merge queue, create the
   `lwp-claude` and `lwp-codex` Apps. It blocks D1 and later merges.
3. Pre-publication history scan passed: `proof/LWP-GPUB-scan.json`.
4. Then D1 core extraction, D2 Codex plugin, D3 migration, D4 Claude
   port, D5 rehearsal and release 1.0.0.

## Re-derive state

```
git fetch origin && git status --short --branch
git log --oneline -10 && git worktree list
gh pr list --state open --json number,title
gh run list --limit 10
gh repo view LEAPWare-Software/LEAPWare-Pulse --json visibility
```

<!-- lwp-handoff:begin -->

Generated: 2026-09-17 22:36 UTC
main SHA: 8bccb1c7c1be6bbbb652c5e88ee7a0138c78479a
CLI: claude
Session: d0-skeleton-parity

Open PRs:
(unavailable: no `gh` auth in this environment, or no open PRs)

Deliverable proof state (from proof/):
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
