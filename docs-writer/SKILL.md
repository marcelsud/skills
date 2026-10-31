---
name: docs-writer
description: Write, revise, or review developer documentation for open source software, including READMEs, quickstarts, tutorials, how-to guides, concepts, API and configuration references, troubleshooting, and upgrade guides. Use when documenting a project or feature, improving onboarding, or checking docs against implementation; not for general prose or marketing copy.
---

# Docs Writer

Help a developer reach a working result, understand the behavior that matters,
and find exact details later. Teach the supported software as it exists.

This workflow draws on Laravel, Symfony, Rivet, SpacetimeDB, and Serverless
Framework. Read [source analysis](references/source-analysis.md) when the
reasoning or a particular site's approach matters. Their product commands and
formatting conventions are examples, not defaults for another project.

## Establish the documentation contract

Inspect the requested scope, nearby docs, contribution rules, navigation,
documentation tooling, and supported releases. Preserve the project's language,
markup, terminology, and URL conventions. A request for one page does not imply
a new documentation framework or a site-wide rewrite.

Identify the reader, their starting knowledge and environment, the task they
want to complete, and observable success. Infer these from available project
evidence; ask only when a missing fact materially changes the instructions.

Ground technical claims in the target revision's public interfaces, schemas,
command help, tests, examples, and release notes. Verify external dependency
behavior against its relevant version. Distinguish intended behavior from
observed implementation when they disagree; report the discrepancy rather
than silently blessing a bug or documenting a promised feature as available.
Do not invent commands, defaults, guarantees, platforms, or compatibility.

## Choose the reader's route

Choose a primary purpose before outlining. Use
[page patterns](references/page-patterns.md) for the selected deliverable:

| Reader's need | Deliverable |
| --- | --- |
| Decide what this project does and where to start | README or overview |
| Reach a first working result | Quickstart |
| Learn through a complete guided example | Tutorial |
| Complete a specific task in an existing project | How-to guide |
| Understand a mechanism or design tradeoff | Concept explanation |
| Look up exact syntax and behavior | API, CLI, or configuration reference |
| Diagnose and resolve a failure | Troubleshooting |
| Move between supported versions | Upgrade or migration guide |

A feature chapter can offer both a guided example and a reference if the
transition is explicit and headings make either easy to find. Keep exhaustive
option lists out of the first-run path; link to their canonical home.

For a documentation set, organize around reader tasks and concepts rather than
mirroring source directories. Provide a clear entry route, recognizable topic
names, and links from first use to deeper guides and reference material. Add
only the pages and navigation changes justified by the requested scope. When
adding or moving a page, update the project's sidebar or navigation config,
landing-page indexes, and agent-facing indexes such as `llms.txt` where these
exist. Update generator inputs and regenerate derived indexes through the
project's normal process. Keep existing anchors stable where practical; update
redirect rules and incoming links when routes change.

## Build the explanation around a working example

Open with what the reader will accomplish or what the feature does. Give enough
context to choose it before introducing internal machinery. Put requirements
before the step that needs them: versions, installed packages, credentials,
permissions, running services, and whether the reader starts from a fresh or
existing project. Distinguish required setup from optional conveniences.

Use one coherent example with meaningful names. Introduce the smallest complete
case, explain its behavior, then extend one decision at a time. Show the
recommended approach first and explain when an alternative is useful. Mark
optional paths so readers know whether they can continue without them.

For each consequential step, connect the action to its purpose, show the code
or command, and state the expected result. Explain automatic behavior that
would otherwise look like missing work: generated files, loaded configuration,
persisted state, redirects, background processes, or client synchronization.
Put failure behavior and relevant limits beside the feature they constrain.

Mark relevant introduction, behavior-change, deprecation, and removal versions
beside affected features or options using the project's conventions. Link a
deprecation to its supported replacement or migration route; state when no
replacement exists only if the project confirms that. Never infer availability
from the version selector alone.

Examples should survive copying into the stated environment:

- Name the file and location, required imports, and insertion or replacement
  point. Keep identifiers consistent across server, client, config, and output.
- State the working directory and shell when they affect a command. Separate
  commands from output, and explain placeholders and where their values come
  from. Use supported platform variants when their syntax actually differs.
- Include the setup needed for the demonstrated behavior. Use omissions only
  in clearly identified excerpts; never hide required logic inside a block
  presented as a complete runnable example.
- Explain which process keeps running, when another terminal is needed, and how
  to stop or clean up resources the example creates. Identify local-only
  shortcuts and the changes required before production use when relevant.
- Use non-secret sample values and environment-variable references. Explain
  destructive effects, access changes, or billable provisioning before the
  corresponding reader action, with recovery or cleanup when applicable.

Code demonstrates the feature; surrounding prose explains the decisions and
results. Avoid narrating every line. End a learning route with a success check
and the next useful task, concept, or reference link.

## Write for scanning and reuse

Address the reader as "you" and give direct instructions. Prefer concrete
verbs and precise nouns. Remove hype, filler, and claims that a step is
"obvious," "easy," or "just" a matter of doing something. Define unfamiliar
terms at first use, use one name per concept, and preserve public identifiers
exactly.

Make headings describe tasks or recognizable concepts. Use numbered steps when
order matters, tables when entries share comparable fields, and code fences
with the correct language. Keep paragraphs focused. Follow established heading
case, punctuation, line wrapping, and callout syntax rather than importing one
source site's formatting rules.

Use notes for surprising behavior, tips for optional improvements, and warnings
for concrete consequences. Essential instructions belong in the main flow.
Add diagrams only when they clarify relationships, lifecycle, or data flow;
provide useful alternative text and explain the important relationships in
prose. Use descriptive links to specific pages or sections instead of vague
"click here" links or duplicated explanations.

## Verify and deliver

Walk through the edited route from its stated starting point. Check that each
prerequisite precedes use, every introduced identifier is defined, steps remain
in order, and the success check demonstrates the promised result.

Run relevant examples in a disposable local environment when available and
within scope. Compare observed results with the documented output. For
services, credentials, or effects that cannot be exercised, check signatures,
schemas, command help, and existing tests, and report the remaining uncertainty.
Do not execute a deployment or destructive example merely to validate prose.

Use the project's documentation build, link checks, and other relevant checks
when available. Check changed links and anchors, snippet syntax, sidebar and
agent-index discovery, redirects, version markers, and rendering of tabs,
callouts, tables, and diagrams. Check affected language and SDK variants together
as described in the page patterns. A spelling pass alone does not verify
instructions; a successful site build does not prove examples.

When behavior changes, find and update affected onboarding examples and
canonical references within scope, keeping release-specific guidance explicit.
Avoid mixing versions or hand-editing generated reference output when the
project expects changes to its source. Surface any necessary follow-up outside
the authorized scope.

For an authoring request, deliver the actual documentation changes and a brief
account of what was verified and what remains untested. For review-only work,
report actionable reader obstacles with locations, consequences, and concrete
fixes without rewriting unrelated pages. Distinguish verified output from
illustrative output. Do not claim a walkthrough, build, or link check ran unless
it did.
