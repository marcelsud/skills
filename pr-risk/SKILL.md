---
name: pr-risk
description: Classify a pull request's merge risk and report a review that determines who may merge. Use when reviewing a PR for merge authorization, especially when the change may depend on secrets or publish a package.
---

# Risk-based PR review

Decide whether a change is safe to merge and who must approve that merge.
A thorough review of correctness is necessary, but it does not by itself
authorize merge of a high-risk change.

## Classify merge risk

Inspect the diff, workflow files, release or publish configuration, and any
documented delivery steps.

Assign **high** risk when the change depends on secrets or publishes a
package. Examples include introducing or rotating credentials, reading
secrets in CI, changing how secrets are injected, adding or altering a
publish job, or releasing a new or existing package. High-risk changes
require approval from the repository owner (a human) before merge.
Coordinator or maintainer merge authority is not sufficient.

Assign **normal** risk to every other change. Some projects label this
level as "the rest" (`demais`) and high as `alto`; use the project's
labels when they are established, and keep the same two-level meaning.

Record the assigned level with a short justification citing the evidence
(files, jobs, or release steps) that led to it. Do not raise or lower the
level based on review findings; findings affect the verdict, not the
inherent merge risk of the change.

If classification is uncertain because evidence is missing, treat the
change as high risk until the uncertainty is resolved.

## Review the change

Freeze the comparison base and the revision under review. Keep the review
read-only.

When a general evidence-backed code-review workflow is available, follow
it for investigation and severity. Otherwise inspect the diff for defects
in correctness, data integrity, reliability, security, privacy, operations,
test trust, and maintainability. Report a finding only with a precise
location, a falsifiable claim, a reachable path, and a concrete consequence.

A focused review needs a focus prompt. Some review-against-base commands
do not accept a focus prompt; this was observed with `codex review --base`
as of Codex 0.167.1. In that case, use a read-only execution that does
accept a focus prompt, for example `codex exec --sandbox read-only`.
Do not require a particular review tool when another available read-only
path can apply the same focus.

## Report the review

Return a single assessment containing:

- **Verdict:** approve, request changes, or needs evidence. Approve only
  when there are no blocking findings. Blocking findings are blockers and
  any material findings that, under the review rules in use, require
  action before delivery.
- **Risk level:** `high` or `normal`, with the justification recorded
  above. Include the project's equivalent label when one is in use.
- **Findings:** grouped by severity (blocker, then material, then any
  retained lower-severity items the project requires). Each finding cites
  `file:line` (or a range), the claim, and the consequence. Omit cosmetic
  preferences and unsupported speculation.

State verification limits, including any focus that was applied and any
evidence that could not be gathered.

## Authorize the merge

The reviewer does not merge. After the review:

- If the verdict is not approval, do not merge. Return the findings and
  wait for a corrected revision and a new review of that revision.
- If the verdict is approval and the risk is high, wait for explicit
  approval from the repository owner (a human). Do not merge on reviewer
  or maintainer authority alone.
- If the verdict is approval and the risk is normal, a coordinator or
  maintainer may merge.

A later revision of a high-risk change remains high risk and still needs
owner approval. Do not treat a previous owner approval as covering a
different revision unless the owner explicitly confirmed the new revision.
