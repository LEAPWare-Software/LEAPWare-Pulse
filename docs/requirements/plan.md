# lwp recast plan (D0–D5)

Recasts LEAPWare-Pulse into the structure of its sibling plugin repos
(`lwt`, `lws`) and ports Panorama, Brief and Focus to Claude Code, to the
proof bar in `approach.md`. Requirements: `requirements.md`. Directives:
`owner-directives.md`.

Phase IDs follow the siblings (`D0`, `D1`, …); each phase's proof record
is `proof/LWP-Dn.json`, announced as `LWP - Alert: LWP-Dn DONE …`. A phase
is done only when committed, pushed, merged, CI green, and its proof record
is checked by a different identity from its author.

Sizes: **S** ≤ 1 session, ≤ 15 files; **M** 1–2 sessions, ≤ 40 files;
**L** 2–4 sessions, > 40 files or a behavior move.

## Target layout

```
.agents/plugins/marketplace.json      Codex marketplace -> plugins/codex/lwp
.claude-plugin/marketplace.json       Claude marketplace -> plugins/claude/lwp
.claude/settings.json  .codex/hooks.json   contributor-side only
.github/{apps,rulesets,workflows(ci,handoff,release),CODEOWNERS,dependabot.yml,ISSUE_TEMPLATE,PULL_REQUEST_TEMPLATE.md}
AGENTS.md CHANGELOG.md CLAUDE.md CODE_OF_CONDUCT.md CONTRIBUTING.md HANDOFF.md LICENSE NOTICE README.md SECURITY.md
adapters/{claude,codex}/              host edges (plugin root, output)
adapters/common/                      shared I/O edges: registry, git, locks, acceptance runner
core/lwp_core/{tasks,report,evidence,learning/*}.py   pure logic only (LWP-R29)
core/contract/{SKILL.md,formats.md}   the one view contract (LWP-R16)
core/policy/release-learning.json     trusted release pins
docs/{architecture,handoff-protocol,install-claude,install-codex,learning,policy}.md docs/maintainers/ docs/requirements/
plugins/{claude,codex}/lwp/{manifest,bin,skills/lwp-status,vendor}
proof/{README.md,schema.json,LWP-D*.json}  reviews/{README.md,schema.json}
scripts/lwp_*.py
tests/{adapters,behavioral,conformance,core,fixtures}/
```

`adapters/common/` is the one deviation from the sibling layout. Siblings
put all I/O in per-host hook adapters; Pulse has a substantial I/O layer
(registry storage, locks, git binding, acceptance runner) that is identical
on both hosts. Duplicating it per host would break LWP-R32. Recorded in
`docs/architecture.md` in D1.

## Gate G-PUB — public, rulesets applied (owner action)

- **Entry:** pre-publication history scan finished and accepted by the owner
  (it covers the 24 legacy-identity commits and the absolute local paths in
  `docs/evidence/*` history — no rewrite, per OD8); D0 merged.
- **Action (owner):** flip visibility to public; apply
  `.github/rulesets/main.json` with `scripts/lwp_apply_rulesets.py`; enable
  merge queue and auto-merge; create GitHub Apps `lwp-claude`/`lwp-codex`
  from `.github/apps/`.
- **Exit:** `gh repo view --json visibility` reads `PUBLIC`;
  `gh api repos/LEAPWare-Software/LEAPWare-Pulse/rulesets` shows the ruleset
  active with no bypass; a probe PR is merged through the queue.
- **Blocks:** merging D1 and later. Work on D1+ branches may start before it.
- **Size:** S (owner time, not a build phase).

## D0 — Skeleton parity and governance (M)

- **Entry:** this plan merged; owner answers to Q1 and Q3 (names used by the
  prefix check).
- **Work:** root meta files (Apache-2.0 LICENSE, NOTICE, SECURITY,
  CODE_OF_CONDUCT, CONTRIBUTING, CHANGELOG, AGENTS.md, CLAUDE.md with the
  worktree rule); `.github/` set; `pyproject.toml`, `.editorconfig`;
  `proof/` and `reviews/` schemas; `scripts/lwp_check_*` for prefix,
  identity (range mode plus legacy boundary at the D0 merge base), env-leak,
  no-instruction-dep, lanes, proof, trace, worktrees; `lwp_handoff.py`;
  `lwp_apply_rulesets.py`; `lwp_check_runners.py` (hosted runners only,
  every workflow); `docs/handoff-protocol.md`;
  `docs/requirements/traceability.md`. `ci.yml` replaces `validate.yml`
  and runs the existing 34 tests unchanged on the six-job matrix; a
  pre-recast test that cannot pass off Windows may be skipped on that OS
  only with a reason naming the D1 requirement that removes the skip. The
  existing Codex package stays where it is and keeps working.
- **Env-leak mode:** range mode (`--range base..head`) gates D0 and D1 PRs;
  the full-tree scan joins CI in D2, after `docs/evidence/*` is dropped.
- **Commit identity:** from this phase on, `LEAPWare <leapware@outlook.com>`,
  enforced per PR range (LWP-R2).
- **Requirements proven:** R2–R6, R8–R12, R39; R1 check exists (applies to real
  plugins in D2/D4).
- **Exit:** CI green on all six jobs; every D0 check broken on purpose and
  restored, recorded in `proof/LWP-D0.json`; `HANDOFF.md` passes
  `lwp_handoff.py --check`; `git worktree list` shows only the main worktree
  or entries under `.worktrees/`.

## D1 — Core extraction and adapters (L)

- **Entry:** D0 merged; owner answer to Q2 (learning subsystem).
  `lw-acceptance.py` removed (private-origin); a clean-room acceptance
  runner is rebuilt in D1.
- **Work:** capture golden outputs of the pre-recast helpers on fixture
  projects first. Move pure logic (checklist parsing, report assembly, spec
  and receipt validation, lesson records, pins) into `core/lwp_core`; move
  I/O (storage, locks, git binding, subprocess, registry path) into
  `adapters/common`; thin host edges into `adapters/{claude,codex}`. Port
  the 34 tests into `tests/{core,adapters}`. Fix the acceptance runner's
  Windows 8.3 alias defect (LWP-R28). Keep the learning data key
  `leapware-pulse` (LWP-R27).
- **Requirements proven:** R7, R13–R15, R20–R29.
- **Exit:** golden outputs byte-identical to the pre-recast helpers on every
  fixture (except the fixed alias defect, listed in the proof record);
  CI green on six jobs; `proof/LWP-D1.json`.

## D2 — Codex plugin at `plugins/codex/lwp` and tree dispositions (M)

- **Entry:** D1 merged; G-PUB passed.
- **Work:** `scripts/lwp_build.py` vendors core, adapters and the contract
  into `plugins/codex/lwp/vendor`; manifest, `bin/`, skill
  `lwp-status` (contract from `core/contract/`, Codex UI metadata
  `agents/openai.yaml`); marketplace repointed; old
  `plugins/LEAPWare-Pulse/` and `scripts/validate_pulse_plugin.py` removed;
  dispositions below applied; size budget set (LWP-R36); version 0.3.0.
- **Requirements proven:** R1 (Codex), R3 on the recast tree, R16–R19
  (Codex), R30, R33, R35, R36.
- **Exit:** CI green; a fresh Codex install from the repository renders all
  three views on the behavioral scenarios (LWP-R18, Codex half);
  `proof/LWP-D2.json`.

## D3 — Migration for existing Codex installs (S)

- **Entry:** D2 merged.
- **Work:** `scripts/lwp_migrate_codex.py` (read-only detector and printed
  steps); `docs/install-codex.md` migration section: remove
  `LEAPWare-Pulse@LEAPWare-Pulse`, re-add the marketplace, add `lwp`;
  existing learning registries keep working unchanged (LWP-R27). CHANGELOG
  states the manifest and skill path change.
- **Requirements proven:** R34.
- **Exit:** a real pre-recast install on one machine migrated by following
  only the doc, then all three views rendered, recorded in
  `proof/LWP-D3.json` with a second OS covered by the fixture test.

## D4 — Claude port at `plugins/claude/lwp` (L)

- **Entry:** D2 merged (D3 may run in parallel).
- **Work:** evidence first: the Claude-vs-Codex capability matrix for skill
  discovery, plugin-root resolution inside a skill, and script invocation,
  each row sourced from docs or a command run against the real CLI. Then the
  Claude manifest, `.claude-plugin/marketplace.json`, skill `lwp-status`
  from the same contract, vendor tree, `lwp_validate_claude_plugin.py`,
  conformance tests, `docs/install-claude.md`.
- **Requirements proven:** R1 (Claude), R16–R19 (Claude), R31, R32, R33,
  R35.
- **Exit:** CI green; a fresh Claude Code install renders all three views
  on the behavioral scenarios with properties judged by a reviewer that did
  not author the port; `proof/LWP-D4.json`.

## D5 — Rehearsal, independent proof, release 1.0.0 (M)

- **Entry:** D3 and D4 merged.
- **Work:** `scripts/lwp_rehearsal.py` and CI job `rehearsal` on all three
  OSes; real-install rehearsal on Claude Code and Codex; traceability matrix
  complete; version 1.0.0 via `release.yml`.
- **Requirements proven:** R37, R38, and a full re-run of every break in
  the traceability matrix against the release commit.
- **Exit:** `proof/LWP-D5.json` authored on one CLI and checked on the
  other; tag `v1.0.0` equals the manifest versions; CI green on the tag.

## Dispositions for items with no template slot

| Item | Decision | Reason |
|---|---|---|
| `docs/evidence/*.md` | Drop from tree in D2 | Absolute local paths fail LWP-R3; describes a private pre-public release. History keeps it; the history scan owns history. |
| `docs/validation.md` | Drop in D2; one-line 0.2.0 entry in CHANGELOG | Superseded by `proof/` and the traceability matrix; cites private CI runs. |
| `docs/superpowers/{plans,specs}/*` | Drop in D2 | Completed private-release planning; the template's homes for plans are `docs/requirements/` and `HANDOFF.md`. |
| `scripts/learning-origin.json` | Drop in D1 | Provenance of code copied from a private repository; its hash test is replaced by the vendor drift check (LWP-R16). Provenance, if any, goes in NOTICE per Q2. |
| `scripts/release-learning.json` | Move to `core/policy/release-learning.json`, vendored | Trusted release metadata; one source for both hosts. |
| `scripts/learning/README.md` | Move to `docs/learning.md`, rewritten | Operator documentation; its references to upstream tests are wrong here. |
| `tests/behavioral-scenarios.md`, `tests/checklist-view-scenarios.md` | Move to `tests/behavioral/` | Acceptance inputs for LWP-R18; synthetic data. |
| `skills/LEAPWare-Pulse/agents/openai.yaml` | Move to `plugins/codex/lwp/skills/lwp-status/agents/` | Codex-only UI metadata. |
| `.github/workflows/validate.yml` | Replace with `ci.yml` in D0 | Windows and 3.12 only; fails LWP-R6. |
| `scripts/validate_pulse_plugin.py` | Replace with `lwp_validate_codex_plugin.py` in D2 | Mutation cases ported (LWP-R17). |

## Decisions (CTO, 2026-09-17)

**Q1 ACCEPTED.** The Claude plugin name is `lwp` in both manifests and
marketplaces; the marketplace name is `leapware-pulse`.

**Q2 DECIDED (owner, 2026-09-17).** The learning code migrated from the
private [removed] is stripped from ALL Pulse history before
going public, and learning is dropped from 1.0. G-PUB runs after the
rewrite and after an independent scan verifies it.

**Q3 ACCEPTED.** One skill, `lwp-status`, answering to `lwp panorama` /
`lwp brief` / `lwp focus`; `lw-pulse` stays an alias through 1.x;
`lw-status` is dropped.

**Q4 ACCEPTED.** No hooks in 1.0; the validators check that none are
registered.

**Q5 ACCEPTED.** 0.3.0 at D2, 1.0.0 at D5.

## Corrections

**Test count, 2026-09-17 (D0).** This plan said "the existing 42 tests" in
D0 and D1. Re-measured at the D0 branch point (`8bccb1c`):
`python -m unittest discover -s tests` runs **34**, all passing. The
learning-subsystem removal (`0586920`) dropped the difference. Both
occurrences corrected to 34 so the D0 exit condition is checkable.
