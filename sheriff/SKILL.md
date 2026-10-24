---
name: sheriff
description: Review code changes or triage issue reports using evidence-backed severity, diagnostic confidence, operational exposure, and project gates. Use for diffs, pull requests, patches, release candidates, or issue batches; check duplicates and current state during triage.
---

# Sheriff

Find broadly, report narrowly. Separate the consequence of a defect from
confidence that it exists and exposure of its preconditions.

## Select the mode

Use [code review](references/code-review.md) for a diff, pull request, patch,
implementation, or release candidate. Use [issue triage](references/issue-triage.md)
for existing or proposed reports, including duplicate and stale-report checks.

A list of suspected bugs about a change follows code review. A list of issue
reports follows triage. A ticket supplied as context for a diff does not change
the mode. If the target is ambiguous, ask which assessment is needed. When both
are requested, assess their respective scopes separately.

Read the [shared rubric](references/rubric.md) and the selected mode's guidance.
Apply repository policy when it is stricter or explicitly authoritative and
identify the governing version.

## Establish evidence before deciding

Freeze the inputs and repository revision. Mark unsupported facts unknown.
Try to disprove each candidate by tracing reachable paths, preconditions,
guards, and consequences before classifying it.

Grade severity, diagnostic confidence, and operational exposure separately.
Never invent numeric likelihoods. Treat automated signals as evidence only
through a documented threshold or a supported defect classification.

Identify documented mandatory project gates, then apply the selected mode's
decision rules in order. Do not choose the outcome first and reverse-engineer
the classifications. Never weaken tests, assertions, types, or project gates
to obtain approval or make a report disappear.

## Return the assessment

For code review, report whether the change requires rework, needs more evidence,
or is approved, with substantive findings and their evidence. For issue triage,
report actionable, tracked, verification, and filtered cases with their reasons
and counts. Tracker mutations require explicit user authorization.

State the rubric version and whether the result is a single-review assessment
or independent consensus. Use an available review process without requiring a
particular tool, output schema, or execution interface.
