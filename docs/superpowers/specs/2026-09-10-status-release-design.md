# LEAPWare Status Private Release Design

## Goal

Prove that LEAPWare-status is tested, independently vetted, privately released, and installed in Codex for authorized LEAPWare use.

## Scope and authority

The GitHub repository remains private. Work may be committed and pushed to `main`, and the local Codex plugin may be reinstalled from the configured private local marketplace. No public publication, force-push, history rewrite, unrelated repository change, or external marketplace submission is allowed.

## Acceptance gates

1. **Deterministic validation:** A repeatable local and CI check validates the manifest, package inventory, UI metadata, reporting contract, percentage rules, authority limits, and absence of undeclared runtime capabilities. Mutation tests prove that the validator rejects material defects.
2. **Behavioral QA:** Independent agents exercise realistic full-plan, partial, unknown-denominator, scope-change, failed/unverified, evidence-drift, and authority-boundary scenarios. Raw prompts, outputs, source identity, and verdicts are retained. Any observed failure becomes the failing test for a narrow skill correction and rerun.
3. **Independent review:** A reviewer who did not implement the changes checks the exact source diff against this design and reports reproducible findings. Important findings are fixed and re-reviewed.
4. **Runtime validation:** The exact reviewed plugin is installed through the supported Codex local-marketplace flow. A fresh Codex task verifies discovery and explicit `lw-status` use; an ordinary status request verifies automatic selection when evidence permits.
5. **Release verification:** Review, QA, CI, installed hashes, rollback instructions, commit, tag, and `main` all identify the same candidate. No required test is skipped and no important finding remains.
6. **Repository hygiene:** The accepted work is on private `main`; local `main` and `origin/main` match; the working tree is clean.

## Continuity and recovery

LEAPWare-continuity is uninstalled and provides no protection. A manual ledger records the plan identity, source commits, test and review evidence, uncertain external effects, and exact next action before and after each gate. After interruption or compaction, execution resumes only after reconciling the ledger with Git and Codex state. This reduces risk but is not an absolute continuity guarantee.

## Rollback

Retain the prior plugin version and source commit. If the new installation fails, reinstall the prior version from the private marketplace and verify its cached files against that commit. Never overwrite or delete unrelated work.

