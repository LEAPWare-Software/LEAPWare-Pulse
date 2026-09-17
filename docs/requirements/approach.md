# Requirements approach for lwp 1.0.0

How `owner-directives.md` becomes a shipped, proven lwp 1.0.0. Same order
as the sibling repos: evidence before drafting, an adversarial audit before
owner decisions, a freeze after that.

## Steps

1. **Evidence.** Measured baseline of the pre-recast package (below) and,
   in D4, the Claude-vs-Codex capability matrix — every row backed by a doc
   link or a command run against the real CLI, never recollection.
2. **Draft.** `requirements.md` (this package) and `plan.md`.
3. **Adversarial audit.** A verifier that did not draft checks each
   requirement against its directive and each acceptance test against its
   requirement. Blockers only, one round.
4. **Apply findings.**
5. **Owner decisions.** The open questions in `plan.md`, answered by the
   owner and recorded there with the answer, not just the question.
6. **Freeze.** After freeze a requirement ID never changes meaning; a
   correction is a new ID or an explicit amendment line.

## Measured baseline (pre-recast `main`, 9e8b9a8)

- Tracked files: 33; tracked bytes: 247,866.
- Shipped Codex plugin (`plugins/LEAPWare-Pulse/**`): 15 files, 95,732 bytes.
- Tests: 5 `unittest` modules, 42 test methods (`grep -c "def test"`),
  plus two Markdown behavioral scenario matrices.
- CI: one workflow, `windows-latest`, Python 3.12 only.
- Commit identity on all 24 commits: the legacy `LEAPWare-HQ` identity.
- Hooks, MCP servers, apps registered by the plugin: none.

Re-measure before quoting any of these after D0.

## Proof bar (directive 5)

A requirement is proven only when all of these exist:

- an automated acceptance test named in `requirements.md`;
- a recorded run of that test failing after the rule is broken on purpose
  (the "break" line of the requirement), then passing after it is restored;
- a row in the traceability matrix (LWP-R12);
- inclusion in a phase proof record `proof/LWP-Dn.json` whose `checked_by`
  differs from its `author`.

The release additionally needs the rehearsal (LWP-R37) and an independent
final proof record (LWP-R38).
