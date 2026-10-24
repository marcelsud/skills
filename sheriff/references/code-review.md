# Code review

Find broadly, report narrowly. Read the [shared rubric](rubric.md) before
grading and identify any stricter or authoritative repository policy.

## Freeze the scope

Collect the diff and comparison revision, requirements, acceptance criteria,
applicable policy, tests, remote-check evidence, and project quality-gate
results. Record missing evidence as unknown.

Default to reviewing the diff. Hold the change responsible only for defects
it introduces or measurably worsens. Inspect existing code to establish
behavior, but do not report unrelated baseline debt. Review the whole
repository only when requested.

## Investigate candidates

Map changed behavior to the intended outcome. Look for defects in correctness,
data integrity, reliability, security, privacy, operations, test trust, and
maintenance cost.

Try to disprove each claim before grading it. Trace callers, data flow, guards,
types, cleanup, failure paths, configuration, and existing tests. Reproduce
material uncertainty when practical. Check whether the path is excluded by
an invariant or whether its consequence is intentional.

Admit a formal finding only when it has an exact evidence location, a
falsifiable claim, a reachable path, explicit preconditions, a concrete
consequence, supported confidence and exposure, and an observable resolution
condition. For diff review, also identify how the change introduced or worsened
the defect. Failure to establish these facts leaves a candidate, not a finding.

Classify severity, confidence, and exposure separately using the shared rubric.
Identify any documented mandatory project gate the finding violates. Do not
infer severity directly from coverage, complexity, duplication, churn, file
length, scanner labels, or a passing suite.

## Apply decision rules in order

First reject unreachable paths. Omit speculative and cosmetic observations.
Neither belongs in formal findings or affects the decision.

A finding violating a documented mandatory project gate requires action
before ordinary delivery. So does a blocker, or a material finding with
common or plausible exposure.

A material finding with unknown exposure requires the missing evidence to
be gathered before deciding. A material finding with exceptional exposure
should be tracked and does not block solely on that finding, unless project
policy imposes a mandatory gate or follow-up requirement.

If any finding requires action before delivery, return a rework decision.
Otherwise, if any requires evidence, return a needs-evidence decision.
With neither, approve the change subject to any explicitly required ownership
or follow-up for tracked findings. Lower-priority improvements never cancel
an unresolved higher-priority finding.

## Report findings

Order findings by required action, severity, and evidence strength. For each,
give its location, claim, preconditions, consequence, evidence, severity,
confidence, exposure, applicable mandatory gate, recommended action, and the
condition that resolves it. Explain how the diff introduced or worsened it.

State the overall decision, rubric version, and verification limits. Omit
cosmetic preferences and unsupported speculation. Passing remote checks does
not establish every changed behavior or failure path.

## Independent review and convergence

For a shipping gate, seek two independent reviews of identical frozen inputs
when available and required by the task or project. Reviewers may be people
or separately run models. Keep first-pass results separate. If independent
execution is unavailable, label the result as a single-review assessment and
leave any mandatory independent-review requirement pending.

Reconcile disagreements through exact source evidence and rubric clauses.
Do not vote, average confidence, or silently select the less restrictive
result. Escalate a factual conflict that changes the delivery decision when
available evidence cannot resolve it.

Use one round for substantive findings and one to verify corrections. Expand
scope after that only for a genuine blocker. Stop when remaining observations
are cosmetic. An unresolved material finding is not approval merely because
the review rounds have ended.

Never weaken tests or project gates to obtain approval. Record rejected or
adjudicated candidates separately when calibration is useful. Change rubric
thresholds only from repeated evidence, outside an active assessment.
