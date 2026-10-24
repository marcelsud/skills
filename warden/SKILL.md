---
name: warden
description: Validate or ship code changes through intent capture, evidence-based review, targeted tests, documentation, and lint. Use when the user asks to gate, validate, or ship changes safely.
---

# Warden

Validate the change against the user's intent, then deliver only the outcome
the user authorized. Use the repository's existing conventions and available
capabilities throughout.

## Establish the delivery scope

Distinguish local validation, publication, and a repository-defined delivery
process. Local validation ends after review, tests, documentation, and lint.
Publication adds branch integration, committing, pushing, a pull request when
requested, and verification of remote checks. A repository-defined process
uses the project's documented steps and review requirements.

Use the user's instructions to choose the scope. If a consequential delivery
choice remains unclear, ask. A request to validate alone does not authorize
publication. Preserve explicit phase skips, but always establish intent and
perform review unless the user explicitly waived it.

Inspect the working tree before editing. Preserve unrelated work and never
stash, reset, clean, stage, or commit it as part of this task. If implementation
is requested, complete it before validating the result.

## Capture intent

Record the desired behavior, acceptance criteria, constraints, exclusions,
deliberate tradeoffs, and rejected approaches. Include context that would
otherwise make a reviewer question an intentional decision. Carry this intent
into every later phase.

## Integrate when publication requires it

Follow the repository's branch and integration policy. Refresh the relevant
remote branches, identify the actual default branch, and inspect the full
change against its intended base. Avoid bundling unpublished local-default
commits or unrelated history.

Use the chosen merge or rebase strategy. Resolve conflicts only when both
sides' intended behavior can be preserved; ask about consequential ambiguity.
Do not leave a failed integration in progress. If the intended diff becomes
empty, report that there is nothing to deliver.

## Review the actual snapshot

Give an independent reviewer the intent, exact revision or working-tree
snapshot, relevant sources, and validation evidence. The reviewer may be a
person or a separately run model; no particular agent role or interface is
required. Keep the review read-only and separate from implementation.

Follow documented requirements for reviewers and models. If an independent
review or required reviewer is unavailable, provide a review handoff and
report the gate as pending. Do not relabel self-review as independent approval
or silently replace a required reviewer.

### Admit substantive findings

Report a finding only when it has an exact source location, a falsifiable
claim, a reachable path with explicit preconditions, and a concrete consequence
for correctness, reliability, security, or the agreed acceptance criteria.
Trace callers, error paths, cleanup, and related uses before reporting it.

Classify findings as blockers when the demonstrated defect makes delivery
unsafe or violates a core acceptance guarantee, and material when the evidence
would change a reasonable delivery decision. Omit cosmetic preferences,
speculative redesign, and unrelated baseline debt. Check sources before
disputing a factual claim.

### Converge on a decision

Ask whether any blocker or material issue remains; otherwise request approval.
Fix substantive findings and rerun the focused checks that prove the fixes.
Have the same reviewer verify them against the updated snapshot.

Use at most two review rounds per artifact: one for substance and one to
verify corrections. Additional review requires a genuine blocker. A round
containing only cosmetic observations ends the exchange. An unresolved
blocker or material finding remains unresolved at the cap; never convert it
into approval merely because review rounds are exhausted.

Raise findings that challenge deliberate product intent with the user. Do
not dismiss them or change the intended behavior without resolving the
decision. Record any remaining review limitation explicitly.

## Verify behavior

Run documented targeted checks first, then the smallest additional checks
that establish the intent. Run broader checks when project policy requires
them or unresolved risk justifies them. A nonzero result is a failure.

Tests must exercise a public interface and assert observable behavior, state,
output, or failure. Matching source text does not establish behavior. For a
regression fix, reproduce the failure before the fix when feasible and observe
success after it. For visual changes, provide rendered evidence or explain
why it could not be captured.

Use a focused test or an evidenced manual check when existing tests cannot
establish the behavior. If verification is impossible, report the missing
evidence and leave the gate pending. Never weaken assertions or change
expected behavior just to pass.

## Update documentation and lint

Repair documentation gaps created by the diff. Follow existing ownership
rules, keep each fact in one place, and remove stale duplication. Create a
new document only when the task or repository requires one. Ask about gaps
that depend on an unresolved product decision.

Run the repository's formatter and linter on the affected scope when available.
Apply safe mechanical fixes and rerun the same checks. Resolve failures that
would block delivery; do not expand the task for optional style changes.

## Publish the validated change

Publish only when authorized and after the applicable local gates pass.
Stage and commit only the task's files. Check the remote state before pushing
and do not overwrite commits missing from the local branch. Use an appropriate
lease safeguard when an authorized rebase requires rewriting a remote branch.
Push exactly the revision reviewed and validated.

For a requested patch, produce the patch without publishing it. For a requested
pull request, create or update it through an available authorized interface.
Describe the concrete problem, resulting behavior, full branch scope, material
risks, review decision, tests run, and any delivery limitations. If the host is
unavailable, report the completed push and the remaining handoff.

## Verify remote results

When delivery includes remote checks, inspect results for the exact published
revision. An empty, cancelled, or still-running check set is not evidence of
success. Honor a documented policy for repositories without remote checks.

Investigate failures, repair their root cause, revalidate affected behavior,
and obtain review of substantive changes before publishing the corrected
revision. Rerun a cancelled check on the same revision when supported. If the
published head changes unexpectedly, stop and resolve the discrepancy.

Cap automatic fixes at three attempts per failing phase. Then report the
remaining failure and ask for the decision needed to continue. Preserve
unrelated work and never claim failed or unobserved checks passed.

Merge only when the user's instructions authorize it. Otherwise return the
published link and completed evidence without merging.

## Close the loop

Report the delivery scope, validated behavior, review status, checks and
results, changes made during validation, and publication details when
applicable. Distinguish local evidence from remote results. Identify pending
gates and unresolved product decisions; do not claim completion while a
required gate remains open.
