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

Run the mutation suite with `py -3.12 -m unittest discover -s tests -v`. To inspect the package directly, run `py -3.12 scripts/validate_pulse_plugin.py plugins/LEAPWare-Pulse`; the command also accepts the repository root.

These checks verify the source package's fixed identity, inventory, metadata, report rules and authority boundary. They do not replace behavioral QA or fresh installation tests in Codex.

The bundled upstream learning README refers to its own `tests/test_learning.py`.
In this Pulse repository, the executable integration workflow is
`tests/test_plugin_learning_cycle.py`; use the discovery command above. Its
concurrency checks distinguish acknowledged capture from unavailable receipts,
reconcile uncertain effects before same-session retries, and verify idempotence.

## Bounded learning (candidate 0.2.0)

The plugin bundles the reviewed [removed] learning helper and acceptance verifier;
`plugins/LEAPWare-Pulse/scripts/learning-origin.json` records exact origin commits,
paths and SHA-256 values. It works without [removed] running. See the bundled
`learning/README.md` for capture, diagnosis, proposal, checked validation,
sanitation, promotion, withdrawal, recurrence and export commands. Those are
explicit operator operations; incident data and lesson text are never executed.

The bundled acceptance runner has a known Windows short-path limitation: mixed
8.3 aliases and long names can produce `write escapes managed scratch root`.
For this pinned revision, supply canonical absolute long-name paths for `--root`,
`--spec`, `--evidence` and `--scratch-root`. Validate lexical paths for traversal
and symlinks/junctions before resolving operator input; never bypass those checks.
The integration tests canonicalize only their own newly created temporary fixture.
The Pulse report helper separately accepts real short-root aliases and retains
traversal and containment tests. Acceptance-runner alias support remains a deferred
upstream defect, not a fixed behavior in this release. A failed acceptance run may
already have executed cases and created a partial evidence directory: inspect the
failed run, then use a fresh evidence directory after correcting the paths. A
refused or incomplete receipt is never passing evidence.

All three plugins use `LEAPWARE_LEARNING_HOME` when set, otherwise
`LOCALAPPDATA/LEAPWare/state/learning` (non-Windows fallback
`~/.local/share/LEAPWare/state/learning`). Share this exact registry convention.
Private incidents remain in the project's ignored `.leapware/local/learning/`;
no project source, transcript or environment dump is copied into the registry.
Capture saves sanitized failure classifications and hashes, not raw exceptions.
Instrumented command failures produce a receipt on stderr. The one-second capture
timeout may leave an uncertain effect: inspect the issue ID before retrying.
Capture unavailability is visible and never treated as evidence of successful capture.
Distinct sessions produce separate occurrence identities; exact unchanged events
are no-ops. New recurrence invalidates prior active lessons. Cross-process callers
must use stable session IDs and a new occurrence identity for a newly observed run.

The helper enforces 8 KiB records, 8 MiB per project and 24 MiB aggregate managed
learning storage. It refuses admission at capacity; no silent pruning or backup.
Limits apply to enrolled paths, not all disk usage or Git history. Mandatory lesson
retrieval overflow blocks advice selection; optional advice stays bounded. Lesson
records are advice only and never change owner authority or global instructions.

`release-learning.json` is trusted package metadata. This candidate ships `{}`,
so it reads current locally validated lessons and includes exact canonical IDs,
versions and validation hashes. A reviewed release may pin a snapshot using
`snapshot`, `expected_version`, `expected_sha256`; the enrolled consumer project's
`.leapware/learning/exports/NAME.json` must match that pin. The pin must come from
release review, never from the untrusted export. Consumer copies retain canonical
identity; editing them fails verification. Offline revocation freshness is explicitly
unknown until an updated trusted release is installed. Withdrawn/stale local lessons
are excluded. No active learned policy or distribution readiness is claimed merely
because tests passed.

Coverage is limited to the documented plugin boundaries. Hidden runtime failures,
commands outside these helpers and failed captures cannot be claimed as observed.
Expected failure injections in the tests use disposable isolated projects/registries;
fixture reviewer names demonstrate schema assertions, not actual independent review.
Native trust, packaging, cold compaction and active-runtime acceptance remain separate
release checks owned by the coordinator.


Private runtime capture now establishes `.leapware/local/learning/.gitignore` with
exact `*` content before writing an incident. Its two bytes count in the reviewed
managed storage budget and admission uses the same registry lock. Existing differing,
partial or redirected markers cause visible capture refusal; no user ignore file is
overwritten. Public lessons and semantic handoffs remain eligible for publication.
This protects ordinary Git adds, not explicit force-add or already tracked files.
