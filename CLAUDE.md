# LEAPWare-Pulse (lwp) — contributor instructions for Claude Code

These are instructions for building this repo, not runtime config. The
lwp plugin itself must never read or depend on this file at runtime.

- Read HANDOFF.md first, every session.
- The repo has been PUBLIC since 2026-09-18; gate G-PUB is otherwise
  still partially open — see HANDOFF.md.
- Learning is dropped from 1.0, so don't reintroduce it.
- Worktrees live only under .worktrees/<branch>, never as sibling folders.
- CI uses GitHub-hosted runners only.
- Commit identity is LEAPWare <leapware@outlook.com>.
- Nothing from private projects enters this repo.
- No force-push.

## CLI lanes (LWP-R8)

- Your lane: `plugins/claude/`, `adapters/claude/`, `tests/**/claude/`.
  Codex's lane (`plugins/codex/`, `adapters/codex/`, `tests/**/codex/`) is
  not yours to edit.
- Shared paths (`core/`, `adapters/common/`, `scripts/`, `.github/`,
  `docs/`, `proof/`, `reviews/`) change only with review records from
  both CLIs under `reviews/<pr>/`.
