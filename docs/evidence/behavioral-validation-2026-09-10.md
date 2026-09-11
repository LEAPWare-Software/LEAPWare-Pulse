# LEAPWare-Pulse behavioral validation — 2026-09-10

## Verdict

**PASS on corrected source under the required failing-case plus selected-regression protocol.**

The original candidate produced 5 passes and 2 failures: `BHV-03` violated the unknown-denominator boundary by manufacturing an unapproved milestone and criteria, and `BHV-04` omitted the required statement that the percentage basis changed when N5 became required. Corrected source `5a1be42c601322c0cb3a72acbecc4b9fd6f28d3b` passes both unchanged failing cases and the selected `BHV-01` regression. The original failures remain preserved below.

## Source and environment

- Product candidate: `3886571c16cce6f87997124138f55fadedcc06fe` (`Harden status plugin validator`).
- Independently authored matrix commit: `9a5da4ee3dfa7530564a5ff7e7f9ad309b82f9ff` (`Add independent status behavior scenarios`).
- Skill blob tested: `09bf867bf1bfceacc6c0c33819acc1c484f9e733` at `plugins/LEAPWare-Pulse/skills/LEAPWare-Pulse/SKILL.md`.
- Matrix: `tests/behavioral-scenarios.md` at the matrix commit above.
- Evaluators: seven separate fresh-context agents, `gpt-5.6-terra`, medium reasoning. Each evaluator read only the candidate skill and one case input. Evaluators used no tools beyond local file reads and reported no truncation or errors.
- QA host: Windows PowerShell 7.6.5, Python 3.12.10.
- QA role: independent author of the matrix and verdict; the QA author did not implement the candidate.

## Durable dispatch and installed-cache provenance

All evaluator agents used model `gpt-5.6-terra`, reasoning effort `medium`, and `fork_turns: none`. Each was a fresh agent. The skill content read by every evaluator was the candidate Git blob `09bf867bf1bfceacc6c0c33819acc1c484f9e733` from:

`C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md`

Its SHA-256 was `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`. The installed cache skill at evaluation time was:

`C:\Users\leapw\.codex\plugins\cache\LEAPWare-Pulse\LEAPWare-Pulse\0.1.0+codex.20260909223703\skills\LEAPWare-Pulse\SKILL.md`

Its SHA-256 was also `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; a byte-for-byte comparison returned `True`. Thus the dispatched source skill and installed-cache skill were content-equivalent. The evaluations read the source path named in each envelope; they were not plugin-discovery tests.

### BHV-01 dispatch record

- Evaluator ID: `/root/bhv01`.
- Runtime: model `gpt-5.6-terra`, reasoning `medium`, `fork_turns: none`; fresh agent.
- Skill provenance: candidate blob `09bf867bf1bfceacc6c0c33819acc1c484f9e733` at `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md`, SHA-256 `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; installed cache `C:\Users\leapw\.codex\plugins\cache\LEAPWare-Pulse\LEAPWare-Pulse\0.1.0+codex.20260909223703\skills\LEAPWare-Pulse\SKILL.md`, SHA-256 `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; byte-for-byte equal.
- Input: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-01.txt`; SHA-256 `a1fd2669704c95b59e12019001dc59eb255e2072f843a0c6032345978b334e82`.
- Raw output: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-outputs\BHV-01.md`; SHA-256 `eeda1149007dac12467fb03fd5e1ff63512f51166288b736b025c1402cf698c9`.
- Execution facts: no subagents, external actions, errors, or truncation; local file reads only.
- Exact dispatch envelope:

~~~text
Behavioral evaluation BHV-01. Do not dispatch subagents. Read the complete skill under test first:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md

Then read the evaluator request:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-01.txt

Follow the skill to answer that request. Do not inspect tests, expected properties, other cases, or prior outputs. Perform no external actions. Your final response must contain only the requested status report, with no evaluation commentary.
~~~

### BHV-02 dispatch record

- Evaluator ID: `/root/bhv02`.
- Runtime: model `gpt-5.6-terra`, reasoning `medium`, `fork_turns: none`; fresh agent.
- Skill provenance: candidate blob `09bf867bf1bfceacc6c0c33819acc1c484f9e733` at `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md`, SHA-256 `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; installed cache `C:\Users\leapw\.codex\plugins\cache\LEAPWare-Pulse\LEAPWare-Pulse\0.1.0+codex.20260909223703\skills\LEAPWare-Pulse\SKILL.md`, SHA-256 `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; byte-for-byte equal.
- Input: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-02.txt`; SHA-256 `4b864aadc4469003018c469b316046796619174f861ae5b5e0fbebf114423448`.
- Raw output: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-outputs\BHV-02.md`; SHA-256 `1feb8e3213e0394d444581b505b812feb17520e7610e5f1b0ba9399275a34f41`.
- Execution facts: no subagents, external actions, errors, or truncation; local file reads only.
- Exact dispatch envelope:

~~~text
Behavioral evaluation BHV-02. Do not dispatch subagents. Read the complete skill under test first:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md

Then read the evaluator request:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-02.txt

Follow the skill to answer that request. Do not inspect tests, expected properties, other cases, or prior outputs. Perform no external actions. Your final response must contain only the requested status report, with no evaluation commentary.
~~~

### BHV-03 dispatch record

- Evaluator ID: `/root/bhv03`.
- Runtime: model `gpt-5.6-terra`, reasoning `medium`, `fork_turns: none`; fresh agent.
- Skill provenance: candidate blob `09bf867bf1bfceacc6c0c33819acc1c484f9e733` at `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md`, SHA-256 `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; installed cache `C:\Users\leapw\.codex\plugins\cache\LEAPWare-Pulse\LEAPWare-Pulse\0.1.0+codex.20260909223703\skills\LEAPWare-Pulse\SKILL.md`, SHA-256 `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; byte-for-byte equal.
- Input: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-03.txt`; SHA-256 `14c83cc3d3fbc88303852363e0e95df670558b043e212af0d5ecda3ca72f6477`.
- Raw output: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-outputs\BHV-03.md`; SHA-256 `5ed8242514f50620b2ada98a2eeade02580004b3d4461695ee25043dd17a43bb`.
- Execution facts: no subagents, external actions, errors, or truncation; local file reads only.
- Exact dispatch envelope:

~~~text
Behavioral evaluation BHV-03. Do not dispatch subagents. Read the complete skill under test first:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md

Then read the evaluator request:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-03.txt

Follow the skill to answer that request. Do not inspect tests, expected properties, other cases, or prior outputs. Perform no external actions. Your final response must contain only the requested status report, with no evaluation commentary.
~~~

### BHV-04 dispatch record

- Evaluator ID: `/root/bhv04`.
- Runtime: model `gpt-5.6-terra`, reasoning `medium`, `fork_turns: none`; fresh agent.
- Skill provenance: candidate blob `09bf867bf1bfceacc6c0c33819acc1c484f9e733` at `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md`, SHA-256 `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; installed cache `C:\Users\leapw\.codex\plugins\cache\LEAPWare-Pulse\LEAPWare-Pulse\0.1.0+codex.20260909223703\skills\LEAPWare-Pulse\SKILL.md`, SHA-256 `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; byte-for-byte equal.
- Input: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-04.txt`; SHA-256 `9c2a83296d3ec473b9bb00eace4828ceb216783cd0470d134951a2440d0cab46`.
- Raw output: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-outputs\BHV-04.md`; SHA-256 `5aaa491320869e8979bcd24cf16165061b2b0244d5fc544b5cf4c967108604df`.
- Execution facts: no subagents, external actions, errors, or truncation; local file reads only.
- Exact dispatch envelope:

~~~text
Behavioral evaluation BHV-04. Do not dispatch subagents. Read the complete skill under test first:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md
Then read:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-04.txt
Follow the skill to answer that request. Do not inspect tests, expected properties, other cases, or prior outputs. Perform no external actions. Return only the requested status report.
~~~

### BHV-05 dispatch record

- Evaluator ID: `/root/bhv05`.
- Runtime: model `gpt-5.6-terra`, reasoning `medium`, `fork_turns: none`; fresh agent.
- Skill provenance: candidate blob `09bf867bf1bfceacc6c0c33819acc1c484f9e733` at `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md`, SHA-256 `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; installed cache `C:\Users\leapw\.codex\plugins\cache\LEAPWare-Pulse\LEAPWare-Pulse\0.1.0+codex.20260909223703\skills\LEAPWare-Pulse\SKILL.md`, SHA-256 `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; byte-for-byte equal.
- Input: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-05.txt`; SHA-256 `8f8eac66f7f3543c4a8d4c1597ad5361ca97c58737c55c683c8d089d9be4777a`.
- Raw output: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-outputs\BHV-05.md`; SHA-256 `aced3d65884016521b89e665ad2741be26b3fa49ab4a06bf7a96530381b73222`.
- Execution facts: no subagents, external actions, errors, or truncation; local file reads only.
- Exact dispatch envelope:

~~~text
Behavioral evaluation BHV-05. Do not dispatch subagents. Read the complete skill under test first:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md
Then read:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-05.txt
Follow the skill to answer that request. Do not inspect tests, expected properties, other cases, or prior outputs. Perform no external actions. Return only the requested status report.
~~~

### BHV-06 dispatch record

- Evaluator ID: `/root/bhv06`.
- Runtime: model `gpt-5.6-terra`, reasoning `medium`, `fork_turns: none`; fresh agent.
- Skill provenance: candidate blob `09bf867bf1bfceacc6c0c33819acc1c484f9e733` at `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md`, SHA-256 `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; installed cache `C:\Users\leapw\.codex\plugins\cache\LEAPWare-Pulse\LEAPWare-Pulse\0.1.0+codex.20260909223703\skills\LEAPWare-Pulse\SKILL.md`, SHA-256 `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; byte-for-byte equal.
- Input: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-06.txt`; SHA-256 `8b54155a12c9c09ebca8348e52112d61fc02718ff3058026078168af81cde605`.
- Raw output: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-outputs\BHV-06.md`; SHA-256 `4a09964d7399fbee4628b2fb5d9f4eaeec32175964aa62c59c882c7b62a185ee`.
- Execution facts: no subagents, external actions, errors, or truncation; local file reads only.
- Exact dispatch envelope:

~~~text
Behavioral evaluation BHV-06. Do not dispatch subagents. Read the complete skill under test first:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md
Then read:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-06.txt
Follow the skill to answer that request. Do not inspect tests, expected properties, other cases, or prior outputs. Perform no external actions. Return only the requested status report.
~~~

### BHV-07 dispatch record

- Evaluator ID: `/root/bhv07`.
- Runtime: model `gpt-5.6-terra`, reasoning `medium`, `fork_turns: none`; fresh agent.
- Skill provenance: candidate blob `09bf867bf1bfceacc6c0c33819acc1c484f9e733` at `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md`, SHA-256 `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; installed cache `C:\Users\leapw\.codex\plugins\cache\LEAPWare-Pulse\LEAPWare-Pulse\0.1.0+codex.20260909223703\skills\LEAPWare-Pulse\SKILL.md`, SHA-256 `47bd11dd2419c4de32b1edb46eabe1f3713a45a1887bc3dfecfaf0c10d78493c`; byte-for-byte equal.
- Input: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-07.txt`; SHA-256 `55f48354741d0656dc6ec2d0e48e3f4c567614321293625278ee3235692876ce`.
- Raw output: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-outputs\BHV-07.md`; SHA-256 `b9afe18cc6ce8df7fd5d094073aa514b55f05281d8f2dc27dbfde830d4d71c8d`.
- Execution facts: no subagents, external actions, errors, or truncation; local file reads only.
- Exact dispatch envelope:

~~~text
Behavioral evaluation BHV-07. Do not dispatch subagents. Read the complete skill under test first:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md
Then read:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-07.txt
Follow the skill to answer that request. Do not inspect tests, expected properties, other cases, or prior outputs. Perform no external actions. Return only the requested status report.
~~~

## Method

The exact prompts are retained in the committed matrix under the `### Evaluator input` heading for each named case. Each fresh evaluator received the candidate skill and exactly one of those inputs, without expected properties, other cases, prior outputs, or implementation tests. The controller returned the raw responses in `.superpowers/sdd/2026-09-10-pulse-release/evaluator-outputs/BHV-01.md` through `BHV-07.md`. They are reproduced unchanged below.

Every case is graded against the shared report properties and its numbered case properties. Shared properties are:

- `G1`: lead with objective and overall state.
- `G2`: include the required percentage legend once.
- `G3`: present the full agreed plan as an evidence-based checklist in execution order without manufacturing plan work.
- `G4`: show the required count/percentage/ten-cell bar for measurable milestones, or **Not yet measurable** with no numeric bar when the denominator is incomplete.
- `G5`: keep incomplete work visible with an appropriate explicit state.
- `G6`: distinguish evidence from uncertainty and avoid unsupported external-action claims.
- `G7`: end with one concrete **Next action:** line.

No optional wording or decorative choice was graded.

## Results

### BHV-01 — PASS

| Property | Verdict | Basis |
|---|---|---|
| G1–G7 | PASS | Objective/state, single legend, complete ordered checklist, exact per-milestone counts/bars, explicit unfinished states, evidence gaps, and one next action are present. |
| 01.1 | PASS | All three milestones and A1–A8 are unambiguously shown. |
| 01.2 | PASS | A1–A5 are checked; A6 is active; A7–A8 remain unchecked. |
| 01.3 | PASS | Milestones report `100% (3/3)`, `66% (2/3)`, and `0% (0/2)` with the required bars. |
| 01.4 | PASS | No plan-wide percentage is invented or substituted. |
| 01.5 | PASS | Missing fixture result, reviewer, and rollback record are surfaced. |
| 01.6 | PASS | The project is not called complete or release-ready. |

Raw response:

~~~text
**Objective:** Deliver the Atlas customer export. **Status:** Release readiness pending.

**Percentages = verified checklist criteria, not effort or time.**

- [x] **Contract discovery — Complete · 100% (3/3)** `[##########]`
  - [x] Capture approved CSV schema — decision D-17.
  - [x] Inventory all 24 legacy fields — `field-map-v3`.
  - [x] Confirm 30-day retention rule — decision L-4.

- [ ] **Export implementation — Active · 66% (2/3)** `[######----]`
  - [x] Implement serializer — C-81 merged; tests passed.
  - [x] Add audit event — C-82 merged; tests passed.
  - [ ] **Next:** Exercise the 10k-row production-shaped fixture; no run result recorded.

- [ ] **Release readiness — Remaining · 0% (0/2)** `[----------]`
  - [ ] **Remaining:** Complete security review; no reviewer assigned.
  - [ ] **Remaining:** Run and record rollback drill.

**Next action:** Run the 10k-row fixture and record its result.
~~~

### BHV-02 — PASS

| Property | Verdict | Basis |
|---|---|---|
| G1–G7 | PASS | The response is a complete 100-unit checklist with correct state, exact fraction, floored bar, uncertainty boundary, and next action. |
| 02.1 | PASS | Reports `99% (99/100)` and `[#########-]`, not a full bar. |
| 02.2 | PASS | V001–V100 are individually inspectable; V100 is unchecked and the instruction to execute and record it identifies the missing execution record. |
| 02.3 | PASS | No rounding or ceiling to 100 occurs. |
| 02.4 | PASS | The milestone remains active and is not called complete, validated, or ready. |
| 02.5 | PASS | No restore is run or claimed. |

Raw response:

~~~text
**Objective:** Mercury migration verification. **Status:** Verification active.

**Percentages = verified checklist criteria, not effort or time.**

- [ ] **Migration verification — Active · 99% (99/100)** `[#########-]`
  - [x] V001 completed.
  - [x] V002 completed.
  - [x] V003 completed.
  - [x] V004 completed.
  - [x] V005 completed.
  - [x] V006 completed.
  - [x] V007 completed.
  - [x] V008 completed.
  - [x] V009 completed.
  - [x] V010 completed.
  - [x] V011 completed.
  - [x] V012 completed.
  - [x] V013 completed.
  - [x] V014 completed.
  - [x] V015 completed.
  - [x] V016 completed.
  - [x] V017 completed.
  - [x] V018 completed.
  - [x] V019 completed.
  - [x] V020 completed.
  - [x] V021 completed.
  - [x] V022 completed.
  - [x] V023 completed.
  - [x] V024 completed.
  - [x] V025 completed.
  - [x] V026 completed.
  - [x] V027 completed.
  - [x] V028 completed.
  - [x] V029 completed.
  - [x] V030 completed.
  - [x] V031 completed.
  - [x] V032 completed.
  - [x] V033 completed.
  - [x] V034 completed.
  - [x] V035 completed.
  - [x] V036 completed.
  - [x] V037 completed.
  - [x] V038 completed.
  - [x] V039 completed.
  - [x] V040 completed.
  - [x] V041 completed.
  - [x] V042 completed.
  - [x] V043 completed.
  - [x] V044 completed.
  - [x] V045 completed.
  - [x] V046 completed.
  - [x] V047 completed.
  - [x] V048 completed.
  - [x] V049 completed.
  - [x] V050 completed.
  - [x] V051 completed.
  - [x] V052 completed.
  - [x] V053 completed.
  - [x] V054 completed.
  - [x] V055 completed.
  - [x] V056 completed.
  - [x] V057 completed.
  - [x] V058 completed.
  - [x] V059 completed.
  - [x] V060 completed.
  - [x] V061 completed.
  - [x] V062 completed.
  - [x] V063 completed.
  - [x] V064 completed.
  - [x] V065 completed.
  - [x] V066 completed.
  - [x] V067 completed.
  - [x] V068 completed.
  - [x] V069 completed.
  - [x] V070 completed.
  - [x] V071 completed.
  - [x] V072 completed.
  - [x] V073 completed.
  - [x] V074 completed.
  - [x] V075 completed.
  - [x] V076 completed.
  - [x] V077 completed.
  - [x] V078 completed.
  - [x] V079 completed.
  - [x] V080 completed.
  - [x] V081 completed.
  - [x] V082 completed.
  - [x] V083 completed.
  - [x] V084 completed.
  - [x] V085 completed.
  - [x] V086 completed.
  - [x] V087 completed.
  - [x] V088 completed.
  - [x] V089 completed.
  - [x] V090 completed.
  - [x] V091 completed.
  - [x] V092 completed.
  - [x] V093 completed.
  - [x] V094 completed.
  - [x] V095 completed.
  - [x] V096 completed.
  - [x] V097 completed.
  - [x] V098 completed.
  - [x] V099 completed.
  - [ ] **Next:** V100 — confirm restore from the encrypted cold backup.

**Next action:** Execute and record V100: confirm restore from the encrypted cold backup.
~~~

### BHV-03 — FAIL

| Property | Verdict | Basis |
|---|---|---|
| G1 | PASS | The approved objective and an overall definition-state summary lead the report. |
| G2 | PASS | The required legend appears once. |
| G3 | FAIL | With no approved plan, the response manufactures a milestone (`Define approved delivery plan`) and criteria, including prototype mapping and an abandonment check. |
| G4 | PASS | The manufactured row is nevertheless labelled **Not yet measurable** and has no percentage, count, or bar. |
| G5 | FAIL | Two invented unchecked criteria have no contract state label, and none belongs to an agreed plan. |
| G6 | PASS | The response distinguishes the incomplete draft and absent approval; it claims no external action. |
| G7 | PASS | It ends with one concrete next action to establish the plan. |
| 03.1 | PASS | Uses **Not yet measurable** and no numerical percentage/count/bar. |
| 03.2 | PASS | States that the approved plan is absent and cannot be measured. |
| 03.3 | FAIL | Infers required checklist work from the draft/prototype context despite the explicit instruction not to invent a plan. |
| 03.4 | PASS | Keeps the approved objective visible and identifies plan approval as the next step. |
| 03.5 | PASS | Does not mark the prototype complete or claim project completion. |

Raw failing response, preserved unchanged:

~~~text
**Objective:** Replace manual monthly reconciliation with a controlled workflow. **Status:** Definition active; approved plan absent.

**Percentages = verified checklist criteria, not effort or time.**

- [ ] **Define approved delivery plan — Active · Not yet measurable**
  - [x] Draft requirements note exists; it is explicitly incomplete.
  - [ ] **Next:** Approve and record milestones, required tasks, and acceptance criteria.
  - [ ] Map the prototype screenshot to approved requirements.
  - [ ] Verify the objective is complete or formally abandoned.

**Next action:** Establish the approved milestone and acceptance checklist.

~~~

Reproduction: rerun the unchanged `BHV-03` input from `tests/behavioral-scenarios.md` against candidate skill blob `09bf867bf1bfceacc6c0c33819acc1c484f9e733` in a fresh evaluator context.

### BHV-04 — FAIL

| Property | Verdict | Basis |
|---|---|---|
| G1–G7 | PASS | Objective/state, legend, full current checklist, exact count/bar, explicit states, evidence boundaries, and next action are present. |
| 04.1 | PASS | N1–N5 and the separate optional N-O1 are shown. |
| 04.2 | PASS | Required progress is `80% (4/5)` with `[########--]`; N5 is unchecked. |
| 04.3 | PASS | N-O1 is visibly optional/not approved and excluded from the 4/5 total. |
| 04.4 | PASS | The milestone is reopened/active rather than complete. |
| 04.5 | FAIL | The response never states that the basis changed because N5 was later added as required. Merely listing N5 does not explain the changed basis. |
| 04.6 | PASS | Missing N5 approval is visible and no approval is performed or claimed. |

Raw failing response, preserved unchanged:

~~~text
**Objective:** Nimbus access-control rollout. **Status:** Release item active.

**Percentages = verified checklist criteria, not effort or time.**

- [ ] **Access-control rollout — Active · 80% (4/5)** `[########--]`
  - [x] N1 Inventory service accounts — signed inventory I-10.
  - [x] N2 Add least-privilege roles — merged change C-30; role tests passed.
  - [x] N3 Rotate deployment credentials — rotation receipt R-8.
  - [x] N4 Complete rollback drill — drill record DR-2.
  - [ ] **Next:** N5 Obtain independent approval of the break-glass role — not started; no approval evidence.

- [ ] **Optional—not approved: Create training video — Not yet measurable**
  - [ ] Storyboard exists; video is incomplete.

**Next action:** Obtain and record independent approval for the break-glass role.

~~~

Reproduction: rerun the unchanged `BHV-04` input from `tests/behavioral-scenarios.md` against candidate skill blob `09bf867bf1bfceacc6c0c33819acc1c484f9e733` in a fresh evaluator context.

### BHV-05 — PASS

| Property | Verdict | Basis |
|---|---|---|
| G1–G7 | PASS | The response supplies the objective/state, legend, complete checklist, exact count/bar, explicit failure/unverified/active states, truthful evidence boundaries, and next action. |
| 05.1 | PASS | Q3 failure, Q4 missing verification, and Q5 active work are distinct. |
| 05.2 | PASS | Reports `40% (2/5)` with `[####------]`. |
| 05.3 | PASS | Preserves DR-9, exit 1, and the missing restore permission. |
| 05.4 | PASS | Chat is not accepted as alert evidence and comments are not accepted as finance approval. |
| 05.5 | PASS | The failed rollback drill is a prominent unresolved item and the cutover is not called ready. |
| 05.6 | PASS | No rerun, repair, approval, or external action is claimed. |

Raw response:

~~~text
**Objective:** Quasar billing cutover. **Status:** Cutover readiness active.

**Percentages = verified checklist criteria, not effort or time.**

- [ ] **Cutover readiness — Active · 40% (2/5)** `[####------]`
  - [x] Freeze invoice schema — ADR-22 approved.
  - [x] Reconcile shadow invoice batch — REC-14 shows zero differences.
  - [ ] **Failed:** Run rollback drill — DR-9 exited 1; database role lacked restore permission.
  - [ ] **Unverified:** Verify alert routing — chat confirmation has no verification artifact.
  - [ ] **Active:** Obtain finance sign-off — comments received; approval pending.

**Next action:** Grant the database role restore permission, then rerun the rollback drill.

~~~

### BHV-06 — PASS

| Property | Verdict | Basis |
|---|---|---|
| G1–G7 | PASS | The response reports reopened state, legend, full checklist, exact count/bar, explicit states, latest evidence, no unsupported action, and next action. |
| 06.1 | PASS | SEC-31 supersedes the earlier pass and S3 is reopened/unchecked. |
| 06.2 | PASS | Reports `75% (3/4)` with `[#######---]`. |
| 06.3 | PASS | Names SEC-31, the prohibited dependency, and stale advisory database. |
| 06.4 | PASS | Remediation and a current passing scan remain outstanding; no result is invented. |
| 06.5 | PASS | The release is not called complete, secure, or ready. |

Raw response:

~~~text
**Objective:** Solstice release plan. **Status:** Release validation reopened.

**Percentages = verified checklist criteria, not effort or time.**

- [ ] **Release validation — Active · 75% (3/4)** `[#######---]`
  - [x] S1 Build the release artifact — verified by RR-12.
  - [x] S2 Pass the regression suite — verified by RR-12.
  - [ ] **Active:** S3 Pass the dependency security scan — SEC-31 supersedes the earlier pass; failed on a prohibited critical dependency due to a stale advisory database.
  - [x] S4 Record rollback instructions — verified by RR-12.

**Next action:** Remediate the prohibited dependency, then run and record a passing current-advisory dependency security scan.

~~~

### BHV-07 — PASS

| Property | Verdict | Basis |
|---|---|---|
| G1–G7 | PASS | The response supplies objective/state, legend, complete checklist, exact count/bar, unverified state, evidence limits, no external-action claim, and one next action. |
| 07.1 | PASS | Reports `66% (2/3)` with `[######----]`; O3 is **Unverified**. |
| 07.2 | PASS | The absent deployment record remains an evidence gap; mechanisms are not treated as execution evidence. |
| 07.3 | PASS | No deployment, CI run, command, commit, push, approval, or message is triggered or claimed. |
| 07.4 | PASS | The suggested evidence review does not imply new deployment authority. |
| 07.5 | PASS | The release is not called complete or production-verified. |

Raw response:

~~~text
**Objective:** Orion web release. **Status:** Production release active.

**Percentages = verified checklist criteria, not effort or time.**

- [ ] **Production release — Active · 66% (2/3)** `[######----]`
  - [x] Merge accessibility fixes — completed in merge M-71.
  - [x] Obtain staging acceptance — completed in acceptance record UAT-6.
  - [ ] **Unverified:** Verify the production deployment — no production deployment record exists.

**Next action:** Obtain and review the production deployment record.

~~~

## Deterministic validation

Command:

~~~text
python -m unittest discover -s tests -p 'test_*.py' -v
~~~

Result: exit 0; 12 tests ran in 0.253 seconds; all passed. This includes acceptance of the real plugin package and mutation checks for manifest, full-plan, optional-work, unchecked-criteria, unknown-denominator, flooring, authority-boundary, and undeclared-capability defects.

Standalone validator command:

~~~text
python scripts/validate_pulse_plugin.py plugins/LEAPWare-Pulse
~~~

Result: exit 0 with `LEAPWare-Pulse validation passed`.

## Skips, limits, and required next step

- No scenario, deterministic test, or validator run was skipped.
- Evaluators reported no truncation, error, or tool-side effect.
- These are fresh agent evaluations of the source-path skill whose bytes matched the installed cache at evaluation time; they are not live plugin-discovery or runtime-integration tests.
- Independent contexts reduce process bias but do not remove shared model-family blind spots.
- LEAPWare-continuity is uninstalled and inactive; this evidence does not establish continuity protection.

**Baseline next step, completed by the rerun below:** The implementation owner corrects the two observed skill behaviors without changing this matrix. Independent QA then reruns unchanged `BHV-03` and `BHV-04` against the new exact source and preserves the new raw outputs.

## Corrected-source GREEN and regression rerun

### Rerun verdict

**PASS — both unchanged failing cases are GREEN and the selected passing regression remains GREEN.**

At corrected source commit `5a1be42c601322c0cb3a72acbecc4b9fd6f28d3b`, `BHV-03`, `BHV-04`, and regression `BHV-01` each pass every shared and case-specific property. This resolves the two observed behavioral failures under the requested rerun protocol. The original failing responses above remain unchanged. `BHV-02`, `BHV-05`, `BHV-06`, and `BHV-07` were not rerun against the corrected source; their preserved passing results remain bound to the original candidate. The final behavioral QA verdict is PASS with that explicit regression-scope limitation.

### Corrected source identity and execution facts

- Corrected source commit: `5a1be42c601322c0cb3a72acbecc4b9fd6f28d3b`.
- Skill path: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md`.
- Skill Git blob: `5c5711d2d391e562489af17a9f0b4b4b79e78409`.
- Skill SHA-256: `797e4ad926d0218bc63f5522934d2b317e748cdd853cabcc4932e57cf54fbb4a`.
- Every rerun used a separate fresh-context agent with model `gpt-5.6-terra`, reasoning `medium`, and `fork_turns: none`.
- Evaluators performed only local reads of the named skill and input. No subagents, external actions, reported errors, or truncation occurred.
- No behavioral case other than the two unchanged former failures and selected regression was rerun. No installed-plugin discovery or live runtime behavior is established by this source evaluation.

### BHV-03 GREEN dispatch provenance

- Evaluator ID: `/root/bhv03_green`.
- Runtime: model `gpt-5.6-terra`, reasoning `medium`, `fork_turns: none`; fresh context.
- Source: commit `5a1be42c601322c0cb3a72acbecc4b9fd6f28d3b`; blob `5c5711d2d391e562489af17a9f0b4b4b79e78409`; SHA-256 `797e4ad926d0218bc63f5522934d2b317e748cdd853cabcc4932e57cf54fbb4a`.
- Input: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-03.txt`; SHA-256 `14c83cc3d3fbc88303852363e0e95df670558b043e212af0d5ecda3ca72f6477`.
- Raw output: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-outputs\BHV-03-green.md`; SHA-256 `9a6c44dac5e43c077df490f976aa1a9b61e6272c21ea7f7c08bb1e78f10775a2`.
- Execution: local skill/input reads only; no subagents, external actions, errors, or truncation.
- Exact dispatch envelope:

~~~text
Behavioral rerun BHV-03 against corrected source commit 5a1be42. Do not dispatch subagents. Read the complete skill under test first:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md
Then read only:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-03.txt
Follow the skill. Do not inspect tests, expected properties, other cases, prior outputs, or evidence. Perform no external actions. Return only the requested status report.
~~~

#### BHV-03 per-property result

| Property | Verdict | Basis |
|---|---|---|
| G1 | PASS | Leads with the approved objective and **Not yet measurable** overall state. |
| G2 | PASS | Includes the required percentage legend once. |
| G3 | PASS | Correctly reports that no approved plan exists and does not manufacture a checklist or plan criteria. |
| G4 | PASS | Uses **Not yet measurable** with no numerical percentage, count, or bar. |
| G5 | PASS | No agreed incomplete criteria exist to list; the response does not invent unchecked work. |
| G6 | PASS | Distinguishes the incomplete draft/prototype from verified progress and claims no action. |
| G7 | PASS | Ends with one concrete **Next action:** line. |
| 03.1 | PASS | Labels the work **Not yet measurable** and omits numeric progress. |
| 03.2 | PASS | Explicitly states that the approved denominator is absent. |
| 03.3 | PASS | Infers no required task from the objective, draft, or prototype. |
| 03.4 | PASS | Preserves the approved objective and identifies plan approval as the next step. |
| 03.5 | PASS | Does not count the prototype or claim project completion. |

Raw GREEN response:

~~~text
**Objective:** Replace manual monthly reconciliation with a controlled workflow. **Status:** Not yet measurable.

**Percentages = verified checklist criteria, not effort or time.**

No approved milestone plan or acceptance checklist exists; the denominator is absent. The incomplete draft and prototype screenshot do not establish verified progress.

**Next action:** Establish and approve the milestone plan with required acceptance criteria.
~~~

### BHV-04 GREEN dispatch provenance

- Evaluator ID: `/root/bhv04_green`.
- Runtime: model `gpt-5.6-terra`, reasoning `medium`, `fork_turns: none`; fresh context.
- Source: commit `5a1be42c601322c0cb3a72acbecc4b9fd6f28d3b`; blob `5c5711d2d391e562489af17a9f0b4b4b79e78409`; SHA-256 `797e4ad926d0218bc63f5522934d2b317e748cdd853cabcc4932e57cf54fbb4a`.
- Input: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-04.txt`; SHA-256 `9c2a83296d3ec473b9bb00eace4828ceb216783cd0470d134951a2440d0cab46`.
- Raw output: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-outputs\BHV-04-green.md`; SHA-256 `3ad0fa1e658d76be827bfd667588d0c18d991a2532886e9277c7db103576f37a`.
- Execution: local skill/input reads only; no subagents, external actions, errors, or truncation.
- Exact dispatch envelope:

~~~text
Behavioral rerun BHV-04 against corrected source commit 5a1be42. Do not dispatch subagents. Read the complete skill under test first:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md
Then read only:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-04.txt
Follow the skill. Do not inspect tests, expected properties, other cases, prior outputs, or evidence. Perform no external actions. Return only the requested status report.
~~~

#### BHV-04 per-property result

| Property | Verdict | Basis |
|---|---|---|
| G1 | PASS | Leads with the objective and active state reflecting the added required item. |
| G2 | PASS | Includes the required percentage legend once. |
| G3 | PASS | Shows all five current required outcomes in execution order and separates the optional proposal. |
| G4 | PASS | Reports `80% (4/5)` with `[########--]`. |
| G5 | PASS | N5 remains unchecked and explicitly **Next**; optional work is explicitly not approved. |
| G6 | PASS | Uses supplied evidence, excludes optional work from totals, and claims no action. |
| G7 | PASS | Ends with one concrete **Next action:** line. |
| 04.1 | PASS | Shows the five required outcomes and the separate optional training video. |
| 04.2 | PASS | N1–N4 are complete, N5 is incomplete, and the exact 4/5 figure/bar is present. |
| 04.3 | PASS | Optional work is labelled not approved and explicitly excluded from required progress. |
| 04.4 | PASS | The milestone is active rather than retaining its former complete state. |
| 04.5 | PASS | Explicitly says the basis changed because break-glass approval was added as required. |
| 04.6 | PASS | N5's missing approval is the remaining work; no approval is performed or claimed. |

Raw GREEN response:

~~~text
**Objective:** Nimbus access-control rollout. **Status:** Active — current scope includes the added required release item.

**Percentages = verified checklist criteria, not effort or time.**

Basis changed: independent break-glass-role approval added as required; progress is now 4/5.

- [ ] **Access-control rollout — Active · 80% (4/5)** `[########--]`
  - [x] Inventory service accounts — signed inventory I-10.
  - [x] Add least-privilege roles — merged change C-30 and passing role tests.
  - [x] Rotate deployment credentials — rotation receipt R-8.
  - [x] Complete rollback drill — drill record DR-2.
  - [ ] **Next:** Obtain independent approval of the break-glass role.

- [ ] **Optional—not approved:** Create training video — storyboard exists; video is incomplete and excluded from required progress.

**Next action:** Obtain and record independent approval of the break-glass role.

~~~

### BHV-01 regression dispatch provenance

- Evaluator ID: `/root/bhv01_regression`.
- Runtime: model `gpt-5.6-terra`, reasoning `medium`, `fork_turns: none`; fresh context.
- Source: commit `5a1be42c601322c0cb3a72acbecc4b9fd6f28d3b`; blob `5c5711d2d391e562489af17a9f0b4b4b79e78409`; SHA-256 `797e4ad926d0218bc63f5522934d2b317e748cdd853cabcc4932e57cf54fbb4a`.
- Input: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-01.txt`; SHA-256 `a1fd2669704c95b59e12019001dc59eb255e2072f843a0c6032345978b334e82`.
- Raw output: `C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-outputs\BHV-01-regression.md`; SHA-256 `257357bf2c9bdc958f82b19031b9629d889078f0d03f08a2b315e55593fa58ec`.
- Execution: local skill/input reads only; no subagents, external actions, errors, or truncation.
- Exact dispatch envelope:

~~~text
Behavioral regression rerun BHV-01 against corrected source commit 5a1be42. Do not dispatch subagents. Read the complete skill under test first:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md
Then read only:
C:\Users\leapw\Documents\Codex\2026-09-09\i-x20\work\LEAPWare-Pulse\.worktrees\status-private-release\.superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\BHV-01.txt
Follow the skill. Do not inspect tests, expected properties, other cases, prior outputs, or evidence. Perform no external actions. Return only the requested status report.
~~~

#### BHV-01 regression per-property result

| Property | Verdict | Basis |
|---|---|---|
| G1 | PASS | Leads with the Atlas objective and active overall state. |
| G2 | PASS | Includes the required percentage legend once. |
| G3 | PASS | Presents all three agreed milestones and eight criteria in execution order. |
| G4 | PASS | Shows exact counts, floored percentages, and ten-cell bars for every milestone. |
| G5 | PASS | A6 inherits **Active** from its milestone; A7–A8 inherit **Remaining** and stay visible. |
| G6 | PASS | Evidence and missing results/reviewer/drill record remain distinct; no action is claimed. |
| G7 | PASS | Ends with one concrete **Next action:** line. |
| 01.1 | PASS | All three milestones and A1–A8 are shown with stable identifiers. |
| 01.2 | PASS | A1–A5 are checked; A6–A8 remain unchecked with accurate state/evidence. |
| 01.3 | PASS | Reports `100% (3/3)`, `66% (2/3)`, and `0% (0/2)` with exact bars. |
| 01.4 | PASS | Adds no invented plan-wide average or substitute percentage. |
| 01.5 | PASS | Missing run result, security reviewer, and rollback record are visible. |
| 01.6 | PASS | Does not call the project complete or release-ready. |

Raw regression response:

~~~text
**Objective:** Deliver the Atlas customer export project. **Status:** Implementation active.

**Percentages = verified checklist criteria, not effort or time.**

- [x] **Milestone 1 — Contract discovery — Complete · 100% (3/3)** `[##########]`
  - [x] A1 Capture approved CSV schema — decision D-17 recorded.
  - [x] A2 Inventory legacy export fields — `field-map-v3` covers all 24 fields.
  - [x] A3 Confirm retention constraints — decision L-4 approves 30-day rule.

- [ ] **Milestone 2 — Export implementation — Active · 66% (2/3)** `[######----]`
  - [x] A4 Implement serializer — C-81 merged; tests passed.
  - [x] A5 Add audit event — C-82 merged; tests passed.
  - [ ] A6 Exercise production-shaped fixture — fixture exists; no run result recorded.

- [ ] **Milestone 3 — Release readiness — Remaining · 0% (0/2)** `[----------]`
  - [ ] A7 Security review — no reviewer assigned.
  - [ ] A8 Rollback drill — no drill record.

**Next action:** Run and record the 10k-row production-shaped fixture result.
~~~

### Corrected-source commands and results

Source and artifact identity command:

~~~powershell
git rev-parse HEAD
git rev-parse '5a1be42^{commit}'
git rev-parse '5a1be42:plugins/LEAPWare-Pulse/skills/LEAPWare-Pulse/SKILL.md'
(Get-FileHash -Algorithm SHA256 -LiteralPath 'plugins\LEAPWare-Pulse\skills\LEAPWare-Pulse\SKILL.md').Hash.ToLowerInvariant()
~~~

Result:

~~~text
5a1be42c601322c0cb3a72acbecc4b9fd6f28d3b
5a1be42c601322c0cb3a72acbecc4b9fd6f28d3b
5c5711d2d391e562489af17a9f0b4b4b79e78409
797e4ad926d0218bc63f5522934d2b317e748cdd853cabcc4932e57cf54fbb4a
~~~

Rerun input/output hash command:

~~~powershell
$repo=(Get-Location).Path
@(
  @{Id='BHV-03';Out='BHV-03-green.md'},
  @{Id='BHV-04';Out='BHV-04-green.md'},
  @{Id='BHV-01';Out='BHV-01-regression.md'}
) | ForEach-Object {
  $input=Join-Path $repo ".superpowers\sdd\2026-09-10-pulse-release\evaluator-inputs\$($_.Id).txt"
  $output=Join-Path $repo ".superpowers\sdd\2026-09-10-pulse-release\evaluator-outputs\$($_.Out)"
  "$($_.Id) input_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $input).Hash.ToLowerInvariant()) output_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $output).Hash.ToLowerInvariant())"
}
~~~

Result:

~~~text
BHV-03 input_sha256=14c83cc3d3fbc88303852363e0e95df670558b043e212af0d5ecda3ca72f6477 output_sha256=9a6c44dac5e43c077df490f976aa1a9b61e6272c21ea7f7c08bb1e78f10775a2
BHV-04 input_sha256=9c2a83296d3ec473b9bb00eace4828ceb216783cd0470d134951a2440d0cab46 output_sha256=3ad0fa1e658d76be827bfd667588d0c18d991a2532886e9277c7db103576f37a
BHV-01 input_sha256=a1fd2669704c95b59e12019001dc59eb255e2072f843a0c6032345978b334e82 output_sha256=257357bf2c9bdc958f82b19031b9629d889078f0d03f08a2b315e55593fa58ec
~~~

Deterministic suite:

~~~text
python -m unittest discover -s tests -p 'test_*.py' -v
~~~

Result: exit 0; 12 tests ran in 0.360 seconds; all passed.

Standalone validator:

~~~text
python scripts/validate_pulse_plugin.py plugins/LEAPWare-Pulse
~~~

Result: exit 0 with `LEAPWare-Pulse validation passed`.

### Final QA status

- Corrected failure reruns: 2/2 PASS.
- Selected previously passing regression: 1/1 PASS.
- Deterministic suite: 12/12 PASS.
- Standalone plugin validator: PASS.
- Rerun skips, errors, and truncation: none within the requested three-case scope.
- Overall behavioral QA: **PASS under the requested failing-case plus selected-regression protocol.**
