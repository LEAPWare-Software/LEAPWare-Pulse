# LEAPWare Pulse

Concise checklist progress reporting that keeps the full agreed plan visible, with subtasks, verified completion percentages and compact progress bars: complete, active, next, remaining, blocked and unverified work.

Use `lw-pulse` in a task or select the LEAPWare-Pulse skill. The phrase is not a shell command. The skill also supports ordinary status requests, progress updates and handoffs through automatic skill selection.

This dedicated repository belongs to LEAPWare-Software. The Codex plugin contains one self-contained skill; it adds no hooks, MCP servers, scheduled jobs or background agents. Reporting does not change task authorization or replace a continuity record.

## Install

Register this repository with `codex plugin marketplace add <repository-root>`, then run `codex plugin add LEAPWare-Pulse@LEAPWare-Pulse`. Check selection in a fresh task after installation.

## Reporting contract

Keep the entire committed plan in milestone order, including completed work. Check a box only when its stated outcome has evidence. Keep partial, blocked, failed or unverified work unchecked. Preserve owner corrections, material gates and the exact next action. Separate optional proposals from approved work. Prefer a brief checklist over a narrative activity log.

Each milestone shows its acceptance criteria as nested checkbox subtasks. Percentages count verified criteria against the explicit complete checklist, not effort or time; show the fraction beside a ten-cell progress bar. Unknown denominators are not yet measurable. Explain changes to the counting basis, and reserve 100% for verified completion of every required criterion.

Source: `plugins/LEAPWare-Pulse/skills/LEAPWare-Pulse/SKILL.md`.

## Deterministic validation

Run the mutation suite with `py -3.12 -m unittest discover -s tests -v`. To inspect the package directly, run `py -3.12 scripts/validate_pulse_plugin.py plugins/LEAPWare-Pulse`; the command also accepts the repository root.

These checks verify the source package's fixed identity, inventory, metadata, report rules and authority boundary. They do not replace behavioral QA or fresh installation tests in Codex.

## Bounded learning (candidate 0.2.0)

The plugin bundles the reviewed [removed] learning helper and acceptance verifier;
`plugins/LEAPWare-Pulse/scripts/learning-origin.json` records exact origin commits,
paths and SHA-256 values. It works without [removed] running. See the bundled
`learning/README.md` for capture, diagnosis, proposal, checked validation,
sanitation, promotion, withdrawal, recurrence and export commands. Those are
explicit operator operations; incident data and lesson text are never executed.

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
