---
name: spec-gap
description: Compare an implementation, PR, or PR stack with its product requirements. Use when asked to score spec coverage, identify missing behavior, or explain what was built beyond the spec.
---

# Spec gap

Show what the implementation covers, what is missing, and what it adds beyond the requirements. Keep coverage and extras separate: extra behavior does not make up for missing requirements.

## Establish scope

Read the supplied requirements and directly relevant linked documents using the available tools. Confirm the code revision and comparison base; for a PR stack, include the full stack. State the sources and code scope in the report.

Use the user's stated scope. Ask only when missing scope or conflicting requirements would materially change the assessment. Do not silently treat the newest document as authoritative. Mark unresolved requirements as Unverified and explain the conflict.

## Compare requirements with code

Build one row per distinct, observable requirement. Deduplicate repeated requirements across documents and keep a consistent level of detail. Exclude explicitly superseded or out-of-scope requirements, with a brief reason.

Trace each requirement through the relevant code and its dependencies, including downstream effects needed to complete the behavior. A method's existence alone does not establish coverage.

| Status | Meaning |
| --- | --- |
| Matched | The code path or test evidence supports the full requirement. |
| Partial | Some required behavior works, with a concrete gap. |
| Missing | Required behavior is absent or a demonstrated blocker makes it unreachable. |
| Unverified | Available evidence cannot establish whether the requirement is met. |

Cite the requirement's source and specific implementation evidence: a file and line, a named test, or an observed result. For Missing, identify the relevant path inspected or the blocker. Keep code inspection, existing test coverage, and tests run during this assessment distinguishable.

Use existing tests when useful to resolve uncertainty. Keep the review read-only: do not patch production code, edit the working tree, or update external documents. If verification requires new tests, use an isolated temporary workspace. Report a blocked test as a verification limit; it does not by itself prove the feature is missing.

## Score coverage

Give Matched one point, Partial half a point, and Missing zero. Divide the
total points by the number of assessed requirements and multiply by 100 to
obtain the coverage percentage.

Show the numerator and denominator alongside the percentage. Exclude Unverified rows from this calculation and report their count. When any remain, label the result **coverage of assessed requirements**, not overall coverage. If no requirements can be assessed, report no score.

This is an equal-weight requirements estimate, not a measure of runtime reliability. Name any critical missing behavior even when the percentage is high. Do not assign an arbitrary ahead/behind verdict.

## Identify extras

List meaningful behavior in the change that the reviewed requirements do not request. Cite evidence and explain its user impact or maintenance cost. An undocumented restriction can be a requirement gap; do not assume it is a harmless guardrail. Avoid calling an extra over-engineering without evidence of unnecessary cost.

## Report

Keep the report proportional to the change:

- Lead with the score, verification limits, and the most important gap.
- State the documentation and code scope, including exclusions.
- Show each requirement, its source, assessment status, and supporting
  evidence or concrete gap in a presentation appropriate to the task.
- List extras separately, or state that none were found.
- End with concrete fixes and decisions needed to reach the requirements.

Mention source conflicts where they affect a row. Group rows only when it improves readability; no separate report template is required.
