# Page patterns

Use the pattern that matches the reader's purpose. These are editorial choices,
not mandatory heading templates. Preserve established project conventions and
omit sections that do not help the task.

## Language and SDK variants

Use tabs when variants share the same goal, prerequisites, step order, and
explanation, with differences confined to short snippets or commands. Use
separate, cross-linked pages when installation, architecture, lifecycle, or the
number of steps differs materially. A reader should be able to follow one
variant from setup to success without stitching together incompatible tabs.
Keep shared conceptual explanations in one canonical place when practical.

Keep equivalent examples aligned on the same scenario, identifiers, and success
criteria. When behavior or an example changes, locate and review the affected
language and SDK variants together, including their version markers and outputs.
Verify each changed variant where possible; report untested variants and label
real support differences instead of forcing false parity.

## README or overview

Answer what the project does, who it serves, and when to choose it. Give a small
concrete example or result before an inventory of features. Show the supported
installation route and first useful action, or link directly to the canonical
quickstart when setup needs more room. Make status and material compatibility
constraints easy to find.

Route readers to learning material, task guides, reference, support, and
contribution instructions where these exist. Mention the actual license and
contribution process without inventing policies or support commitments. A
README is an entry point; it need not contain the whole manual.

## Quickstart

Choose one supported environment and one small outcome. State prerequisites,
then take the reader through install, create or configure, run, use, and verify
as the product requires. Keep required steps on one route. Offer another
language or runtime as an explicit variant rather than interleaving several
unrelated command sequences.

Choose tabs or separate pages using the language and SDK criteria above.

Show the files the reader edits and identify generated files. Explain whether a
command creates a project, starts a server, publishes code, or performs several
of these operations. Give the address, request, query, or output that confirms
success. Include stopping or cleanup instructions when the route leaves work
running or creates persistent resources. Link deeper explanations after the
first result; do not promise a completion time without evidence.

## Tutorial

Teach through a recognizable project with a stated end result. Explain what
the reader needs to know and what the tutorial will teach. Keep names, data,
paths, and assumptions consistent throughout the sequence.

Introduce a concept when the example first needs it. Each milestone should
produce something the reader can inspect before adding more complexity. Say
whether a later snippet replaces earlier code or adds to it. Clearly label
diffs and excerpts; make the complete resulting code available when incremental
edits would be hard to reconstruct. Close with what was built and a sensible
next extension, not an exhaustive feature tour.

## How-to guide or feature chapter

Name the goal and assumed starting state. Show the standard solution first,
then relevant variations and their selection criteria. For a feature chapter,
a useful progression is purpose, basic use, actual behavior, customization,
constraints, and links to exact reference entries. Use only the parts needed.

Place introduction, behavior-change, deprecation, and removal versions beside
the affected feature or option when relevant; link deprecated usage to the
supported replacement or migration guidance.

Explain prerequisites hidden in framework defaults: middleware, registration,
environment settings, generated bindings, or lifecycle hooks. Describe how
errors surface and how the result can be inspected. Include a second example
when it teaches a distinct decision, not merely a renamed version of the first.

## Concept explanation

Start with a concrete problem or question. Define the primitive and show its
relationship to familiar concepts without implying an exact equivalence where
semantics differ. Walk through one request, state transition, or lifecycle.
Identify ownership, execution location, and persistence boundaries when they
matter to behavior.

Explain tradeoffs, guarantees, and non-guarantees supported by the project.
Distinguish a deployment choice from an application concept. Link to a working
example and the relevant task guides. A diagram helps when relationships are
hard to hold in prose; decorative architecture boxes do not establish behavior.

## API, CLI, and configuration reference

Make entries consistent and independently understandable for readers arriving
from search. Group them by recognizable resource, command, or feature. State
the supported version and relevant platform or provider scope.

Choose the fields that define the interface:

| Reference | Useful fields |
| --- | --- |
| Function or method | Signature, inputs and types, requiredness, defaults, return value, async behavior, errors, side effects, minimal example |
| HTTP endpoint | Method and path, authentication, path/query/body fields, request and response examples, status codes, pagination or limits |
| CLI command | Purpose, invocation, arguments, flags and aliases, defaults, working context, output and exit behavior, examples |
| Configuration | Key and nesting, type, allowed values, default or absence behavior, requiredness, scope, precedence, interactions, example |

For every reference type, include relevant introduction, deprecation, and
removal versions, plus a link to the supported replacement or migration
instructions. Apply availability markers at the affected member, flag, or option
as well as the parent entry when their histories differ. Use release evidence
for version claims; if history or a replacement is unknown, report that gap
rather than inventing a version or implying that no alternative exists.

Include units for durations and sizes, and distinguish missing values from
empty values or explicit nulls when behavior differs. State precedence across
flags, environment variables, and files where relevant. Separate mutually
exclusive alternatives; do not present contradictory settings as one runnable
configuration. For each option, explain its effect rather than restating its
name. Link to a guide when an entry requires a multi-step workflow.

## Troubleshooting

Use headings readers can recognize from a symptom or exact error. Separate
similar symptoms with checks that discriminate between causes. A useful entry
connects symptom, likely cause, diagnostic evidence, remedy, and confirmation.
State preconditions instead of prescribing the same reset for every failure.

Prefer inspection before state-changing repair. Put concrete data loss,
credential replacement, or access consequences before the affected command.
Provide a preservation or recovery route where supported. Show the observation
that confirms the remedy. If escalation is needed, identify useful versions,
logs, and reproduction details without asking readers to disclose secrets.

## Upgrade or migration guide

Specify the starting and target versions and prerequisites. Distinguish
required breaking changes from optional adoption of new features. Organize
changes by recognizable subsystem or action; show before and after examples
when syntax or behavior changes.

For each material change, identify who is affected, what breaks, how to adapt,
and how to verify the adaptation. Include deployment ordering, data migration,
or rollback constraints when supported and relevant. Do not imply reversibility
where a format or schema change prevents it. Link to the target version's
canonical reference rather than reproducing the whole API.
