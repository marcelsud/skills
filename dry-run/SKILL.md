---
name: dry-run
description: Trial a specification with a disposable end-to-end implementation, then suggest only the spec changes and comments the frictions justify. Prepare the environment for the next iteration and implement the accepted revision. Use when stress-testing stories before delivery, or when asked to dry-run a change.
---

# Dry run

Use a throwaway implementation to expose what a specification leaves unsaid,
then suggest the few changes that finding justifies. The trial's value is
the friction it records. Its diff is evidence, not the deliverable. A
specification cannot hold every implementation detail.

Keep the trial off the delivery branch. The spec author who wrote the
stories reviews the trial. An independent judge is optional. When one
reviews the delivery, keep that verdict so the process itself can improve.

## Decide how far to go

When the user asks only for the trial, stop after the friction report, the
spec-author review, the suggestions, and the learnings entries. When the
user asks for the full technique, continue through the spec writer's
decisions, environment preparation, delivery, and history. Include the
judge when an independent reviewer is available.

The trial may change only its disposable workspace. Delivery edits follow
the user's authorization and the project's conventions. Do not merge,
cherry-pick, or copy the trial onto the delivery branch and treat that copy
as the implementation.

## Keep the roles distinct

The spec author writes the stories and reviews the trial. The implementer
builds the trial and the delivery. The same participant may do both. Do
not ask the environment to switch models; some harnesses cannot.

The spec author does not accept their own suggestions. The spec writer
decides.

A judge is optional. Use an independent reviewer when the user supplies
one. Do not require the harness to choose or launch a model for that
review. When no independent judge is available, skip the comparison. Do
not present the spec author's or the implementer's review as a judge
verdict.

## Write the stories and run the trial

Read the spec writer's learnings log when one exists. Apply a lesson only
when it still matches this repository, and check an environment lesson
against the current environment before treating it as open. Write the
stories the implementer will follow. Then implement them end to end in a
disposable branch or git worktree: environment, code, and tests. Keep that
workspace isolated from the delivery branch.

Start from the stories as written. Do not revise them during the trial in
order to erase a friction. Record each friction against the text the
implementer actually had.

The trial is complete when the stories have been exercised or a concrete
gap blocks them. A missing setting, tool, or skill is a friction, and it
still requires a report. Read the
[friction report](references/friction-report.md) and finish it before
discarding the workspace. The user may keep the workspace for inspection.
It still must not become the delivery branch.

Run every check the trial claims. Report an observed result, a blocker, or
an explicit statement that a check did not run. Do not infer a pass from
the presence of a test.

## Review the trial as the spec author

The spec author who wrote the stories reviews the friction report and the
trial evidence. The review does not polish the trial's code.

For each friction, the spec author answers three questions:

- Was the specification incomplete, contradictory, or naive?
- Did the implementer deviate from the specification, or did the
  specification leave no other faithful option?
- Was a skill, tool, or environment setting missing? Name the gap. Name a
  missing setting, never its value.

A deviation stays a deviation. Do not turn an unforced choice into a
suggested requirement. These answers feed the suggestions. They do not edit
the specification.

If the spec author cannot review, leave the review pending. Do not
substitute the implementer or a judge.

## Suggest changes and prepare the next iteration

Do not rewrite the specification from the friction list. A specification
holds the facts that are hard to infer and that depend on the environment,
not every detail the trial happened to need. Read
[suggestions and learnings](references/suggestions.md).

For each friction, suggest one or more responses:

- A spec change, when the missing fact cannot be inferred from the
  repository and depends on the environment, or when the stories contradict
  each other or state a requirement the trial showed cannot be built.
- Additional context, as a comment beside the story, when the detail is
  inferable or would only narrate the implementation.
- Environment preparation, when the friction is the environment, so the
  next trial or the delivery can run.

Present the suggestions in the conversation. The spec writer owns the
specification. The spec author proposes and does not accept its own
suggestions. The spec writer accepts, edits, or rejects each one. Silence
is not acceptance. Apply only accepted spec changes. Attach accepted
comments as context, not as new requirements. The accepted specification
is the original stories plus those accepted changes.

When no learnings log exists, suggest one for the spec writer. Keep the
entries in the conversation until they name where it lives.

Carry out accepted environment preparation before another trial or the
delivery. Leave preparation pending when it needs a secret, a production
change, or a fact the stories did not assume. Record the lesson for each
suggestion in the spec writer's learnings log.

## Implement on the delivery branch

Implement the accepted specification on the delivery branch. Take behavior
from those stories. Use the trial only to recall which frictions the
accepted changes and the environment preparation were meant to close.
Additional context does not add requirements.

When delivery meets a problem the friction report already contains, record
the rediscovery. Repairing it in the product does not erase the signal.
Treat the repeat as evidence that the accepted specification, a skill, or
the environment preparation still did not make the next iteration
executable.

Follow the project's tests, conventions, and authorization boundaries for
the delivery change. Claim a check only after it has been run.

## Judge the delivery

Judging is optional. When the user supplies an independent reviewer, have
them compare the trial with the delivery. Read the [judge
rubric](references/judge.md) and brief the reviewer with the material it
names. The reviewer is read-only.

The comparison covers adherence to the accepted specification, deviations,
test solidity, evident rework, and whether the improvement is real.
Repeating the trial, including its mistakes, is not an improvement.
Copying a sound approach can still be an improvement when the accepted
specification calls for it and the trial's mistakes stay behind. A comment
the spec writer did not promote is not a missed requirement.

Record scores only with the evidence the reviewer cites. Do not invent
scores or benchmark results. When no independent judge is available, skip
this stage, leave the scores unset, and record the verdict as skipped.

## Record the verdict and improve the process

Append a record to the persistent history described in
[history](references/history.md), including a skipped judge and a verdict
of inconclusive. Record who filled each role as `same-session`,
`independent`, or `skipped`. Do not record a model name.

Before appending, compare the new root-cause category and signature with
earlier records. When the same pair recurs after a process fix was
recorded, the process is not improving. Update the skill, the spec
template, the learnings log, or the environment setup that the earlier
action claimed to fix, and record the new action. Another one-off patch
of the current task does not clear that recurrence.

Report the stage reached, where the friction report, suggestions, and
learnings log live, which suggestions are still pending, the environment
preparation still unfinished, the verdict or that judging was skipped,
whether history was updated, and any recurrence.
