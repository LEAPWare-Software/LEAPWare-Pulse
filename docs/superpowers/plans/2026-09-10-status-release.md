# LEAPWare Status Private Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a tested, independently vetted, privately released, and verified-installed LEAPWare-status plugin.

**Architecture:** A standard-library Python validator checks the source package and is exercised by mutation tests locally and in GitHub Actions. Independent behavioral QA, source review, runtime installation, and release verification produce source-bound evidence outside the plugin runtime.

**Tech Stack:** Markdown skill, JSON plugin manifest, YAML UI metadata, Python 3.12 standard library, `unittest`, GitHub Actions, Codex CLI 0.153.4.

**Spec:** `docs/superpowers/specs/2026-09-10-status-release-design.md`

## Global Constraints

- Keep `LEAPWare-Software/LEAPWare-Status` private and LEAPWare-only.
- Preserve the plugin name `LEAPWare-status` and command phrase `lw-status`.
- Do not add hooks, MCP servers, background agents, scheduled jobs, or runtime executable helpers.
- Percentages equal `floor(100 * verified / total)`; bars equal `floor(10 * verified / total)` filled cells; unknown or empty denominators are not measurable.
- Required, failed, blocked, partial, and unverified criteria remain visible and unchecked; optional unapproved work stays outside totals.
- Do not claim testing, review, installation, or readiness without fresh evidence bound to the exact candidate.
- Keep a durable SDD ledger and reconcile it after interruption or compaction.
- Finish with accepted work on private `main`, matching `origin/main`, and a clean working tree.

---

### Task 1: Deterministic validator and continuous checks

**Files:**
- Create: `scripts/validate_status_plugin.py`
- Create: `tests/test_validate_status_plugin.py`
- Create: `.github/workflows/validate.yml`
- Modify: `README.md`

**Interfaces:**
- Consumes: repository root or an explicit plugin directory.
- Produces: `validate(plugin_dir) -> list[str]` and a command that exits 0 only when no errors exist.

- [ ] **Step 1: Write failing mutation tests**

Create `tests/test_validate_status_plugin.py` with `unittest` cases that import `validate`, confirm the real package passes, then copy the package to temporary directories and prove rejection of: a wrong manifest name, undeclared extra top-level capability, missing full-plan rule, missing unknown-denominator rule, incorrect percentage-floor rule, missing authority boundary, and missing `$LEAPWare-status` default prompt.

- [ ] **Step 2: Run the tests and verify RED**

Run: `py -3.12 -m unittest discover -s tests -v`

Expected: FAIL because `scripts.validate_status_plugin` does not exist.

- [ ] **Step 3: Implement the minimal validator**

Create `scripts/validate_status_plugin.py` using only `argparse`, `json`, and `pathlib`. `validate()` must parse the manifest, inspect the exact package inventory, read `SKILL.md` and `agents/openai.yaml`, and return one error per violated acceptance invariant. The CLI prints every error and exits 1 when any exist; otherwise it prints `LEAPWare-status validation passed` and exits 0.

- [ ] **Step 4: Verify GREEN and mutation coverage**

Run: `py -3.12 -m unittest discover -s tests -v`

Expected: all tests pass with zero failures and every mutation is detected.

- [ ] **Step 5: Add CI and usage documentation**

Create `.github/workflows/validate.yml` to run the exact unittest command on `windows-latest` with Python 3.12 for pushes and pull requests. Add the local validation command and its limits to `README.md`; state that deterministic checks do not replace behavioral QA or fresh installation tests.

- [ ] **Step 6: Run full local validation and commit**

Run both `py -3.12 -m unittest discover -s tests -v` and `py -3.12 scripts/validate_status_plugin.py plugins/LEAPWare-status`.

Commit the task with its tests and documentation.

---

### Task 2: Independent behavioral QA

**Files:**
- Create: `tests/behavioral-scenarios.md`
- Create: `docs/evidence/behavioral-validation-2026-09-10.md`

**Interfaces:**
- Consumes: exact candidate commit and realistic status prompts with complete fixture evidence.
- Produces: independently authored, source-bound prompts, raw outputs, verdicts, limitations, and reproducible failing cases. QA does not modify product source.

- [ ] **Step 1: Define behavioral cases before changing the skill**

Record seven cases: complete and partial milestones; 99/100 flooring; unknown or empty denominator; added required scope with optional work; failed and unverified work; later evidence reopening a completed item; and a status request that does not authorize external action.

- [ ] **Step 2: Run independent RED/baseline evaluations**

Give each evaluator only the installed skill, one fixture, and one request. Save each exact prompt and response. Judge against explicit expected properties, not preferred wording.

- [ ] **Step 3: Judge every case against its written properties**

Record PASS or FAIL for each required property. Preserve every failing output unchanged so a separate implementer can reproduce it.

- [ ] **Step 4: Save complete QA evidence**

Save source identity, environment, commands or dispatch method, prompts, raw outputs, verdicts, skips, and untested paths. Do not call failed, skipped, or unavailable behavior ready.

- [ ] **Step 5: Validate and commit**

Run the deterministic suite and plugin validator again. Commit only the independently authored scenario matrix and evidence.

---

### Task 3: Correct demonstrated behavioral failures

**Files:**
- Modify only for a reproducible Task 2 failure: `plugins/LEAPWare-status/skills/LEAPWare-status/SKILL.md`
- Modify only if UI metadata becomes inconsistent: `plugins/LEAPWare-status/skills/LEAPWare-status/agents/openai.yaml`
- Append rerun evidence: `docs/evidence/behavioral-validation-2026-09-10.md`

**Interfaces:**
- Consumes: exact failing Task 2 prompt, output, expected property, and source identity.
- Produces: the smallest justified skill correction plus unchanged-case rerun evidence. If Task 2 has no failures, record this task as not required and make no product edit.

- [ ] **Step 1: Reproduce each failing behavior**

Run the exact failing case against the same source and confirm the failure before editing the skill.

- [ ] **Step 2: Make the smallest instruction correction**

Change only guidance directly supported by the observed failure. Preserve discovery, reporting shape, authority limits, and all passing behavior.

- [ ] **Step 3: Rerun failed cases and one passing regression case**

Require every formerly failing property to pass and confirm at least one previously passing case remains passing. Preserve raw outputs.

- [ ] **Step 4: Validate and commit**

Run the deterministic suite, repository validator, and plugin validator. Commit the correction and source-bound rerun evidence. If no Task 2 failure exists, make no commit and ledger the task as not required.

---

### Task 4: Package, install, and release verification

**Files:**
- Modify: `plugins/LEAPWare-status/.codex-plugin/plugin.json` through the cachebuster helper.
- Modify: `docs/validation.md`
- Create: `docs/evidence/release-2026-09-10.md`

**Interfaces:**
- Consumes: reviewed candidate, QA evidence, CI result, configured private marketplace `LEAPWare-Status`.
- Produces: exact release identity, installed hashes, fresh-task results, rollback instructions, and readiness verdict.

- [ ] **Step 1: Run independent source review**

Bind review to the exact base and head commits. Fix every important finding and rerun the affected checks before proceeding.

- [ ] **Step 2: Update the Codex cachebuster through the supported helper**

Run `update_plugin_cachebuster.py` against `plugins/LEAPWare-status`. Do not hand-edit marketplace configuration.

- [ ] **Step 3: Run every local gate and commit the candidate**

Run unittests, the repository validator, the bundled plugin validator, `git diff --check`, and confirm no required case was skipped. Update evidence with exact commands and results, then commit.

- [ ] **Step 4: Push the candidate and verify CI**

Push the reviewed branch, verify the GitHub Actions run for the exact commit passes, then integrate the reviewed commit into private `main` and verify `origin/main` matches.

- [ ] **Step 5: Reinstall and verify exact identity**

Run `codex plugin add LEAPWare-status@LEAPWare-Status`. Confirm installed and enabled status, and compare hashes for the manifest, skill, and UI metadata with private `main`.

- [ ] **Step 6: Validate in fresh Codex tasks**

Verify skill discovery, explicit `lw-status`, and ordinary status selection in fresh tasks. Save the raw results and limits; do not equate discovery with behavior.

- [ ] **Step 7: Final release gate and repository hygiene**

Confirm review, QA, CI, installed hashes, rollback instructions, commit, version, and private `main` all identify the same candidate. Tag the internal release only after the gate passes. Leave local and remote `main` equal and the working tree clean.
