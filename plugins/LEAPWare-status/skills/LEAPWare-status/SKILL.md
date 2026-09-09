---
name: LEAPWare-status
description: Report project status and progress as a concise checklist of the full agreed plan, completed work and remaining steps. Use for lw-status, status requests, progress updates and project handoffs.
---

# LEAPWare status

Request phrase: `lw-status`. This is a skill routing phrase, not an installed shell executable or native slash command. Follow the owner's preference for concise checklist reporting.

## Build the report

Read the current objective, accepted plan, material owner corrections and latest evidence. Use an existing task record or continuity checkpoint when available; check material drift before presenting old information as current. If context is missing, label it unknown and retrieve the plan where possible. Never silently reconstruct a smaller plan from only the latest message.

Lead with one short line naming the objective and overall state. Show the complete agreed plan in execution order, with one line per milestone. Keep completed milestones visible alongside remaining ones. Group small tasks beneath a meaningful milestone to stay concise; do not hide unresolved acceptance criteria, branches of work or blockers in a completed group. Preserve stable milestone names across updates. A mid-task request is an update, not a new plan.

Use ordinary Markdown checkboxes, with explicit state labels on unfinished items:

- `[x]` Complete: the stated outcome is established by evidence.
- `[ ]` **In progress:** work has actually started and remains unfinished.
- `[ ]` **Next:** the next actionable step, not yet started.
- `[ ]` **Remaining:** agreed work that follows.
- `[ ]` **Blocked:** identify the missing prerequisite and how it can be resolved.
- `[ ]` **Unverified:** reported or attempted work whose outcome is not established.

Use **Deferred** or **Cancelled** explicitly when the owner changes scope; do not mark either complete. Label optional proposals **Optional—not approved** and keep them separate from committed work. A failed attempt leaves its outcome unchecked. Partial completion stays unchecked; state the completed portion briefly if useful.

Keep each row to an outcome and, when needed, one short evidence or blocker phrase. Prefer roughly 5–10 milestone rows and 100–200 words, but preserve the complete plan when it needs more. Avoid a tool-call diary, repeated summaries and large evidence dumps. Link decisive evidence once. Do not invent percentages or ETAs; a milestone count, if requested, is a count rather than a measure of effort.

End with one concrete **Next action:** line. Include **Needed from you:** only for a real unresolved dependency. Do not request permission already granted. A status request does not authorize external messages, deployments, new scope or background monitoring. During active work, report briefly and continue authorized work.

## Truthful completion

Match the checkbox to the exact claim: created, installed, discovered, executed, tested and operational are different outcomes. Passing unit tests does not establish integration readiness. Installed hooks do not establish active protection. Preserve applicable migration or release gates visibly; do not introduce unrelated gates.

When a milestone was previously complete but new evidence invalidates it, reopen it and explain the change briefly. When reporting saved state, include its date if freshness matters. Never imply a checkpoint guarantees recovery beyond the evidence. This skill formats status; it is not a replacement for the project's durable work record.

## Example shape

**Objective:** Ship the agreed change. **Status:** Validation in progress.

- [x] Define scope and acceptance criteria.
- [x] Implement the change.
- [ ] **In progress:** Run integration checks; unit checks passed.
- [ ] **Remaining:** Resolve findings and obtain required review.
- [ ] **Blocked:** Release; integration evidence is incomplete.

**Next action:** Run the pending integration scenario and record its result.
