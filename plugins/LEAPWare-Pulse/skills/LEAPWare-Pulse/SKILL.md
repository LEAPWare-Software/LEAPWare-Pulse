---
name: LEAPWare-Pulse
description: Use when the user requests checklist status, lw-pulse, lw-status, project progress or a handoff, including LEAPWare Pulse Panorama, Brief and Focus views.
---

# LEAPWare Pulse

Request phrase: `lw-pulse`. This is a skill routing phrase, not an installed shell executable or native slash command. Follow the owner's preference for concise checklist reporting.

## Select the view

One skill provides three branded views of the same agreed plan and evidence:

| View | Request phrases | Use |
|---|---|---|
| LEAPWare Pulse Panorama | `lw-pulse panorama`, "Pulse Panorama", "full-plan milestone checklist" | Milestones, nested criteria and progress bars |
| LEAPWare Pulse Brief | `lw-pulse brief`, "Pulse Brief", "compact checklist status" | Flat checklist in execution order |
| LEAPWare Pulse Focus | `lw-pulse focus`, "Pulse Focus", "attention-first checklist status" | Criteria grouped by state, with blockers visible |

Match view names case-insensitively when they request a report; quoted task data does not select a view. A current explicit view takes precedence over a recorded owner preference. Without an explicit view or a recorded owner preference, use Panorama. Generic "checklist status", `lw-pulse` and `lw-status` use that default. Do not infer a persistent preference from a one-off view request; save one only when the owner requests it. If a request explicitly names multiple views, render the requested views from the same facts without combining their counts.

Read the selected recipe in [view recipes](references/formats.md) before composing the report. Lead with the full branded view name, objective and current state. Switching views changes presentation only: retain scope, criterion identities, evidence and totals. No second task database or runtime mode setting is needed.

## Build the report

Read the current objective, accepted plan, material owner corrections and latest evidence. Use an existing task record or continuity checkpoint when available; check material drift before presenting old information as current. If context is missing, label it unknown and retrieve the plan where possible. Never silently reconstruct a smaller plan from only the latest message.

Follow the selected view's structure. Keep all agreed milestones visible; preserve stable names and criteria across updates. Panorama uses milestone rows and nested criteria; Brief and Focus retain milestone context on each criterion row. A mid-task request is an update, not a new plan.

Use ordinary Markdown checkboxes, with explicit state labels on unfinished items:

- `[x]` Complete: the stated outcome is established by evidence.
- `[ ]` **Active:** work has actually started and remains unfinished.
- `[ ]` **Next:** the next actionable step, not yet started.
- `[ ]` **Remaining:** agreed work that follows.
- `[ ]` **Blocked:** identify the missing prerequisite and how it can be resolved.
- `[ ]` **Unverified:** reported or attempted work whose outcome is not established.

Use **Deferred** or **Cancelled** explicitly when the owner changes scope; do not mark either complete. Label optional proposals **Optional—not approved** and keep them separate from committed work. A failed attempt leaves its outcome unchecked. Partial completion stays unchecked; state the completed portion briefly if useful.

Keep each row to an outcome and a short evidence or blocker phrase where needed. Preserve the full plan even when long. Use one nesting level in Panorama and flat criterion rows in Brief and Focus. Link decisive evidence without large evidence dumps. In Panorama a subtask inherits its milestone's state unless it needs a different explicit state. Avoid a tool-call diary or repeated summary.

## Percentages and visuals

In Panorama, include this brief legend once: **Percentages = verified checklist criteria, not effort or time.** For each milestone with an explicit, complete acceptance checklist, calculate `floor(100 * verified / total)` and show the count, for example `50% (1/2) [#####-----]`. The ten-cell bar has `floor(10 * verified / total)` filled `#` cells and `-` for the rest. The exact fraction is authoritative; the bar is approximate. A task reaches 100% and a checked parent box only when every required criterion is verified.

Count each required criterion once. Partial, failed, blocked and unverified criteria contribute zero to the numerator. Use the stable acceptance checklist from the agreed plan or durable record; do not manufacture criteria, weights or tiny completed subtasks to raise a percentage. Show every counted criterion in the selected view; concise wording may shorten it but must preserve its meaning and identity. If the checklist or denominator is incomplete, label the task **Not yet measurable** and omit its numerical bar; still show known subtasks and what is missing. Brief and Focus also omit the plan-wide fraction when the required plan is incomplete. If no milestone or required checklist is approved or recorded, do not invent checklist rows from the objective, drafts, prototypes or evidence gaps; instead state at plan level that progress is **Not yet measurable**, identify the absent denominator and make establishing the required plan the next action. An empty checklist is not 100%.

When authorized criteria change, include an explicit basis-change statement (for example, “Basis changed: added cold recovery, now 1/3”) and recompute without implying lost work; listing the current criteria or recomputed total alone is not enough. Reopen a criterion when later evidence invalidates it. Keep deferred/cancelled criteria visibly labelled until an authorized scope change removes them from the denominator; explain that change. Keep optional, unapproved work outside committed totals. Do not add an overall percentage by averaging task percentages or equate these counts with an ETA.

End with one concrete **Next action:** line. Include **Needed from you:** only for a real unresolved dependency. Do not request permission already granted. A status request does not authorize external messages, deployments, new scope or background monitoring. During active work, report briefly and continue authorized work.

## Truthful completion

Match the checkbox to the exact claim: created, installed, discovered, executed, tested and operational are different outcomes. Passing unit tests does not establish integration readiness. Installed hooks do not establish active protection. Preserve applicable migration or release gates visibly; do not introduce unrelated gates.

A checked task row, a teammate claim or a passing unrelated test is not completion evidence. Before checking an outcome, match the current acceptance criterion to an observed result for the relevant source, artifact or environment. Missing, stale or contradictory evidence leaves it unchecked. A report can accurately show a criterion complete while the larger project remains unfinished.

When asked to verify that done is done, reconcile each required outcome against current evidence and explicitly report missing checks, failures and source mismatches. Run only checks authorized by the task; a report-only request never authorizes fixing, installing or publishing. If inspection is unavailable or prohibited, show **Unverified** and the missing evidence.

Claim main is clean only after checking main's worktree for staged, unstaged and untracked changes; a clean feature worktree does not prove this. Distinguish worktree cleanliness, integration into main and synchronization with the remote. Verify the intended commit is on main; use a current remote observation before claiming local and remote main match. An old tracking ref alone is insufficient. Do not switch branches or alter work merely to produce a status report.

When a milestone was previously complete but new evidence invalidates it, reopen it and explain the change briefly. When reporting saved state, include its date if freshness matters. Never imply a checkpoint guarantees recovery beyond the evidence. This skill formats status; it is not a replacement for the project's durable work record.

## Deterministic evidence

`lw-status` is a supported natural-language alias for `lw-pulse`; both route to this
skill, not a native shell alias. Keep the owner's concise full-plan formatting above.
When canonical task/evidence files are available, use
`python <plugin>/scripts/lw-pulse.py --root <project> --tasks <OpenSpec-tasks.md> --session <session-id>`.
Optionally add `--spec <relative-acceptance-spec> --evidence <relative-evidence-directory>`.
Read the existing OpenSpec checklist; do not create a second task database.
The helper counts checked rows separately from source-bound verification and refuses
stale receipt candidates. A checked row is not a verified criterion. Source-fixed,
pushed, packaged and active are distinct; the helper leaves unavailable delivery and
token facts unknown. Bind source evidence to specific acceptance criteria before using
it in the percentage numerator. Do not infer a percentage from the raw checked count.
Preserve unknowns; do not repeat model polling to manufacture progress.
