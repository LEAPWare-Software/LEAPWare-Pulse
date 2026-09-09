# LEAPWare Status

Concise checklist progress reporting that keeps the full agreed plan visible: complete, in progress, next, remaining, blocked and unverified work.

Use `lw-status` in a task or select the LEAPWare-status skill. The phrase is not a shell command. The skill also supports ordinary status requests, progress updates and handoffs through automatic skill selection.

This dedicated repository belongs to LEAPWare-Software. The Codex plugin contains one self-contained skill; it adds no hooks, MCP servers, scheduled jobs or background agents. Reporting does not change task authorization or replace a continuity record.

## Install

Register this repository with `codex plugin marketplace add <repository-root>`, then run `codex plugin add LEAPWare-status@LEAPWare-Status`. Check selection in a fresh task after installation.

## Reporting contract

Keep the entire committed plan in milestone order, including completed work. Check a box only when its stated outcome has evidence. Keep partial, blocked, failed or unverified work unchecked. Preserve owner corrections, material gates and the exact next action. Separate optional proposals from approved work. Prefer a brief checklist over a narrative activity log.

Source: `plugins/LEAPWare-status/skills/LEAPWare-status/SKILL.md`.
