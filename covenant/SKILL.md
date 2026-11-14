---
name: covenant
description: Guide agentic reviews of code, plans, summaries, and responses with evidence, severity criteria, and a limit on review rounds. Use when an author and reviewer need to resolve findings and reach a decision without repeated cosmetic revisions.
---

# Covenant

Fix problems that affect the result. End the review when the work meets its
acceptance criteria and the required checks pass.

## Establish the review

Identify the work and revision under review, the author's task, the acceptance
criteria, and the required checks. Use the participants and tools authorized
for the task. If a required reviewer is unavailable, report it. Reviewing your
own work does not count as independent review.

## Classify findings

Classify each finding before sending it:

- Blocker. An error or misleading claim compromises the work's purpose, or
  the behavior risks safety, security, or data loss. The author must fix it.
- Material. The finding changes a reasonable reader's action or a decision
  about implementation, design, merge, or operation. The author must fix it.
- Cosmetic. The change affects wording, precision, or style without changing
  the result. Include it only when the requester asks for cosmetic feedback.

For each Blocker or Material finding, state the evidence, the wrong decision
or behavior it causes, and how to verify the fix. If you cannot name a wrong
decision or behavior, treat the finding as Cosmetic. Synonym changes, line
numbers, and more precise phrasing are usually Cosmetic. A broken reference
that changes a decision can be Material.

Ask for or offer cosmetic opinions only when the task requester asks for that
feedback. List them separately as optional suggestions. They do not block
approval, require fixes, or justify another review round. If the requester
asks only for cosmetic opinions, give those opinions without adding a
readiness assessment.

Check the code or authoritative source before disputing a factual claim.
Withdraw an objection when the evidence disproves it. If the source is
unavailable, state what you could not verify. Do not assert an error without
evidence. Withdrawing an objection does not start another round.

## Limit review rounds

1. In round 1, review the revision against its purpose and acceptance criteria.
   Report Blocker and Material findings. Add optional cosmetic suggestions
   separately if requested. The author fixes the reported problems within
   the task's authorized scope.
2. In round 2, verify the fixes and affected checks. Check that the fixes
   resolve the findings and introduce no Blocker or Material regression.

Stop as soon as no Blocker or Material finding remains and the required checks
are verified. If only cosmetic suggestions remain, end the review. Include
them only if requested and keep them separate from the approval decision.

Allow two rounds per artifact. A third round requires a Blocker and covers
that Blocker and its fix. If Material findings remain at the limit, return
REWORK with the evidence and conditions for resolving them. Leave the next
step to the task owner. Do not reset the count after small revisions or
withdrawn objections. After round 3, the task owner must define and bound any
further review.

Judge severity by consequence, not edit size. A one-line defect can require a
fix. Reaching the round limit does not waive findings or required checks.

## Return a decision

Ask the reviewer, "Does any Blocker or Material issue remain? If none remain
and the required checks are verified, answer APPROVED."

- Return APPROVED with a brief reason when the work meets the criteria.
- Return REWORK with findings the author can act on when problems remain.
- Return NEEDS EVIDENCE and name the missing verification when you cannot
  support a decision. Report known failures even when evidence is also missing.

APPROVED ends the review. Commit, merge, publication, and release still require
the authorization that applies to the task.
