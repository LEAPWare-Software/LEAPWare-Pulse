# LEAPWare Pulse view recipes

Apply the shared truth, scope and authority rules in SKILL.md before formatting.
Each report starts with its full branded view name, objective and overall state,
and ends with one concrete **Next action:** line. State labels convey meaning
without relying on color. Preserve required failed/unverified work in every view.

## LEAPWare Pulse Panorama

Show all milestones in execution order, with every required criterion as a nested checkbox.
Each milestone row shows its state, verified/required fraction, floored percentage
and ten-cell bar. Check the milestone only when all required criteria are verified.
Keep a blank line between milestone groups and use only one nesting level.
An unknown denominator uses **Not yet measurable**, without a numerical bar.

## LEAPWare Pulse Brief

Show one flat checkbox per required criterion in execution order, labelled with its milestone and stable criterion identity.
Keep each row to its outcome, unfinished state and decisive evidence/blocker phrase.
Retain all completed criteria. Do not add parent milestone checkboxes, nested
criteria or per-milestone percentages/bars. An agreed milestone whose criteria
are incomplete stays visible as **Not yet measurable**, with known criteria and
the specific information gap; that milestone label is not a counted criterion.
Use one **Verified criteria: N/M** line when the entire required plan is known.
Add: **Counts = verified required criteria, not effort or time.**

## LEAPWare Pulse Focus

Group criteria under Active, Next, Blocked, Unverified, Remaining, Complete, Deferred and Cancelled, in that order; omit empty groups.
Use plain group labels and one flat checkbox per criterion. Include the milestone
and stable criterion identity on every row. Within a group preserve plan order.
Each criterion appears exactly once: use Blocked if a missing prerequisite prevents
progress, otherwise Unverified for an unsupported completion claim, otherwise its
actual execution state. A failed result keeps the **Failed** label and cause in
its appropriate unfinished group. Check only criteria in Complete.

Each blocked row identifies the missing prerequisite, the concrete unblock action
and the responsible party if known; write **Responsible: Unassigned** if unknown.
Do not invent owners, deadlines or an owner decision. An agreed milestone with
incomplete criteria stays visible as **Not yet measurable** outside the state
groups; show known criteria in their actual groups. Use the same single verified
count and count legend as Brief when the entire required plan is known.

## Counting and scope in all views

Compute the plan-wide count from unique required criteria, never from milestone rows or state-group totals.
Reuse existing identifiers. When none exist, use stable outcome names instead of
inventing or persisting a second task list. Showing several views does not multiply
the denominator. Brief and Focus display no plan-wide fraction for an incomplete
or empty plan; state **Not yet measurable** and identify the missing plan instead.

Keep optional proposals in a separate **Optional—not approved** list outside the
required checklist and totals. Deferred/cancelled work remains visibly labelled
and unchecked until an authorized scope change removes it from the denominator;
explain the basis change. Never hide completed milestones or remaining criteria
just to shorten a view. A high count never establishes readiness by itself.

## Same facts, three views

Illustrative only: four required outcomes, two verified. Evidence labels below
are fixture identifiers, not claims about the current project. Real reports use
the current agreed plan and actual evidence.

### Panorama example

**LEAPWare Pulse Panorama — Atlas export — Build active**

**Percentages = verified checklist criteria, not effort or time.**

- [x] **Design — Complete · 100% (1/1)** `[##########]`
  - [x] D1: Approve CSV shape — decision DEC-1.

- [ ] **Build — Active · 50% (1/2)** `[#####-----]`
  - [x] B1: Implement serializer — reviewed diff C-1.
  - [ ] **Active:** B2: Pass fixture test — result pending.

- [ ] **Validate — Blocked · 0% (0/1)** `[----------]`
  - [ ] **Blocked:** V1: Verify fresh-session behavior — session unavailable.

**Next action:** Finish the B2 fixture test and record its result.

### Brief example

**LEAPWare Pulse Brief — Atlas export — Build active**

**Verified criteria: 2/4. Counts = verified required criteria, not effort or time.**

- [x] **Design · D1:** Approve CSV shape — decision DEC-1.
- [x] **Build · B1:** Implement serializer — reviewed diff C-1.
- [ ] **Active · Build · B2:** Pass fixture test — result pending.
- [ ] **Blocked · Validate · V1:** Verify fresh-session behavior — session unavailable.

**Next action:** Finish the B2 fixture test and record its result.

### Focus example

**LEAPWare Pulse Focus — Atlas export — Build active**

**Verified criteria: 2/4. Counts = verified required criteria, not effort or time.**

**Active**

- [ ] **Build · B2:** Pass fixture test — result pending.

**Blocked**

- [ ] **Validate · V1:** Verify fresh-session behavior — session unavailable. **Unblock:** establish the test session. **Responsible: Unassigned.**

**Complete**

- [x] **Design · D1:** Approve CSV shape — decision DEC-1.
- [x] **Build · B1:** Implement serializer — reviewed diff C-1.

**Next action:** Finish the B2 fixture test and record its result.
