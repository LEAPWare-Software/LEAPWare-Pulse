# Session carryover — detail that doesn't fit HANDOFF.md's 3000-byte cap

Read `HANDOFF.md` first. This is the long-form backing for its "Blocker"
and "In flight" sections, plus D0 limitations a next session should
know about before touching the affected code.

## The `lwp-lanes` blocker, in full

CI job `lwp-lanes` runs `scripts/lwp_lanes.py`. Bootstrap exception:
`BOOTSTRAP_LAST_EXEMPT_PR = 5` — enforcement is a no-op for PR numbers
1-5 (`check_lanes`: `if pr_number <= BOOTSTRAP_LAST_EXEMPT_PR: return []`).
PR #6 is the first PR the check actually enforces, and it is the PR
carrying this very handoff rewrite.

**What triggers a review requirement.** For each commit in the PR's
range, `check_lanes` reads the `LWP-Agent:` trailer via `commit_agent`.
A commit trailered `human` is skipped entirely:
```python
if agent == "human":
    continue  # the owner's own commits are unrestricted
```
That is a genuine bypass in the code — but it exists for the owner's
own commits, not for a CLI session to self-declare `human` and dodge
review; doing so would misrepresent authorship, not satisfy the gate's
intent. For `claude`/`codex` commits, every touched file is classified
by `classify_path`; if any file classifies `shared`, both reviews are
required:
```python
if touches_shared:
    _review_ok(pr_number, "claude", sha, errors)
    _review_ok(pr_number, "codex", sha, errors)
```
PR #6's only commit (`690eab6`) is trailered `LWP-Agent: claude` and
touches `docs/requirements/plan.md`, `docs/github-apps.md`, and
`HANDOFF.md` — all `shared` by `SHARED_PREFIXES`/`SHARED_FILES`. So both
`reviews/6/claude-cto.json` and `reviews/6/codex-cto.json` are required.

**Exact required shape** (`reviews/schema.json`, `reviews/README.md`),
one file per agent, filename `reviews/<pr>/<agent>-cto.json`:
```json
{
  "pr": 6,
  "reviewer_agent": "claude",
  "reviewer_id": "<free-form id, must differ from commit_author_id>",
  "commit_author_agent": "claude",
  "commit_author_id": "<free-form id>",
  "verdict": "AGREE",
  "notes": "optional"
}
```
`_review_ok` checks: file exists; valid JSON; `verdict == "AGREE"`;
`reviewer_agent` matches the filename's agent; `reviewer_id` and
`commit_author_id` both present and **not equal by literal string
comparison** — the check does not derive identity from git authorship
at all, `reviewer_id`/`commit_author_id` are free-form strings supplied
inside the JSON itself, checked only for self-declared inequality.

**Is this a hard blocker or a misunderstanding?** Structurally, nothing
in `lwp_lanes.py` cryptographically ties a review record to an actual
second CLI session — it only checks JSON field shape and string
inequality. That means the check *could* technically be satisfied by
one session writing both files. It must not be, for two reasons: (1)
the design intent stated in the module docstring is an actual
adversarial second opinion ("the CTO/CIO role on each CLI adversarially
checks and agrees"), and (2) this session was explicitly instructed not
to fabricate a review record or invent a reviewer identity. So this is
a genuine process blocker, not a code defect: resolving it requires a
real, independent Codex session to write `reviews/6/codex-cto.json`
(and this Claude session, or another independent Claude session, to
write `reviews/6/claude-cto.json`).

**Resolution options for PR #6:**
1. Run an actual independent Codex CTO-role session against `690eab6`,
   have it write `reviews/6/codex-cto.json` with a genuine `AGREE`/
   `DISAGREE` verdict, and have an independent Claude session (not the
   one that authored the commit) write `reviews/6/claude-cto.json`.
2. Have the owner commit the fix directly with `LWP-Agent: human` (or
   re-author the change as an owner commit) — bypasses review lawfully
   since it's a real human commit, not a spoofed one.
3. Raise `BOOTSTRAP_LAST_EXEMPT_PR` from `5` to `6` — an owner decision,
   since it edits `scripts/lwp_lanes.py` itself (a shared path) and
   changes what the gate enforces going forward, not a routine fix.

## G-PUB status

| Item | State |
|---|---|
| Visibility | PUBLIC since 2026-09-18 |
| Ruleset `23672521` | Active, empty `bypass_actors`, 6 required checks match CI |
| Auto-merge | Enabled |
| `lwp-claude` / `lwp-codex` Apps | NOT created — procedure in `docs/github-apps.md` |
| Merge-queue probe | NEVER run — "merges work end to end" is UNPROVEN |

## D0 known limitations (carried forward, not yet fixed)

- `lwp_check_env_leak.py`: spaced-join false positives possible (a
  leaked token split across tokens/lines with intervening whitespace
  can evade detection).
- Same scanner: a secret split across three or more lines is a known
  gap — only adjacent-pair joins are checked.
- The placeholder guard (distinguishing a real secret from a
  placeholder/example value) is heuristic, not exact; treat its
  negatives as "probably fine," not "proven fine."
- `proof/LWP-D0.json` is a **sealed** record of D0's proof at merge
  time. Never edit it to reflect later reality (e.g. publication,
  ruleset changes) — it is a historical attestation, not a live status
  file. Live status belongs in `HANDOFF.md`'s generated block.
