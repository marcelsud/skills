# History

Append one record after delivery, including a skipped judge and a verdict
of `inconclusive`. The history is a file or spreadsheet the user or the
project designates, such as CSV or JSONL. Use the columns below. Do not
create a database for this workflow, and do not store the history in this
skill.

If no location has been chosen, ask. Until the user names one, keep the
record in the conversation and do not claim it was persisted.

## Fields

| Field | Content |
| --- | --- |
| `date` | Date the verdict was recorded. |
| `task_id` | Task or story identifier. |
| `roles` | Who filled the spec author, the implementer, and the judge: `same-session`, `independent`, or `skipped`. Do not record a model name. |
| `problems_found` | Short description of the dry-run frictions. |
| `root_cause` | Primary category: `env/config`, `spec gap`, `skill gap`, `tooling`, or `repo convention`. |
| `signature` | Stable problem-class label copied from the friction report. |
| `judge_scores` | The five rubric scores, or `unset` when the judge did not run. |
| `verdict` | `improved`, `copied`, `regressed`, `mixed`, `inconclusive`, or `skipped`. |
| `action_taken` | The process change that followed, such as a skill update, a spec-template update, an environment prepared for the next iteration, or a learnings-log lesson the spec writer will reuse. Use `none` when no process change was made. |
| `recurrence` | `true`, `false`, or `unknown`. |
| `rediscovered` | Frictions from this task's dry run that appeared again during delivery, or `none`. |

A record may summarize several frictions. It still has one primary root
cause and one signature. When two primary causes would hide a later match,
append one record per primary signature.

## Recurrence

Before appending, search the history for the same `root_cause` and
`signature`.

- Set `recurrence` to `false` when no earlier record matches, or when every
  match has `action_taken` of `none`.
- Set `recurrence` to `true` when an earlier match records a process action
  and the same class has appeared again. The recorded fix did not hold.
  The next action updates the skill, the spec template, or the environment
  setup again. A patch limited to the current task does not clear the flag.
- Set `recurrence` to `unknown` when the history cannot be read. Do not
  treat an unreadable history as `false`.

Reuse the existing signature for that class. A renamed signature that
points at the same gap is still a recurrence; correct the label instead of
starting a new series.

## Example

The following record shows the field shape only. It is not an observed dry
run, not a measured score, and not a benchmark. Do not copy it into a real
history as if it were a result.

```text
date: EXAMPLE
task_id: EXAMPLE-STORY
roles: spec_author=same-session; implementer=same-session; judge=skipped
problems_found: EXAMPLE. The stories assumed a setting the environment did not define, and the trial invented a default.
root_cause: env/config
signature: assumed-setting-absent
judge_scores: unset
verdict: skipped
action_taken: none
recurrence: false
rediscovered: none
```
