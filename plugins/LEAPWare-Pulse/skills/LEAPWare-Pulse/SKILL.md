---
name: LEAPWare-Pulse
description: Report project status as a full-plan checklist with subtasks, evidence-based completion percentages and compact progress bars. Use for lw-pulse, status requests, progress updates and project handoffs.
---

# LEAPWare Pulse

Request phrase: `lw-pulse`. This is a skill routing phrase, not an installed shell executable or native slash command. Follow the owner's preference for concise checklist reporting.

## Build the report

Read the current objective, accepted plan, material owner corrections and latest evidence. Use an existing task record or continuity checkpoint when available; check material drift before presenting old information as current. If context is missing, label it unknown and retrieve the plan where possible. Never silently reconstruct a smaller plan from only the latest message.

Lead with one short line naming the objective and overall state, followed by a single full-plan checklist in execution order. Each milestone row contains its name, state, percentage, verified/total criterion count and compact progress bar. Nest concise checkbox subtasks beneath each milestone to show its acceptance criteria, including completed and outstanding work. Keep all agreed milestones visible; preserve stable names and criteria across updates. A mid-task request is an update, not a new plan.

Use ordinary Markdown checkboxes, with explicit state labels on unfinished items:

- `[x]` Complete: the stated outcome is established by evidence.
- `[ ]` **Active:** work has actually started and remains unfinished.
- `[ ]` **Next:** the next actionable step, not yet started.
- `[ ]` **Remaining:** agreed work that follows.
- `[ ]` **Blocked:** identify the missing prerequisite and how it can be resolved.
- `[ ]` **Unverified:** reported or attempted work whose outcome is not established.

Use **Deferred** or **Cancelled** explicitly when the owner changes scope; do not mark either complete. Label optional proposals **Optional—not approved** and keep them separate from committed work. A failed attempt leaves its outcome unchecked. Partial completion stays unchecked; state the completed portion briefly if useful.

Keep each row to an outcome and, when needed, one short evidence or blocker phrase. Prefer 5–10 milestones with short subtasks; preserve the full plan when it needs more. Use one nesting level, blank lines between milestone groups and decisive evidence links without large evidence dumps. A subtask inherits its milestone's state unless it needs a different explicit state. Avoid a tool-call diary or repeated summary.

## Percentages and visuals

Include this brief legend once: **Percentages = verified checklist criteria, not effort or time.** For each task with an explicit, complete acceptance checklist, calculate `floor(100 * verified / total)` and show the count, for example `50% (1/2) [#####-----]`. The ten-cell bar has `floor(10 * verified / total)` filled `#` cells and `-` for the rest. The exact fraction is authoritative; the bar is approximate. A task reaches 100% and a checked parent box only when every required criterion is verified.

Count each required criterion once. Partial, failed, blocked and unverified criteria contribute zero to the numerator. Use the stable acceptance checklist from the agreed plan or durable record; do not manufacture criteria, weights or tiny completed subtasks to raise a percentage. Show the counted criteria as subtasks; concise wording may shorten them but must preserve their meaning and count. If the checklist or denominator is incomplete, label the task **Not yet measurable** and omit its numerical bar; still show known subtasks and what is missing. If no milestone or required checklist is approved or recorded, do not invent checklist rows from the objective, drafts, prototypes or evidence gaps; instead state at plan level that progress is **Not yet measurable**, identify the absent denominator and make establishing the required plan the next action. An empty checklist is not 100%.

When authorized criteria change, include an explicit basis-change statement (for example, “Basis changed: added cold recovery, now 1/3”) and recompute without implying lost work; listing the current criteria or recomputed total alone is not enough. Reopen a criterion when later evidence invalidates it. Keep deferred/cancelled criteria visibly labelled until an authorized scope change removes them from the denominator; explain that change. Keep optional, unapproved work outside committed totals. Do not add an overall percentage by averaging task percentages or equate these counts with an ETA.

End with one concrete **Next action:** line. Include **Needed from you:** only for a real unresolved dependency. Do not request permission already granted. A status request does not authorize external messages, deployments, new scope or background monitoring. During active work, report briefly and continue authorized work.

## Truthful completion

Match the checkbox to the exact claim: created, installed, discovered, executed, tested and operational are different outcomes. Passing unit tests does not establish integration readiness. Installed hooks do not establish active protection. Preserve applicable migration or release gates visibly; do not introduce unrelated gates.

When a milestone was previously complete but new evidence invalidates it, reopen it and explain the change briefly. When reporting saved state, include its date if freshness matters. Never imply a checkpoint guarantees recovery beyond the evidence. This skill formats status; it is not a replacement for the project's durable work record.

## Example shape

Illustrative plan with explicit criteria; use the current task's actual plan and evidence in reports.

**Objective:** Prove recovery before migration. **Status:** Validation active.

**Percentages = verified checklist criteria, not effort or time.**

- [x] **Install repairs — Complete · 100% (2/2)** `[##########]`
  - [x] Verify installed source matches reviewed repairs.
  - [x] Publish the repaired source.

- [ ] **Validate recovery — Active · 33% (1/3)** `[###-------]`
  - [x] Pass the defined unit checks.
  - [ ] **Next:** Verify native hook execution.
  - [ ] Verify cold recovery.

- [ ] **Migrate project — Blocked · 0% (0/2)** `[----------]`
  - [ ] Establish required continuity proof.
  - [ ] Complete project enrollment and migration.

- [ ] **Extend runtime support — Remaining · Not yet measurable**
  - [ ] Define the required runtime acceptance checklist.

**Next action:** Run the native hook check and record its evidence.
