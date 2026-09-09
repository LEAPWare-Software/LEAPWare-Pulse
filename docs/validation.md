# Validation — 9 September 2026

- Plugin manifest validation passed.
- Codex CLI 0.153.4 installed version 0.1.0 and native skills/list discovered LEAPWare-status:LEAPWare-status without skill errors.
- Inspected package inventory: one skill, UI metadata and manifest; no hooks, MCP, executable commands or background agents.
- Generic skill lint rejects uppercase LEAPWare. The case is intentional under the owner's naming convention; native discovery accepts it. Do not describe this as a generic lint pass.
- Author manually checked the instructions against partial completion, failed attempts, missing context, scope changes, optional proposals and installed-but-unverified capabilities. These are author checks, not independent behavioral evaluation.

This simple reporting skill has no executable helper or test suite. Native discovery establishes availability, not guaranteed skill selection in every task. Verify selection in a fresh desktop task after installation.

## Approved checklist format revision

Source-only revision: one full-plan checklist, nested acceptance subtasks, per-task completion fractions/percentages and ten-cell text bars. Installation and publication of this revision remain pending.

Baseline: the existing skill/example supplied a flat checklist without the owner-requested subtasks, computed task percentages or progress bars. Bounded author format verification of the revised instructions covers:

- Two of two verified criteria: 100%, full bar and checked milestone.
- One of three verified criteria: 33%, three filled cells and unchecked active milestone; unit checks alone do not establish native/cold recovery.
- Ninety-nine of one hundred verified criteria: 99%, nine filled cells and unchecked milestone; rounding cannot claim completion.
- Missing or empty acceptance checklist: not yet measurable, no numerical bar; known subtasks remain visible.
- Added required criterion: recalculate from the new denominator and explain the basis change; optional work stays outside committed totals.
- Blocked/unverified criteria: remain unchecked and do not contribute to verified count; full plan and migration gate remain visible.

These are author application checks, not independent behavioral testing. `git diff --check` passed. The generic skill validator initially hit Windows default-encoding failure; rerunning with Python UTF-8 mode reached the known owner-required uppercase naming rejection. No generic lint pass or fresh native discovery is claimed for this source revision.
