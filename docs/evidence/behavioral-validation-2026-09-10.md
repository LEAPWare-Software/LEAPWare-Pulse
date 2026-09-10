# LEAPWare-status behavioral validation — 2026-09-10

## Verdict

**FAIL — 5 of 7 scenarios passed; 2 failed.**

`BHV-03` violates the unknown-denominator boundary by manufacturing an unapproved milestone and criteria. `BHV-04` recomputes the changed scope correctly but omits the required statement that the percentage basis changed when N5 became required. These failures require a product correction by the implementation owner and fresh reruns of the unchanged failing cases. Passing deterministic validation does not override observed behavioral failures.

## Source and environment

- Product candidate: `3886571c16cce6f87997124138f55fadedcc06fe` (`Harden status plugin validator`).
- Independently authored matrix commit: `9a5da4ee3dfa7530564a5ff7e7f9ad309b82f9ff` (`Add independent status behavior scenarios`).
- Skill blob tested: `09bf867bf1bfceacc6c0c33819acc1c484f9e733` at `plugins/LEAPWare-status/skills/LEAPWare-status/SKILL.md`.
- Matrix: `tests/behavioral-scenarios.md` at the matrix commit above.
- Evaluators: seven separate fresh-context agents, `gpt-5.6-terra`, medium reasoning. Each evaluator read only the candidate skill and one case input. Evaluators used no tools beyond local file reads and reported no truncation or errors.
- QA host: Windows PowerShell 7.6.5, Python 3.12.10.
- QA role: independent author of the matrix and verdict; the QA author did not implement the candidate.

## Method

The exact prompts are retained in the committed matrix under the `### Evaluator input` heading for each named case. Each fresh evaluator received the candidate skill and exactly one of those inputs, without expected properties, other cases, prior outputs, or implementation tests. The controller returned the raw responses in `.superpowers/sdd/2026-09-10-status-release/evaluator-outputs/BHV-01.md` through `BHV-07.md`. They are reproduced unchanged below.

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
python scripts/validate_status_plugin.py plugins/LEAPWare-status
~~~

Result: exit 0 with `LEAPWare-status validation passed`.

## Skips, limits, and required next step

- No scenario, deterministic test, or validator run was skipped.
- Evaluators reported no truncation, error, or tool-side effect.
- These are fresh agent evaluations of the source-bound skill, not a live installed-plugin discovery or runtime integration test.
- Independent contexts reduce process bias but do not remove shared model-family blind spots.
- LEAPWare-continuity is uninstalled and inactive; this evidence does not establish continuity protection.

**Required next step:** The implementation owner corrects the two observed skill behaviors without changing this matrix. Independent QA then reruns unchanged `BHV-03` and `BHV-04` against the new exact source, preserves the new raw outputs, and updates this evidence. Until both pass, behavioral QA remains failed.
