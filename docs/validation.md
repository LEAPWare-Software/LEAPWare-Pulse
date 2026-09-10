# Validation — 10 September 2026

This document supersedes the 9 September source-only summary. It separates evidence that is established for the reviewed source from release gates that remain unperformed for this local candidate.

## Established deterministic source validation

At reviewed evidence head `f17832fdca1bdd5efd6690c56c0abfd9473fe347`, the deterministic mutation suite ran 12 tests and all passed. The suite checks the real package plus mutations for manifest shape and identity, exact package inventory, full-plan and unknown-denominator handling, flooring rules, unchecked criteria, optional work outside totals, the authority boundary, and the default prompt.

The repository validator also passed:

```text
py -3.12 scripts/validate_status_plugin.py plugins/LEAPWare-status
```

It printed `LEAPWare-status validation passed`. The repository-root entry path passed as well. These checks verify source invariants; they do not establish that Codex has installed, discovered, or selected this local candidate.

## Established independent behavioral QA

The independent behavioral evidence is [behavioral-validation-2026-09-10.md](evidence/behavioral-validation-2026-09-10.md). The original seven fresh-context cases were preserved, including the initial `BHV-03` and `BHV-04` failures. The subsequent minimal source correction at `5a1be42c601322c0cb3a72acbecc4b9fd6f28d3b` received independent unchanged-case reruns for `BHV-03` and `BHV-04`, plus the selected `BHV-01` regression: all 38 evaluated properties passed, with no error, truncation, or skipped case within that three-case protocol.

This is behavioral evaluation of named source bytes, not a live plugin-discovery or installation test. `BHV-02` and `BHV-05` through `BHV-07` retain their original passing evidence and were not rerun against the corrected blob; the evidence states that limitation explicitly.

## Established source review

The project ledger records the Task 3 source review of `9083181..f17832f` as clean after the correction and rerun evidence. That review covers the correction/evidence range, not any future remote integration, installation, or fresh-task behavior.

## Current packaging state

The Phase A local candidate uses plugin version `0.1.0+codex.20260910194515`, produced by the supported plugin-creator cachebuster helper. No marketplace or Codex configuration was hand-edited. The accompanying release record binds the precise local evidence and lists remaining gates.

After packaging this candidate, Phase A reran the 12-test deterministic suite, repository validator, plugin-creator validator, and `git diff --check`; all exited 0. No deterministic test or requested behavioral rerun was skipped. Exact commands and output belong in the release record.

## Remote CI warning remediation

GitHub Actions run `34525323554` for exact reviewed head `ddf26ed` completed the 12-test suite, but GitHub emitted a Node.js 20 deprecation annotation because the workflow used `actions/checkout@v4` and `actions/setup-python@v5`. Treat that result as **RED** for this release gate: it is a pass-with-warning, not a clean CI pass. The workflow now uses `actions/checkout@v7` and `actions/setup-python@v7`; a new clean CI run for the final reviewed branch tip is still required and is not claimed here.

## Still pending — do not infer a pass

- Push the final reviewed branch tip and obtain a clean private GitHub Actions result for that exact SHA; the earlier `ddf26ed` pass-with-warning does not satisfy this gate.
- Review/integrate it into private `main` and verify `origin/main` identifies the same commit.
- Reinstall `LEAPWare-status@LEAPWare-Status`, verify installed/enabled state, and compare manifest, skill, and UI-metadata hashes with private `main`.
- In fresh Codex tasks, record skill discovery, explicit `lw-status`, and ordinary status-request selection/behavior.
- Perform the final release gate, then tag only if every identity and result agrees.

LEAPWare-continuity is uninstalled and inactive. This documentation and the SDD ledger are recovery records, not continuity-hook protection.
