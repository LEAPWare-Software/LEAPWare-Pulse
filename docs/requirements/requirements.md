# lwp requirements (draft for audit, not frozen)

Numbered, testable requirements for lwp 1.0.0. Each traces to a line of
`owner-directives.md` (shown as `OD#`, to keep them apart from phase IDs `D0`–`D5`). Each has:

- **Rule** — what must be true.
- **Test** — the automated acceptance test (Given/When/Then) and the file
  it lives in once built. Paths are the target layout from `plan.md`.
- **Break** — how the rule is broken on purpose to prove the test catches
  it. The broken run and the restored run are both recorded in the phase
  proof record (`proof/LWP-Dn.json`, `commands[]` with `expect_exit`).
- **Phase** — the `plan.md` phase that must prove it.

Requirements marked *(pending Qn)* depend on an owner answer in `plan.md`;
their wording follows the recommendation and is amended if the owner
decides otherwise.

## A. Repository and governance

### LWP-R1 — Prefix (OD1) *(pending Q1, Q3)*
- **Rule:** every skill directory under `plugins/**/skills/` starts with
  `lwp-` and its front-matter `name:` equals the directory; every
  `plugins/*/lwp/bin/*.py` and `scripts/*.py` entrypoint starts with `lwp`;
  both plugin manifests and both marketplace entries are named `lwp`.
- **Test:** Given the tree, when `scripts/lwp_check_prefix.py` runs, then
  it exits 0 and prints `lwp-prefix check passed`
  (`tests/test_lwp_check_prefix.py`).
- **Break:** in a fixture copy, rename a skill directory to `pulse-status`
  and set one manifest name to `LEAPWare-Pulse`; the check exits 1 and
  names both.
- **Phase:** D0 (check), D2 and D4 (real plugins).

### LWP-R2 — Commit identity going forward (OD8)
- **Rule:** every commit in a PR range `base..head` is authored
  `LEAPWare <leapware@outlook.com>` or an allow-listed GitHub bot. The
  full-history mode stops at a committed legacy boundary (the last commit
  before the switch); commits at or before it are reported as legacy, not
  failures. No history rewrite.
- **Test:** Given a fixture repo, when
  `scripts/lwp_check_commit_identity.py --base B --head H` runs on a range of
  LEAPWare commits, then exit 0; on full history with legacy commits only
  below the boundary, exit 0 (`tests/test_lwp_check_commit_identity.py`).
- **Break:** add a fixture commit with a different author inside the range,
  and a legacy-identity commit above the boundary; each exits 1.
- **Phase:** D0.

### LWP-R3 — No local-environment or private leak (OD6, OD7)
- **Rule:** no tracked file and no line added in a PR range contains an
  absolute user path (drive-letter or home-directory form), a local
  hostname, or a name on the private-name list.
- **Test:** Given the tree, when `scripts/lwp_check_env_leak.py` and
  `--range base..head` run, then both exit 0
  (`tests/test_lwp_check_env_leak.py`).
- **Break:** add a drive-letter user path to a fixture file (exit 1); add
  it in one commit and revert it in the next, then scan the range (still
  exit 1).
- **Phase:** D0; D2 must pass it on the recast tree (see dispositions).

### LWP-R4 — No instruction-file dependency (OD2)
- **Rule:** no shipped runtime file (`core/`, `adapters/`, `plugins/**`)
  reads `CLAUDE.md` or `AGENTS.md`.
- **Test:** `scripts/lwp_check_no_instruction_dep.py` exits 0
  (`tests/test_no_instruction_file_dependency.py`).
- **Break:** add an `open("AGENTS.md")` line to a fixture core module;
  exit 1.
- **Phase:** D0.

### LWP-R5 — Ruleset shape (OD3)
- **Rule:** `.github/rulesets/main.json` targets the default branch, has no
  bypass actors, blocks deletion and non-fast-forward, requires a PR with
  squash only, requires exactly the CI job names of `ci.yml`, and enables
  the merge queue with squash.
- **Test:** `tests/test_rulesets_shape.py`, plus
  `scripts/lwp_apply_rulesets.py --dry-run --repo LEAPWare-Software/LEAPWare-Pulse`
  exits 0 and prints the payload.
- **Break:** add one bypass actor (fail); rename one CI matrix job without
  updating the ruleset (fail).
- **Phase:** D0 (files); gate G-PUB (applied).

### LWP-R6 — Hosted cross-platform CI (OD6)
- **Rule:** the CI test matrix covers `windows-latest`, `macos-latest` and
  `ubuntu-latest` with Python 3.10 and 3.12. (Runner kind: LWP-R39.)
- **Test:** `tests/test_ci_matrix.py` parses `ci.yml` and asserts the six
  combinations.
- **Break:** drop `macos-latest` from the matrix; the test fails.
- **Phase:** D0.

### LWP-R7 — Standard library only (OD2)
- **Rule:** `core/`, `adapters/` and everything shipped under
  `plugins/*/lwp/` import only the Python 3.10 standard library and their
  own package modules.
- **Test:** `tests/test_stdlib_only.py` walks imports with `ast` and checks
  them against `sys.stdlib_module_names` plus the package allow-list.
- **Break:** add `import yaml` to a fixture core module; the test fails.
- **Phase:** D1.

### LWP-R8 — CLI lanes (OD2)
- **Rule:** a commit from the Codex lane changes only Codex-lane paths, a
  commit from the Claude lane only Claude-lane paths; shared paths
  (`core/`, `scripts/`, `.github/`, `docs/`, `proof/`, `reviews/`) change
  only with review records from both CLIs under `reviews/<pr>/`.
- **Test:** `scripts/lwp_check_lane_write.py` and `scripts/lwp_lanes.py`
  (`tests/test_lwp_check_lane_write.py`, `tests/test_lwp_lanes.py`).
- **Break:** a fixture Codex-lane commit touching `plugins/claude/lwp/`
  (fail); a shared-path change with only one CLI's review record (fail).
- **Phase:** D0.

### LWP-R9 — Worktree location (OD9)
- **Rule:** every linked worktree of the repository is under
  `<repo>/.worktrees/<branch>`; `.gitignore` contains `.worktrees/`; no
  sibling folder next to the repository is a worktree of it or a clone of
  the same `origin`; `AGENTS.md` and `CLAUDE.md` both state the rule.
- **Test:** `scripts/lwp_check_worktrees.py` reads
  `git worktree list --porcelain` and fails on any worktree outside
  `<toplevel>/.worktrees/`; scans only the immediate siblings of the
  top-level for a `.git` file pointing into this repository or a `.git/config`
  naming the same `origin` URL; checks `.gitignore` and both instruction
  files for the rule (`tests/test_lwp_check_worktrees.py`, all in temporary
  fixture directories). The PR template carries the same item for review.
- **Break:** in a temporary fixture, `git worktree add ../sibling-wt` (exit
  1, names the path); clone the fixture into a sibling folder (exit 1);
  remove `.worktrees/` from the fixture `.gitignore` (exit 1); delete the
  rule sentence from the fixture `CLAUDE.md` (exit 1).
- **Phase:** D0.

### LWP-R10 — Proof records (OD5)
- **Rule:** every `proof/*.json` validates against `proof/schema.json`;
  `checked_by` differs from `author`; each command's `exit` equals its
  `expect_exit`; each phase D0–D5 has a record before its exit gate closes.
- **Test:** `scripts/lwp_check_proof.py` (`tests/test_lwp_check_proof.py`).
- **Break:** set `checked_by` equal to `author` in a fixture record (exit
  1); set one `exit` different from `expect_exit` (exit 1).
- **Phase:** D0.

### LWP-R11 — Handoff file (OD2)
- **Rule:** `HANDOFF.md` is at most 6000 bytes, carries the
  `lwp-handoff:begin`/`end` markers, and contains no absolute path;
  `scripts/lwp_handoff.py --write` regenerates only the marked block.
- **Test:** `scripts/lwp_handoff.py --check` (`tests/core/test_lwp_handoff.py`).
- **Break:** pad a fixture to 6001 bytes (fail); insert a drive-letter path
  (fail); edit prose outside the markers and run `--write` (prose unchanged).
- **Phase:** D0.

### LWP-R12 — Traceability (OD5)
- **Rule:** every `LWP-R` ID in this file has a row in the traceability
  matrix naming at least one existing test node and a break description;
  no row names an ID that does not exist here.
- **Test:** `scripts/lwp_check_trace.py` (`tests/test_lwp_check_trace.py`).
- **Break:** delete a referenced test function (fail); add an `LWP-R99`
  heading with no row (fail).
- **Phase:** D0 (check), every phase (rows).

### LWP-R39 — GitHub-hosted runners only (OD10)
- **Rule:** every `runs-on` in every `.github/workflows/*.yml`, including
  each value a matrix expression can expand to, is a GitHub-hosted label
  matching `ubuntu-*`, `windows-*` or `macos-*`. Never `self-hosted`, a
  custom label, a runner group, or a local runner.
- **Test:** `scripts/lwp_check_runners.py` parses every workflow and exits 0
  only when all labels match (`tests/test_lwp_check_runners.py`); it runs as
  a step of every CI job.
- **Break:** add `runs-on: self-hosted` to a fixture workflow (exit 1, names
  the file and job); add `self-hosted` to a matrix `os` list (exit 1); add
  a `group:` runner mapping (exit 1).
- **Phase:** D0.

## B. Pulse views and verification

### LWP-R13 — Checklist parsing (OD4)
- **Rule:** the task reader counts `- [x]`/`- [X]` as checked and `- [ ]`
  as unchecked, reports `checked` and `total`, and refuses a task document
  over 256 KiB.
- **Test:** `tests/core/test_tasks.py` golden fixtures, run against the
  pre-recast `lw-pulse.py` output in D1 to prove parity.
- **Break:** treat `[X]` as unchecked, or raise the cap to 1 MiB; the
  golden and cap tests fail.
- **Phase:** D1.

### LWP-R14 — Checked is not verified (OD4)
- **Rule:** without both `--spec` and `--evidence`, `verification` is
  `unknown`; supplying only one is refused; `pushed`, `packaged`, `active`
  and `tokens` stay `unknown`.
- **Test:** `tests/core/test_report.py` (ported from
  `test_checked_tasks_are_not_verification`).
- **Break:** set `verification` to `pass` when `checked == total`; fail.
- **Phase:** D1.

### LWP-R15 — Source-bound evidence (OD4)
- **Rule:** a spec whose candidate differs from `git rev-parse HEAD` is
  stale and yields `unverified` with a capture receipt; only a verified
  receipt sets `source_fixed` to that HEAD.
- **Test:** `tests/adapters/test_evidence.py` (ported from
  `test_real_passing_receipt_from_previous_revision_is_refused`).
- **Break:** remove the candidate-equals-HEAD comparison; the stale
  receipt is accepted and the test fails.
- **Phase:** D1.

### LWP-R16 — One view contract, two hosts (OD4)
- **Rule:** the Panorama, Brief and Focus contract (skill body and
  `formats.md`) has one source of truth and is vendored byte-identically
  into both plugins.
- **Test:** `scripts/lwp_build.py --check` (`tests/test_vendor_committed.py`).
- **Break:** edit one sentence in the Claude copy of `formats.md` only; the
  drift check fails.
- **Phase:** D2 (Codex), D4 (Claude).

### LWP-R17 — Contract rules present (OD4)
- **Rule:** the shipped contract states: full plan retained; unknown
  denominator is *Not yet measurable*; `floor` percentage and ten-cell bar;
  unfinished criteria unchecked; optional work outside totals; explicit view
  overrides a recorded preference, default Panorama, one-off requests not
  persisted; evidence gate; main-clean rule; status grants no authority.
- **Test:** `scripts/lwp_validate_codex_plugin.py` and
  `scripts/lwp_validate_claude_plugin.py`, each with the mutation cases
  ported from `test_validate_pulse_plugin.py` and `test_pulse_formats.py`
  (`tests/test_lwp_validate_*_plugin.py`).
- **Break:** for each rule, delete its sentence from a fixture copy of each
  host's skill; each deletion fails its named case.
- **Phase:** D2, D4.

### LWP-R18 — Behavioral parity on both hosts (OD4, OD5)
- **Rule:** the behavioral scenarios (`BHV-*`, `BP-*`) pass on Codex and on
  Claude Code, each run by a fresh evaluator given only the shipped skill
  and one scenario; raw outputs are hashed into the proof record.
- **Test:** `tests/behavioral/README.md` protocol, run per host in D2 and
  D4; each property judged by a reviewer that did not author the skill.
- **Break:** run `BHV-03` against a skill copy with the unknown-denominator
  rule removed; the judged result must be FAIL. A scenario that cannot
  detect this is itself a defect.
- **Phase:** D2 (Codex), D4 (Claude).

### LWP-R19 — Authority boundary (OD4) *(pending Q4)*
- **Rule:** neither plugin registers hooks, MCP servers, apps or background
  agents; the contract states that a status request authorizes no fix,
  install, commit or deployment.
- **Test:** both plugin validators assert zero such registrations.
- **Break:** add a `hooks` entry to the Claude manifest, or an
  `mcpServers` entry to the Codex manifest; the validator fails.
- **Phase:** D2, D4.

## C. Learning subsystem *(pending Q2)*

### LWP-R20 — Capture carries no payload (OD7)
- **Rule:** a boundary failure capture records only the exception class
  and hashes; no message text or input bytes leave the caller.
- **Test:** `tests/adapters/test_capture.py` (ported
  `test_malformed_input_captured_without_private_payload`).
- **Break:** put `str(error)` into the `actual` field; fail.
- **Phase:** D1.

### LWP-R21 — Capture failure is visible (OD4)
- **Rule:** an unavailable registry yields `health: unavailable` with a
  warning, never `captured`.
- **Test:** ported `test_registry_failure_visible`.
- **Break:** return `captured` from the exception path; fail.
- **Phase:** D1.

### LWP-R22 — Storage ceilings (OD4)
- **Rule:** 8 KiB per record, 8 MiB per project, 24 MiB aggregate; admission
  is refused at capacity; nothing is pruned silently.
- **Test:** ported `test_cap_capture_failure_visible` plus a record-size case.
- **Break:** raise the record limit to 16 KiB; fail.
- **Phase:** D1.

### LWP-R23 — Private capture marker (OD7)
- **Rule:** before the first incident write, `.leapware/local/learning/.gitignore`
  exists with exactly `*\n`, created exclusively; a differing marker refuses
  capture and no user file is overwritten.
- **Test:** ported `test_capture_is_ignored_in_fresh_consumer_git_root`.
- **Break:** skip marker creation; `git status` in the fixture shows the
  incident and the test fails.
- **Phase:** D1.

### LWP-R24 — Lesson lifecycle and pins (OD4)
- **Rule:** stale, wrong-scope and withdrawn lessons are inactive; a new
  recurrence invalidates active lessons; a consumer export that mismatches
  its release pin, or was edited, is refused; release pins have exactly
  the empty shape or `snapshot`, `expected_version`, `expected_sha256`.
- **Test:** ported `test_stale_wrongscope_and_withdrawn_lesson_not_active`,
  `test_consumer_pin_and_tampered_export`, `test_private_publication_refused`.
- **Break:** treat a withdrawn lesson as active; fail. Edit one byte of a
  fixture export; must still be refused.
- **Phase:** D1.

### LWP-R25 — Concurrency and idempotence (OD4)
- **Rule:** distinct sessions get distinct occurrences; an unchanged event
  is a no-op; contended capture is reported unavailable and later reconciles
  without duplicates.
- **Test:** ported `test_parallel_sessions_and_project_ownership`,
  `test_contended_capture_is_unavailable_then_reconciled_without_duplicates`.
- **Break:** bypass the registry lock; duplicates appear and the test fails
  (run 20 iterations in the proof run to rule out a lucky pass).
- **Phase:** D1.

### LWP-R26 — Registry location on every OS (OD6)
- **Rule:** `LEAPWARE_LEARNING_HOME` wins; otherwise
  `%LOCALAPPDATA%/LEAPWare/state/learning` when `LOCALAPPDATA` is set,
  otherwise `~/.local/share/LEAPWare/state/learning`; resolution writes
  nothing.
- **Test:** `tests/adapters/test_registry_path.py` on all six CI jobs.
- **Break:** read `os.environ["LOCALAPPDATA"]` unconditionally; the macOS
  and Linux jobs fail.
- **Phase:** D1.

### LWP-R27 — Stable data key across the rename (OD1)
- **Rule:** learning records keep the plugin key `leapware-pulse` and the
  consumer paths `.leapware/local/learning/` and `.leapware/learning/exports/`,
  so registries written by 0.2.x keep working under lwp.
- **Test:** `tests/adapters/test_legacy_registry.py` loads a fixture registry
  written by the pre-recast code and retrieves its validated lesson.
- **Break:** change the key to `lwp`; retrieval returns no lesson; fail.
- **Phase:** D1.

### LWP-R28 — Path safety (OD6)
- **Rule:** traversal is refused before canonicalization; symlinks and
  junctions are refused; a Windows 8.3 short alias of the root is accepted
  by both the report and the acceptance runner.
- **Test:** ported `test_root_traversal_is_refused_before_canonicalization`,
  both short-alias tests, plus a new acceptance-runner alias case
  (Windows-only, skipped elsewhere with a stated reason).
- **Break:** remove the lexical traversal check (fail); remove alias
  normalization from the acceptance runner (the new case fails with
  `write escapes managed scratch root`).
- **Phase:** D1 (fixes the known deferred defect).

## D. Plugins, packaging, release

### LWP-R29 — Pure core (OD2)
- **Rule:** `core/lwp_core` does no I/O: no file, stdin, environment,
  clock, subprocess or network access.
- **Test:** `tests/core/test_core_is_pure.py` scans `core/lwp_core` with
  `ast` for forbidden calls and imports.
- **Break:** add `import subprocess` to a fixture core module; fail.
- **Phase:** D1.

### LWP-R30 — Codex plugin valid (OD2, OD4)
- **Rule:** `plugins/codex/lwp/.codex-plugin/plugin.json` has name `lwp`, a
  semver version, a `skills` path that exists, and an exact file inventory;
  `.agents/plugins/marketplace.json` points at it.
- **Test:** `scripts/lwp_validate_codex_plugin.py`.
- **Break:** change the marketplace path to `./plugins/LEAPWare-Pulse`;
  fail.
- **Phase:** D2.

### LWP-R31 — Claude plugin valid (OD4)
- **Rule:** `plugins/claude/lwp/.claude-plugin/plugin.json` and
  `.claude-plugin/marketplace.json` are well formed, the source path exists,
  and the inventory is exact.
- **Test:** `scripts/lwp_validate_claude_plugin.py`.
- **Break:** point the marketplace `source` at a missing directory; fail.
- **Phase:** D4.

### LWP-R32 — Same answer on both hosts (OD4)
- **Rule:** the same fixture project through the Claude and the Codex
  report entrypoints yields byte-identical report JSON.
- **Test:** `tests/conformance/test_same_report_both_adapters.py`.
- **Break:** reorder keys in the Codex adapter's output; fail.
- **Phase:** D4.

### LWP-R33 — Helper launches on every OS (OD6)
- **Rule:** the helper command each skill tells the model to run resolves
  the plugin root and a Python 3 interpreter on Windows, macOS and Linux
  without a machine-specific path.
- **Test:** `scripts/lwp_check_helper_launch.py` runs each skill's
  documented command against a fixture project in every CI job.
- **Break:** change the documented command to a Windows-only launcher; the
  macOS and Linux jobs fail.
- **Phase:** D2, D4.

### LWP-R34 — Codex install migration (OD2) *(pending Q3)*
- **Rule:** `scripts/lwp_migrate_codex.py --config <path>` is read-only: it
  detects a pre-recast `LEAPWare-Pulse@LEAPWare-Pulse` install and prints
  the exact remove and add commands, exiting 3; with no old install it exits
  0. `docs/install-codex.md` carries the same steps.
- **Test:** `tests/test_lwp_migrate_codex.py` with fixture config files;
  asserts the fixture bytes are unchanged afterwards.
- **Break:** make the script return 0 on an old install (fail); make it
  write the config (byte-equality assertion fails).
- **Phase:** D3.

### LWP-R35 — One version everywhere (OD2)
- **Rule:** both manifests, both marketplace entries and the top
  `CHANGELOG.md` entry carry the same version; a release tag equals it.
- **Test:** `scripts/lwp_release.py --check`.
- **Break:** bump the Codex manifest only; fail.
- **Phase:** D2 (Codex), D4 (both).

### LWP-R36 — Size budget (OD2)
- **Rule:** each shipped plugin tree stays within a byte budget set in D2
  from the measured recast size plus 20 percent, recorded in
  `scripts/lwp_build.py`.
- **Test:** `scripts/lwp_build.py --check` reports size against budget.
- **Break:** add a 1 MiB fixture file to a vendor tree; fail.
- **Phase:** D2.

### LWP-R37 — Rehearsal (OD5)
- **Rule:** a scripted rehearsal runs on each OS against a fixture project
  and covers: checked-but-unverified tasks, a stale receipt, a passing
  source-bound receipt, unavailable capture, lesson retrieval, and all three
  views on both hosts' skill copies. A recorded rehearsal on a real Claude
  Code install and a real Codex install renders Panorama, Brief and Focus
  from the same fixture.
- **Test:** CI job `rehearsal` (`scripts/lwp_rehearsal.py`), expected
  outputs committed under `tests/fixtures/rehearsal/`.
- **Break:** plant a passing receipt from a previous commit into the
  fixture and change the expected output to `source-bound pass`; the job
  fails because the real run reports `unverified`.
- **Phase:** D5.

### LWP-R38 — Independent final proof (OD5)
- **Rule:** `proof/LWP-D5.json` is checked by a different identity from its
  author, running on the other CLI from the author's, and lists every
  unproven item explicitly.
- **Test:** `scripts/lwp_check_proof.py` plus a D5-specific assertion that
  the author and checker CLIs differ.
- **Break:** set both to the same CLI in a fixture; fail.
- **Phase:** D5.

## Traceability matrix

Built in D0 at `docs/requirements/traceability.md` and enforced by
LWP-R12. Every row: requirement ID, test node IDs, break description,
proof record.
