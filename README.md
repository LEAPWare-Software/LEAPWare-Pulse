# LEAPWare Pulse

Three branded checklist views of the full agreed plan: **LEAPWare Pulse Panorama**, **LEAPWare Pulse Brief** and **LEAPWare Pulse Focus**. All retain completed and outstanding work, evidence-based completion and one concrete next action.

Use `lw-pulse` in a task or select the LEAPWare-Pulse skill. The phrase is not a shell command. The skill also supports ordinary status requests, progress updates and handoffs through automatic skill selection.

This dedicated repository belongs to LEAPWare-Software. The Codex plugin contains one self-contained skill; it adds no hooks, MCP servers, scheduled jobs or background agents. Reporting does not change task authorization or replace a continuity record.

## Choose your view

| Brand | Request phrase | Report shape |
|---|---|---|
| LEAPWare Pulse Panorama | `lw-pulse panorama` | Full plan in milestone order, nested criteria and per-milestone progress bars |
| LEAPWare Pulse Brief | `lw-pulse brief` | Flat checklist in execution order, milestone labels and one verified count |
| LEAPWare Pulse Focus | `lw-pulse focus` | Active work and blockers first; all criteria grouped by state with milestone labels |

Natural requests such as "Pulse Brief", "compact checklist status" and "attention-first checklist status" select the matching view. Generic "checklist status", `lw-pulse` and `lw-status` use Panorama unless the owner has explicitly recorded another default. An explicit view overrides that default for the current request. One-off requests do not change the saved preference. These phrases select the skill; they are not shell commands or new native slash commands.

See [the three view recipes and examples](plugins/LEAPWare-Pulse/skills/LEAPWare-Pulse/references/formats.md). The views share the existing task/evidence record; switching views cannot change the underlying scope or progress.

## Install

Register this repository with `codex plugin marketplace add <repository-root>`, then run `codex plugin add LEAPWare-Pulse@LEAPWare-Pulse`. Check selection in a fresh task after installation.

## Reporting contract

Keep the entire committed plan, including completed work. Panorama and Brief preserve execution order; Focus groups criteria by state while preserving their identities and milestone context. Check a box only when its stated outcome has current, relevant evidence. Keep partial, blocked, failed or unverified work unchecked. Preserve owner corrections, material gates and the exact next action. Separate optional proposals from approved work.

Panorama shows nested acceptance criteria, verified fractions and ten-cell progress bars per milestone. Brief and Focus show each criterion once and one plan-wide verified/required count. Counts and percentages represent verified criteria, not effort or time. Unknown denominators are not yet measurable. Explain changes to the counting basis, and reserve completion for verified satisfaction of every required criterion.

"Done" requires evidence for the exact outcome and relevant source/environment. A checked task, unsupported claim or unrelated test pass is insufficient. A clean feature worktree does not prove main is clean; integration, main's working-tree cleanliness and current remote synchronization are separate observations. A status request does not authorize fixes, installation, commits or deployment.

Source: `plugins/LEAPWare-Pulse/skills/LEAPWare-Pulse/SKILL.md`.

## Deterministic validation

Run the mutation suite with `python -m unittest discover -s tests -v`. To inspect the package directly, run `python scripts/validate_pulse_plugin.py plugins/LEAPWare-Pulse`; the command also accepts the repository root.

These checks verify the source package's fixed identity, inventory, metadata, report rules and authority boundary. They do not replace behavioral QA or fresh installation tests in Codex.

Learning is dropped from this release; the reporting helper (`lw-pulse.py`) is
self-contained and does not depend on any external capture or lesson-retrieval
subsystem.

`lw-acceptance.py` removed (private-origin); a clean-room acceptance runner is
rebuilt in D1.
