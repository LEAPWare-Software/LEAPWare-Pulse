# Security Policy

## Reporting a vulnerability

Please report a suspected vulnerability privately via GitHub's
["Report a vulnerability"](https://github.com/LEAPWare-Software/LEAPWare-Pulse/security/advisories/new)
flow on this repository (once published), rather than a public issue. If
that is not available yet, open an issue with the security-sensitive
details omitted and a maintainer will follow up privately.

Include, where possible:

- The affected file(s) or plugin (`plugins/claude/lwp` or `plugins/codex/lwp`).
- Whether the issue is in the pure engine (`core/`), an adapter, or a
  plugin's own script.
- Reproduction steps and, if relevant, which view (Panorama, Brief, Focus)
  is affected.

## Scope notes

- `core/` and `adapters/` do no I/O beyond what the report and evidence
  flows require; a report there is most likely about a verification rule
  (a status reported as verified that should not be, or vice versa).
- Neither plugin registers hooks, MCP servers, apps or background agents;
  reports assuming one does are out of scope.
- A status request from either plugin authorizes no fix, install, commit
  or deployment; reports assuming otherwise are out of scope.

## Supported versions

Pre-1.0: only the latest tagged release receives fixes.
