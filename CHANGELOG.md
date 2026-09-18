# Changelog

All notable changes to this project are documented in this file. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning
follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- D0 recast: repository skeleton brought to parity with the sibling
  `lwt`/`lws` plugin repos — root meta files (`LICENSE`, `NOTICE`,
  `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`), the `.github/`
  set (`CODEOWNERS`, `dependabot.yml`, issue templates, PR template,
  rulesets, GitHub Apps, `ci.yml`/`handoff.yml`/`release.yml`), and the
  governance scripts under `scripts/lwp_check_*`. `ci.yml` replaces
  `validate.yml`. The pre-recast Codex package under
  `plugins/LEAPWare-Pulse/` stays in place and keeps working until D2.
  Learning is dropped from 1.0 (owner decision, 2026-09-17); see
  `docs/requirements/plan.md`.

## [0.2.0]

### Added

- Pre-recast Codex plugin: checklist parsing, evidence-gated verification,
  and the `Panorama` / `Brief` / `Focus` status views, released as a
  private Codex CLI plugin.

### Removed

- `docs/validation.md`, `docs/evidence/*.md`, and `docs/superpowers/`
  dropped from the tree ahead of publication: absolute local paths and
  private-era planning notes. Superseded by `proof/` and the
  traceability matrix; retained in git history.
