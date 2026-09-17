## Summary

<!-- What changed and why. -->

## Checklist

- [ ] `python -m pytest -q` passes
- [ ] `python scripts/lwp_check_prefix.py` passes
- [ ] `python scripts/lwp_check_no_instruction_dep.py` passes
- [ ] `python scripts/lwp_check_proof.py` passes
- [ ] `python scripts/lwp_check_worktrees.py` passes — no worktree or clone
      created as a sibling folder next to the repo; every linked worktree
      is under `<repo>/.worktrees/<branch>`
- [ ] `python scripts/lwp_check_runners.py` passes
- [ ] `python scripts/lwp_check_trace.py` passes
- [ ] `python scripts/lwp_handoff.py --check` passes
- [ ] No third-party runtime import added under `core/` or `adapters/`
- [ ] If a shared path changed (`core/`, `adapters/`, `scripts/`,
      `.github/`, `docs/`, `proof/`, `reviews/`): review records from both
      CLIs are under `reviews/<pr>/`
