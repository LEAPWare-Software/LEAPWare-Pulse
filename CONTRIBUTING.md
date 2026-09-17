# Contributing to LEAPWare Pulse

## Runtime dependency policy — read this first

`core/` and `adapters/` are **Python 3.10+ standard library only**. A pull
request that adds a third-party runtime import to either directory, or to
any plugin's `bin/` script, will be closed without review. `pytest` is the
one dev-only exception, used solely under `tests/`.

## CLI lanes

Codex's lane is Codex-lane paths; Claude's lane is Claude-lane paths. A
shared path (`core/`, `adapters/`, `scripts/`, `.github/`, `docs/`,
`proof/`, `reviews/`) needs review records from both CLIs under
`reviews/<pr>/` before it lands. See `AGENTS.md` / `CLAUDE.md` for the
exact lane paths.

## Workflow

```
python -m pytest -q
python scripts/lwp_check_prefix.py
python scripts/lwp_check_no_instruction_dep.py
python scripts/lwp_check_proof.py
python scripts/lwp_check_worktrees.py
python scripts/lwp_check_runners.py
python scripts/lwp_check_trace.py
python scripts/lwp_handoff.py --check
```

All must pass before opening a pull request. CI (`.github/workflows/ci.yml`)
runs the same checks, plus range-scoped checks on pull requests, on a
Windows/macOS/Ubuntu x Python 3.10/3.12 matrix.

## Commit and PR conventions

- One logical change per commit; write the "why", not just the "what".
- Reference the issue a PR closes, if one exists.
- Commit identity is `LEAPWare <leapware@outlook.com>` from D0 forward.
- Worktrees only under `<repo>/.worktrees/<branch>`; never a sibling
  folder next to the repo.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
