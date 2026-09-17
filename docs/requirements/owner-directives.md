# Owner directives (recast session, 2026-09-17)

Binding. These are the owner's decisions for recasting LEAPWare-Pulse into
the structure its sibling plugin repos already use (LEAPWare-TokenWise,
code `lwt`; LEAPWare-SessionKeeper, code `lws`). Every requirement in
`requirements.md` traces back to one of these lines. A change to a line is
a new owner decision, recorded here by PR, never an edit of meaning.

1. Code name `lwp` (collision-checked). The repository keeps the name
   `LEAPWare-Pulse` in org `LEAPWare-Software`.
2. Same structure as `lwt` and `lws`: root meta files, `.github/`
   (rulesets, workflows, apps, templates), `adapters/{claude,codex}`,
   `core/lwp_core`, `plugins/{claude,codex}/lwp`, `proof/`, `reviews/`,
   `scripts/lwp_*`, `tests/{adapters,conformance,core,fixtures}`, and the
   handoff protocol with a root `HANDOFF.md`.
3. Public repository, with the same rulesets and merge queue as `lwt` and
   `lws`. The visibility flip happens only after the separate
   pre-publication history scan; "public and rulesets applied" is a phase
   gate in `plan.md`, performed by the owner, not by a plan phase.
4. Full Claude port: LEAPWare Pulse Panorama, Brief and Focus work in
   Claude Code as well as Codex.
5. Proof bar, same as `lws`: a numbered testable requirements list; a test
   per rule, each proven by breaking it on purpose; a rehearsal; an
   independent proof record.
6. Works on Windows, macOS and Linux.
7. Nothing from private projects is copied into the public repository.
8. Commit identity going forward is `LEAPWare <leapware@outlook.com>`.
   Existing history is not rewritten.
9. Worktrees live only under `<repo>/.worktrees/<branch>`; `.worktrees/` is
   gitignored; no worktree or clone is ever created as a sibling folder next
   to the repository. The rule is written in `AGENTS.md` and `CLAUDE.md`.
10. As a public repository, Pulse uses only GitHub-hosted runners
    (`ubuntu-*`, `windows-*`, `macos-*`); never self-hosted or local
    runners. A CI check fails the build otherwise.
