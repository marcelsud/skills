---
name: covenant
description: Bring an author and reviewer to a bounded, evidence-backed review decision on code, plans, summaries, or responses. Use for multi-agent review exchanges or repeated review-and-revision loops that need clear severity and stopping rules.
---

# Covenant

Resolve consequential problems and end the exchange when the artifact meets
its acceptance criteria. Review for readiness, rather than open-ended
improvement.

## Establish the review

Identify the artifact and revision, the author's task, acceptance criteria,
and any required checks. Use the review participants and capabilities already
authorized for the task. If a separate reviewer is required but unavailable,
report that limitation; a self-check is not independent review.

## Filter findings by consequence

Classify each proposed finding before sending it:

- **Blocker:** factually wrong or misleading in a way that compromises the
  artifact's purpose, including unsafe behavior, security exposure, or data
  loss. Must fix.
- **Material:** changes a reasonable reader's action or an implementation,
  design, merge, or operational decision. Fix.
- **Cosmetic:** changes wording, precision, or style without changing the
  outcome. Omit it unless cosmetic feedback was explicitly requested.

For each Blocker or Material finding, give the evidence, concrete consequence,
and an observable resolution condition. If you cannot identify the wrong
decision or behavior it causes, treat it as Cosmetic. Synonym swaps,
line-number adjustments, and slightly more precise phrasing are Cosmetic by
default; a broken reference that changes a decision can still be Material.

Cosmetic feedback is opt-in. The author may ask a reviewer for cosmetic
opinions when the task requester has asked for that feedback. Do not solicit
or volunteer cosmetic opinions otherwise. When requested, present them
separately as optional suggestions; they do not block approval, require fixes,
or justify another substantive review round. A request for cosmetic opinions
alone calls for those opinions, not an unrequested readiness assessment.

Verify disputed factual claims against the code or authoritative source
before challenging them. If the evidence disproves your objection, withdraw
it plainly and close it. If the source is unavailable, state what remains
unverified rather than asserting an error. A withdrawn objection does not
start another round.

## Run a bounded exchange

1. **Round 1: substance.** Review the identified revision against its purpose
   and acceptance criteria. Send Blocker or Material findings, plus separately
   identified optional cosmetic feedback if explicitly requested. The author
   addresses consequential findings within the authorized scope.
2. **Round 2: verification.** Inspect the corrections and affected checks.
   Confirm that the findings are resolved and the fixes introduce no
   consequential regression. Do not reopen the exchange for cosmetic polish.

Stop early when no Blocker or Material issue remains and the required evidence
is available. A round containing only cosmetic suggestions ends the
substantive exchange; include those suggestions only if requested, without
turning them into approval conditions.

The normal limit is two rounds per artifact. A third round requires a genuine
Blocker and stays focused on that Blocker and its fix. If Material findings
remain at the limit, return REWORK with their evidence and resolution
conditions, and hand the decision to the task owner rather than cycling or
approving them. Do not reset the count for each small revision or withdrawn
objection. Further Blocker-driven work needs an explicit bounded next step
from the task owner, rather than an automatic fourth round.

Judge severity by consequence, never by edit size. A one-line defect remains
consequential. A round limit bounds the exchange; it does not waive an
unresolved finding or a required check.

## Close with a decision

Ask the reviewer: **"Any Blocker or Material issue? If none remain and required
checks are verified, answer APPROVED."**

Return APPROVED with a brief basis when the criteria are met, REWORK with
actionable findings when they are not, or NEEDS EVIDENCE with the missing
verification when a decision cannot yet be supported. Distinguish known
failures from unknowns; do not conceal a known failure behind missing evidence.

APPROVED ends this review exchange. It does not grant permission to commit,
merge, publish, or release; delivery follows the task's existing authorization.
