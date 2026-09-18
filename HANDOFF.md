# HANDOFF

Read this before any other file. Protocol: `docs/handoff-protocol.md`.
Longer detail that doesn't fit this cap: `docs/session-carryover.md`.

## Start of session

- [ ] Read this file, run "Re-derive state", trust its output over prose.
- [ ] Confirm your CLI lane (`AGENTS.md` / `CLAUDE.md`, LWP-R8).
- [ ] Read "Blocker" below before touching any shared path.

## Blocker — `lwp-lanes` blocks all shared-path merges

PR #6 BLOCKED by CI job `lwp-lanes`. From PR #6 on, any `claude`/`codex`
commit touching a shared path (`core/`, `scripts/`, `.github/`, `docs/`,
`proof/`, `reviews/`, `HANDOFF.md`, `AGENTS.md`, `CLAUDE.md`,
`README.md`) needs BOTH `reviews/<pr>/claude-cto.json` and
`reviews/<pr>/codex-cto.json`, `"verdict": "AGREE"`, distinct
`reviewer_id`/`commit_author_id` (`lwp_lanes.py::_review_ok`).
`LWP-Agent: human` skips this — for real owner commits only, never a
CLI self-declaring human. Blocks all shared-path work, D1 included, until
resolved. Needs a genuine independent Codex session to write
`reviews/6/codex-cto.json`; details/options: `docs/session-carryover.md`.

## In flight

Plan of record: `docs/requirements/plan.md` (D0-D5, gate G-PUB), proven
against `docs/requirements/requirements.md` (LWP-R1-R39) and traced in
`docs/requirements/traceability.md`.

1. D0 MERGED (PR #2, `8071687`). CI green, 6 jobs. `proof/LWP-D0.json`
   sealed — never edit to match later reality.
2. G-PUB PARTIALLY met. PUBLIC since 2026-09-18; ruleset `23672521`
   active, empty bypass_actors, 6 checks match CI, auto-merge on.
   Outstanding: (a) `lwp-claude`/`lwp-codex` Apps — `docs/github-apps.md`;
   (b) merge-queue probe — never run, UNPROVEN.
3. THEN: D1 core extraction. Mergeable now, but mostly shared-path
   (`core/`) — the blocker above applies.
4. After D1: D2 Codex plugin, D3 migration, D4 Claude port, D5 release.

## Re-derive state

```
git fetch origin && git status --short --branch
git log --oneline -10 && git worktree list
gh pr list --state open --json number,title
gh run list --limit 10
gh repo view LEAPWare-Software/LEAPWare-Pulse --json visibility
```

<!-- lwp-handoff:begin -->

Generated: 2026-09-18 18:36 UTC
main SHA: 5ba0947329fe83592c5472d034fccdff077a5740
CLI: claude
Session: handoff-carryover

Open PRs:
#6 docs(gpub): GitHub Apps procedure and partial gate record (docs/handoff-next-session)

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

`docs/handoff-protocol.md` "Traps"; D0 limitations in
`docs/session-carryover.md`.
