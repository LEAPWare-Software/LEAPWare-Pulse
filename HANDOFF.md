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
2. NEXT, owner-only: finish gate G-PUB. Public, ruleset `23672521`
   applied/active (empty bypass_actors, six checks match CI), merge queue
   and auto-merge on — all verified from the API. Two things remain: (a)
   create the `lwp-claude`/`lwp-codex` Apps by hand, procedure in
   `docs/github-apps.md`; (b) run a probe PR through the merge queue —
   never done, so "merges work end to end" is UNPROVEN, not just
   unverified on paper. G-PUB blocks D1+ merges until both are done.
3. THEN: D1 core extraction, unblocked and mergeable now (may be branched
   before G-PUB finishes, per plan, just not merged before it).
4. After D1: D2 Codex plugin, D3 migration, D4 Claude port, D5 rehearsal
   and release 1.0.0.

## Re-derive state

```
git fetch origin && git status --short --branch
git log --oneline -10 && git worktree list
gh pr list --state open --json number,title
gh run list --limit 10
gh repo view LEAPWare-Software/LEAPWare-Pulse --json visibility
```

<!-- lwp-handoff:begin -->

Generated: 2026-09-18 18:02 UTC
main SHA: 5ba0947329fe83592c5472d034fccdff077a5740
CLI: claude
Session: handoff-next-session

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

Listed in `docs/handoff-protocol.md`, "Traps". `docs/evidence/*` is gone
(brought forward from D2 ahead of publication); the full-tree
`lwp_check_env_leak.py` scan now gates every push and PR, alongside the
range-mode scan on PRs.
