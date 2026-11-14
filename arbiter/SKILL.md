---
name: arbiter
description: Grade the value of proposed work, the quality of an implementation, or the health of a project or release. Use when the user asks for a grade or grading consensus. Use the project's review workflow for ordinary code review.
---

# Arbiter

Base each grade on the intended outcome and the evidence. Explain which facts
determine the grade and what would change it.

## Define the assessment

State what you are grading, its revision, its intended outcome, and any
comparison baseline. Use the user's requirements and the project's contracts
and constraints. You do not need a formal issue, objective registry, or grading
configuration. Ask for clarification if the intended outcome is unclear enough
to change the grade.

Grade value and quality separately. Value measures the benefit of solving the
problem. Quality measures how well the implementation meets its requirements.
Do not combine them into one letter. For implementations and releases, also
report readiness under the project's delivery rules.

## Check the evidence

Read the relevant requirements, source, diff, reproductions, tests, measurements,
or observed behavior. Choose checks that match the change and its risks. Inspect
whether test assertions prove the intended behavior and relevant failure paths.
Green CI or a coverage number alone does not prove either.

Separate facts, inferences, and unknowns. Use `UNGRADED` when missing evidence
could change the grade. Say what evidence is needed and report known failures.
A missing optional check need not prevent grading if other evidence proves
the outcome.

A weakness needs a concrete consequence for correctness, safety, reliability,
usability, operations, or maintenance. Cite its location or source, explain
the consequence, and state how to verify a fix.

| Severity | Meaning |
| --- | --- |
| Blocker | A defect or exposure makes delivery unsafe or defeats an essential requirement. |
| Material | The consequence changes a reasonable product, design, maintenance, or delivery decision. |
| Cosmetic | A preference or equivalent formulation has no demonstrated consequence. Exclude it from grade penalties. |

For a change, show what it introduces or worsens compared with the baseline.
Report existing debt separately. It can still affect project health or release
readiness. Size, effort, naming, abstraction count, and style do not determine
a grade without evidence of a consequence.

## Grade value

For an issue or proposed work, assess the benefit of solving the problem.
Check that the problem still exists and that existing work has not addressed it.

| Grade | Value |
| --- | --- |
| A | Protects an essential guarantee, removes a critical risk, or enables a major outcome for the project or its users. |
| B | Makes a meaningful, localized improvement to behavior, capability, or operation. |
| C | Removes bounded maintenance or test debt with a concrete benefit. |
| D | Provides cosmetic, administrative, or preference value without a demonstrated material outcome. |

Choose the highest grade the impact supports. A D value grade does not forbid
the work. Record severity separately from value.

## Grade quality

For an implementation or pull request, check that it meets its requirements,
preserves relevant contracts, handles material failure paths, and has enough
evidence to prove those claims. Assess complexity, dependencies, hidden effects,
and ownership cost by their consequences.

| Grade | Quality |
| --- | --- |
| A | Meets the intended outcome with convincing evidence. No consequential implementation weakness was found in the assessed scope. |
| B | Meets the outcome with bounded local compromises whose consequences are understood. |
| C | Has a material implementation weakness or ongoing cost, while evidence establishes the essential behavior. |
| D | Has a proven failure of essential behavior, a Blocker, or unsafe exposure. |

Apply the worst condition shown by the evidence. Strengths elsewhere
cannot cancel a serious defect. An exception records acceptance of a weakness;
it does not improve the grade. If evidence cannot distinguish the applicable
grades, use `UNGRADED` and report any known limit on the grade.

## Grade project or release health

Apply the quality scale to the current scope. Use evidence of working behavior,
reliability, test trust, and outstanding debt. To assess a change in health,
compare with the previous release or another stated baseline.

Report the limits of what you inspected. A few good pull requests, issue value
grades, or an empty set of changes cannot establish good health for the whole
project. A proven release blocker establishes D even if the rest of the project
has not been assessed.

## Report the result

Give the scope and revision, each requested grade, and the evidence that
determined it. Include findings and unanswered questions. State what change
or evidence would improve the result. Use prose or a table.

For an implementation or release, report readiness separately:

| Status | Meaning |
| --- | --- |
| READY | Evidence establishes the relevant requirements, required checks pass, and no finding requires action before delivery under the project's rules. Disclose accepted compromises. |
| REWORK | A known defect, unmet requirement, or policy failure needs correction. A D quality grade always means REWORK. |
| NEEDS EVIDENCE | A material unknown prevents a readiness decision. |

Report known reasons for REWORK even if other evidence is missing. A grade or
READY status does not authorize a merge, release, policy change, or publication
of findings. Follow the user's and repository's approval rules.

When the user requests consensus, compare independent assessments of the same
scope, revision, criteria, and evidence. Check disputed facts against the
source and explain unresolved disagreement. Matching letters alone do not
establish consensus. Rereading your own work is not an independent review.
If no other reviewer is available, return your assessment and state that
consensus has not been established.
