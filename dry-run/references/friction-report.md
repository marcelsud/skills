# Friction report

The dry run's artifact. Write it while the trial is underway and finish it
before the trial workspace is discarded. Cite the trial diff when it shows
a friction. The diff itself is not the report.

The implementer records the observations and evidence. The spec author
fills the judgment on each item. The implementer does not answer the
spec-author questions.

## Identify the trial

Record:

- The task or story id.
- The specification the implementer actually used, with its location and
  revision. Quote the clauses that later items rely on.
- The isolation used: a disposable branch or git worktree, and confirmation
  that it is not the delivery branch.
- Who actually wrote the stories and implemented the trial. Preserve any
  explicit participant or model assignments; identifying those actors does
  not require choosing models dynamically.
- The environment the trial exercised, including settings that were present
  and settings the stories assumed.
- The checks that ran and their observed results. State which claimed
  checks did not run.

## Record each friction

Use one item per distinct problem. A trial that reaches a passing result
still reports assumptions the stories left unspoken and behavior the
implementer had to invent.

Each item has:

- **Observation.** What was missing, ambiguous, broken, or assumed by the
  specification and absent from the repository or environment.
- **Evidence.** Where it appeared. Cite a story clause, a file and line, a
  missing setting, or an observed failure. Quote the specification or state
  that it is silent.
- **Kind.** One of `missing`, `ambiguous`, `broken`, or `assumed-absent`.
- **Root cause.** One primary category: `env/config`, `spec gap`,
  `skill gap`, `tooling`, or `repo convention`. Add a second category only
  when it has its own evidence.
- **Signature.** A short stable label for the problem class, such as
  `assumed-setting-absent` or `story-contradiction`. Reuse a signature
  already present in history when it is the same class. The task id is not
  a signature, and a new wording for an old class hides recurrence.
- **Spec-author judgment.** Completed after the trial, by the spec author:
  - whether the specification was incomplete, contradictory, naive, or
    adequate for this item;
  - whether the implementer deviated from the specification, or the
    specification left no other faithful option;
  - whether a skill, tool, or environment setting is missing, and its name.
    Record a setting's name, never a secret value.

## State the limits

List what the trial did not exercise. Keep preferences out of the item
list. An implementer's unforced choice is a deviation, not a new
requirement.

Do not turn these items into specification edits in this report. The
suggestion stage separates spec changes, additional context, and
environment preparation. See
[suggestions and learnings](suggestions.md).

## Keep secrets out

Name missing configuration. Do not record secret values, tokens, or other
private data. Do not reconstruct a secret from its name.
