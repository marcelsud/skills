# Issue triage

Investigate broadly, retain narrowly. Read the [shared rubric](rubric.md)
before grading and identify any stricter or authoritative repository policy.

## Freeze the inputs

Collect the issue set, repository revision, report bodies, linked evidence,
requirements, acceptance criteria, tests, remote-check evidence, existing
open and closed issues, active pull requests, and project policy. Preserve
the original issue identifiers and mark missing facts unknown.

Assess reports against the current repository state. A baseline defect need
not prove which change introduced it unless the report claims a regression.
Do not expand triage into an unrelated repository audit.

## Establish the claim and current state

Normalize each report into a falsifiable problem. Split bundled reports only
when their claims have independent causes or resolutions. Trace callers,
data flow, guards, types, cleanup, failure paths, configuration, and tests to
try to disprove the claim. Reproduce it when practical.

Search existing issues and pull requests for the same root cause and
substantially the same resolution. Shared symptoms, files, labels, titles,
or keywords do not establish duplication. Name the owning issue or pull
request for every duplicate.

Mark a report resolved only when evidence at the frozen revision establishes
that its claim is already fixed. A proposed fix, an open pull request, a
failed reproduction without controlled preconditions, or old line numbers
do not establish resolution. A demonstrated invariant may instead show the
path is unreachable; record that distinction.

## Establish eligibility

A retained issue needs an exact source or evidence location, a falsifiable
claim, a reachable path, explicit preconditions, a concrete consequence,
supported confidence and exposure, and an observable resolution condition.
It must be current and have no existing owner of the same root cause and
resolution.

Unknown evidence is not evidence that a claim is false. Use targeted
verification when one observation can settle eligibility. Do not retain a
speculative or cosmetic report as a confirmed issue. Do not discard a
demonstrated current defect merely because its exposure is exceptional.

Classify severity, confidence, and exposure separately using the shared
rubric. Identify any violated mandatory project gate. Tracker state and
duplication are separate from severity.

## Apply disposition rules in order

Filter a proven duplicate in favor of its named owner. Next filter a report
proven resolved at the frozen revision, then a proven unreachable path.
Then filter speculative or cosmetic reports as unsubstantiated. When a
specific unresolved fact can be settled by a targeted check, leave the report
pending verification rather than pretending it was disproven.

For an eligible current report, retain it as actionable if it violates a
documented mandatory project gate, is a blocker, or is material with common
or plausible exposure. Follow project policy for ordinary or urgent ownership.

A material report with unknown exposure remains pending verification. Name
the exact missing evidence and how it can be obtained. A material report
with exceptional exposure remains tracked; rarity alone does not invalidate
the report. Mandatory project gates can still require immediate action.

## Return the triage

Report retained actionable and tracked issues first, pending verification
second, and filtered reports last. Preserve original identifiers. For every
case, explain the claim, location, current state, duplicate owner when
applicable, preconditions, consequence, evidence, classifications, required
action, and resolution condition. Give a concrete evidence-backed reason for
every filter decision.

Count retained, pending-verification, and filtered reports so every input is
accounted for once. A pending case is neither accepted nor filtered. State
the rubric version and review limits.

Filtering is an assessment, not permission to modify a tracker. Close,
relabel, or otherwise change issues only when the user authorized those
actions and the evidence for each change is recorded.

## Independent review and convergence

For consequential cleanup or automated closure batches, seek two independent
reviews of the same frozen reports and evidence. Reviewers may be people or
separately run models. Keep first-pass results separate and resolve conflicts
through source evidence and rubric clauses rather than votes or averaged
confidence.

Require agreement on any disposition that closes or suppresses a report
when the task or project requires consensus. If independent review is
unavailable, label the assessment accordingly and leave mandatory consensus
pending. Escalate unresolved factual conflicts that would change a closure
decision.

Never weaken tests or gates to make reports disappear. Do not add unrelated
issues without authorization for an audit. Keep rejected or adjudicated
reports for calibration when useful, and change rubric thresholds only from
repeated evidence outside an active assessment.
