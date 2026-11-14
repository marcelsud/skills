# History

Append one record after an actual requested judge review, including an
`inconclusive` outcome when the judge returned it. Do not append a judge
record when judging was not requested or remains pending because a requested
reviewer could not run. Those states have no scores or verdict. Friction
observations and spec-writer decisions still belong in the learnings log.

The history is a file or spreadsheet the user or project designates, such
as CSV or JSONL. Use the columns below. Do not create a database for this
workflow, and do not store the history in this skill.

If no location has been chosen, ask. Until the user names one, keep the
record in the conversation and do not claim it was persisted.

## Fields

| Field | Content |
| --- | --- |
| `date` | Date the verdict was recorded. |
| `task_id` | Task or story identifier. |
| `roles` | Actual spec author, trial implementer, delivery implementer, and judge, with evidence the judge did not author or implement either artifact. Known user-assigned model names may accompany participant identities; no model selection or invented identity is required. |
| `spec_revision` | Accepted specification location and revision. |
| `trial_revision` | Trial artifact location and revision used by the judge. |
| `delivery_revision` | Delivery artifact location and revision used by the judge. |
| `problems_found` | Short description of the dry-run frictions. |
| `root_cause` | Primary category: `env/config`, `spec gap`, `skill gap`, `tooling`, or `repo convention`. |
| `signature` | Stable problem-class label copied from the friction report. |
| `judge_scores` | Scores the actual judge supplied with citations; `unset` for dimensions whose evidence the judge found missing. |
| `verdict` | The actual judge's `improved`, `copied`, `regressed`, `mixed`, or `inconclusive` result. |
| `judge_evidence` | Citations and the rule supporting the judge's verdict, including missing material inputs for an `inconclusive` result. |
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
roles: EXAMPLE. Participant A wrote the stories and implemented both artifacts; participant B is an independent read-only judge with no authorship or implementation role.
spec_revision: EXAMPLE accepted stories revision S2
trial_revision: EXAMPLE disposable artifact T1
delivery_revision: EXAMPLE delivery artifact D1
problems_found: EXAMPLE. The stories assumed a setting the environment did not define, and the trial invented a default.
root_cause: env/config
signature: assumed-setting-absent
judge_scores: unset
verdict: inconclusive
judge_evidence: EXAMPLE. The supplied brief B1 lacks delivery test results, so the actual judge returned inconclusive under the missing-material-input rule.
action_taken: none
recurrence: false
rediscovered: none
```
