# Acceptance criteria and evidence

A gate is an observable outcome required by the task. Describe the outcome,
the check that can establish it, the expected result, its current status, and
the evidence observed. Use a format appropriate to the project's existing
task records; no parser, template, or fixed filename is required.

## Define meaningful outcomes

State what must be true for the user, rather than an activity such as working
on a component. Separate outcomes that can pass or fail independently. Keep
each set small enough to review without losing requirements.

Prefer repeatable checks through public interfaces when they can observe
the outcome. A success marker must distinguish success from partial execution
or failure. For outcomes requiring judgment, cite direct observations and
the requirement they establish.

## Assess status

A criterion passes only when the check succeeds and its evidence supports
the full outcome. Pending, missing, stale, or contradictory evidence leaves
it unmet even if its status was previously marked complete.

Record concise evidence: the relevant result, source location, measurement,
or artifact. Preserve enough context to identify what was checked and against
which revision or state. Rerun relevant checks when that state changes.

A failed verification reopens the criterion. A blocker should identify the
missing prerequisite and the decision or external change needed to proceed.
A user-approved waiver is recorded separately from successful validation;
it must remain visible in the final report.

## Verify integration and reporting

Parent criteria establish that child deliverables work together, their
interfaces match the agreed contract, and affected related behavior still
works. A child's completion claim alone does not establish integration.

Measure every count or percentage reported to the user. For an exhaustive
task, compare the required inventory with what was actually checked and
report omissions explicitly.
