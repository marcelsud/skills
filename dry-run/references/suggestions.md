# Suggestions and learnings

The friction report is not a rewritten specification. Suggest what should
change, then let the spec writer decide. A specification cannot carry every
detail of an implementation.

## Choose the response

A friction may need more than one suggestion. Split them. Do not fold an
environment fault and a product decision into one paragraph.

Use `spec-change` only when both are true:

- The next implementer cannot infer the fact from the repository, its
  conventions, or the stories as written.
- The fact depends on the environment: a deployment choice, a setting, or
  an external contract this environment uses and the repository does not
  show.

Also use `spec-change` when the stories contradict each other or state a
naive requirement the trial showed cannot be implemented as written. Say
which reading the evidence supports. The spec writer still decides.

Use `additional-context` for everything else that is worth keeping beside
the story: an edge case the trial met, a pointer to the code or convention
that already answers the question, or an implementation note. A comment is
not a requirement. Prefer this when the detail is inferable once the
implementer looks in the right place.

Use `environment` when the friction is the environment itself: a missing
tool, an absent setting, a setup step the stories already assumed, or a
convention the workspace did not have. The response is to make the next
iteration runnable. Do not copy that setup into the specification unless
the `spec-change` test above also passes.

Name settings. Do not record secret values.

## What a suggestion contains

For each suggestion, state:

- The friction it answers, by its signature.
- The response: `spec-change`, `additional-context`, or `environment`.
- The proposed text. For a spec change, the requirement or non-goal to add
  or replace. For additional context, the comment to attach and where.
  For the environment, the preparation the next trial or the delivery
  needs.
- Why it does or does not belong in the specification. Name what was
  difficult to infer and which environment fact it depends on, or name the
  place the repository already makes it inferable.
- What the next iteration still cannot do until this suggestion is
  resolved, if anything.

Present the suggestions in the conversation. Recommend an option when the
evidence supports one, and label it as a recommendation.

## Wait for the spec writer

The spec writer accepts, edits, or rejects each suggestion. Silence is not
acceptance. Do not edit the specification until they decide.

Apply only accepted spec changes. Attach accepted comments as additional
context and keep them distinct from requirements. An edited suggestion
replaces the proposed text; record the edit.

Carry out accepted environment preparation before another trial or the
delivery implementation. Preparation that needs a secret, a production
change, or a fact the stories did not assume stays pending until the spec
writer provides it. Say what remains unfinished. Do not describe the next
iteration as ready while that preparation is pending.

The accepted specification is the original stories plus accepted spec
changes. Additional context travels with it and does not add requirements
the spec writer did not promote.

## Learnings log

Keep a learnings log for the spec writer, separate from the judge history.
The log is how later specifications avoid repeating the same miss. It is a
file or spreadsheet the user or the project designates. Do not store it in
this skill, and do not create a database for it.

Read the log before writing the next stories. Apply a lesson only when it
still matches this repository. Verify an environment lesson against the
current environment before treating it as open.

If no location has been chosen, ask. Until the user names one, keep the
entries in the conversation and do not claim they were persisted.

Append one entry per suggestion. Update it when the spec writer decides.

| Field | Content |
| --- | --- |
| `date` | Date the suggestion was recorded. |
| `task_id` | Task or story identifier. |
| `spec_revision` | Stories revision the suggestion addresses. |
| `evidence` | Friction report item and the artifact or observation supporting it. |
| `signature` | Friction signature this entry answers. |
| `response` | `spec-change`, `additional-context`, or `environment`. |
| `suggestion` | The proposed requirement, comment, or environment preparation. |
| `why` | Why it belongs in the spec, in a comment, or in the environment. |
| `decision` | `accepted`, `edited`, `rejected`, or `pending`. |
| `environment_ready` | What was prepared for the next iteration, `pending`, or `not-applicable`. |
| `lesson` | What the spec writer should do differently on the next specification. |

A lesson says whether to state an environment-dependent fact, leave an
inferable detail out of the spec, or prepare the environment before the
next trial. It does not restate the whole friction report.

## Example

The following entries show the field shape only. They are not an observed
dry run and not a measured result. Do not copy them into a real log as if
they were findings.

```text
date: EXAMPLE
task_id: EXAMPLE-STORY
spec_revision: EXAMPLE stories S1
evidence: EXAMPLE friction report item F1, trial T1
signature: assumed-setting-absent
response: environment
suggestion: EXAMPLE. Document the tax-mode setting the stories already assumed, without placing the tax procedure into the spec.
why: EXAMPLE. The calculation is inferable from the existing tax module. The missing setting is environment setup.
decision: pending
environment_ready: pending
lesson: EXAMPLE. Check documented setup before treating a missing setting as a story gap.

date: EXAMPLE
task_id: EXAMPLE-STORY
spec_revision: EXAMPLE stories S1
evidence: EXAMPLE friction report item F1, trial T1
signature: assumed-setting-absent
response: spec-change
suggestion: EXAMPLE. State which tax mode this environment uses, because the repository does not record that deployment choice.
why: EXAMPLE. The mode is hard to infer and depends on the environment.
decision: pending
environment_ready: not-applicable
lesson: EXAMPLE. Put an environment-dependent mode in the story when the repository does not already show it.
```
