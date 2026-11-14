---
name: arbiter
description: Grade issue value, implementation quality, or project and release health from evidence and concrete consequences. Use when an explicit grade or grading consensus is requested; ordinary code review belongs to the project's review workflow.
---

# Arbiter

Explain how valuable an outcome is or how well an artifact achieves its
purpose. Derive the grade from the evidence, then state what would change it.
This file contains the complete grading method.

## Start with the outcome

Identify what is being assessed, its revision, the intended outcome, and any
comparison baseline. Use the user's requirements and the project's actual
contracts and constraints. A formal issue, objective registry, or grading
configuration is unnecessary. If the intended outcome is unclear enough to
change the assessment, clarify it before assigning a grade.

Keep three questions separate:

- **Value:** How much does solving this problem matter?
- **Quality:** How well does the implementation achieve its purpose?
- **Readiness:** Is the change sufficiently proven for delivery under the
  project's requirements?

A small improvement can be implemented excellently. An important problem can
have a poor solution. Report those facts separately instead of forcing them
into one overall letter.

## Establish the facts

Inspect the relevant artifact and evidence: requirements, source, diff,
reproductions, tests, measurements, or observed behavior. Match verification
to the change and its risks. Check whether assertions prove the intended
behavior and relevant failure paths; green CI or a coverage number alone
does not establish that.

Separate demonstrated facts, inferences, and unknowns. Missing evidence that
could materially change a grade means `UNGRADED` for that dimension. Name
what is needed and retain any known failures; uncertainty must not hide a
proven defect. An unavailable optional check does not automatically prevent
grading when other evidence establishes the outcome.

Count a weakness only when it has a concrete consequence for correctness,
safety, reliability, usability, operations, or maintenance. Cite a location
or source, explain the consequence, and give an observable resolution
condition. Distinguish:

- **Blocker:** A defect or exposure that makes delivery unsafe or defeats
  an essential requirement.
- **Material:** A consequence that changes a reasonable product, design,
  maintenance, or delivery decision.
- **Cosmetic:** A preference or equivalent formulation with no demonstrated
  consequence. Exclude it from grade penalties.

When assessing a change, establish what it introduces or worsens relative
to the baseline. Keep pre-existing debt separate; it can still affect current
project health or release readiness. Size, effort, naming, abstraction count,
and stylistic preference do not independently determine a grade.

## Grade the requested dimension

### Issue or proposed work: value

Assess the demonstrated benefit of resolving the problem, independently of
implementation quality. Check whether the problem is still present and
whether existing work already addresses it.

| Grade | Demonstrated value |
| --- | --- |
| A | Protects an essential guarantee, removes a critical risk, or enables a major outcome for the project or its users. |
| B | Produces a meaningful, localized improvement in behavior, capability, or operation. |
| C | Removes bounded maintenance or test debt with a concrete benefit. |
| D | Provides cosmetic, administrative, or preference value with no demonstrated material outcome. |

Use the highest level whose impact is supported. D does not mean the work
is forbidden, and severity alone does not describe every kind of value.

### Implementation or pull request: quality

Assess whether the artifact meets its intended behavior, preserves relevant
contracts, handles material failure paths, and has proportionate proof.
Consider unnecessary complexity, dependencies, hidden effects, and ownership
cost only where they have a demonstrated consequence.

| Grade | Demonstrated quality |
| --- | --- |
| A | Meets the intended outcome with convincing evidence and no consequential implementation weakness found in the assessed scope. |
| B | Meets the outcome with bounded local compromises whose consequences are understood. |
| C | Has a material implementation weakness or ongoing cost, while the essential behavior is established. |
| D | Has a proven failure of essential behavior, a Blocker, or unsafe exposure. |

Apply the worst demonstrated condition. Do not average a serious defect away
with strengths elsewhere. A permitted exception records an accepted weakness;
it does not improve the quality grade. Use `UNGRADED` when the evidence cannot
distinguish the applicable levels, while reporting any established grade
ceiling and findings.

### Project or release: health

Apply the quality scale to the current assessed scope using direct evidence
of working behavior, reliability, test trust, and outstanding debt. Compare
with the previous release or another stated baseline when judging change.
Do not infer whole-project health from a few reviewed PRs or from issue-value
grades. State limits on coverage: narrow positive evidence cannot establish
good whole-project health, while a demonstrated release-relevant Blocker
establishes D even when the remaining scope is unassessed. An empty set of
changes proves no health grade by itself.

## Report the decision

Give the scope and revision, the grade for each requested dimension, a short
rationale tied to decisive evidence, consequential findings, and unresolved
questions. Explain what improvement or evidence would change the result.
Use a compact narrative or table; no special record format is required.

For implementation or release assessments, report readiness separately:

- **READY:** Relevant requirements are established, applicable required
  checks pass, and no unresolved finding requires action before delivery
  under the project's rules. Disclose any accepted compromises.
- **REWORK:** A known defect, unmet requirement, or applicable policy failure
  requires correction. A D-quality artifact is always REWORK.
- **NEEDS EVIDENCE:** A consequential unknown prevents deciding readiness.

Report known reasons for REWORK even when other evidence is missing. A grade
or READY assessment does not grant permission to merge, release, change
policy, or publish findings; existing user and repository approvals apply.

When consensus is requested, compare independently produced assessments of
the same scope, revision, criteria, and evidence. Resolve factual differences
against the artifacts and explain remaining disagreement. Matching letters
alone do not establish consensus, and rereading one's own work is not an
independent review. If another reviewer is unavailable, return the available
assessment and state that consensus has not been established.
