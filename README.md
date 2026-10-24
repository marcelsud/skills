# skills

Agent skills maintained by [@marcelsud](https://github.com/marcelsud). Each
directory contains a SKILL.md entrypoint and any supporting prose references.
The workflows are independent of agent harnesses: they describe outcomes,
decisions, and verification without requiring a particular tool API, command
syntax, installation path, or runtime configuration.

## Skills

Grouped by their role in the software development lifecycle.

### Plan

| Skill | Purpose |
| --- | --- |
| `prep-dev` | Examine the premise and clarify implementation through a short interview. |
| `fusion` | Run two user-selected models on one prompt and reconcile the answers. |

### Test

| Skill | Purpose |
| --- | --- |
| `unit-tests` | Evaluate test relevance and protect business use cases and domain invariants in any language. |

### Review

| Skill | Purpose |
| --- | --- |
| `spec-gap` | Compare code with product requirements; score coverage and identify gaps and extras. |
| `sheriff` | Review code changes and triage issues by evidence and risk. |
| `prep-pr` | Assess implemented changes and prepare an evidence-backed review handoff. |

### Ship

| Skill | Purpose |
| --- | --- |
| `warden` | Validate intent, review, tests, documentation, and lint; then deliver within the authorized scope. |

### General

| Skill | Purpose |
| --- | --- |
| `gatekeeper` | Acceptance criteria, evidence, and the Depth Tree for substantial tasks. Fork of `Leonxlnx/unlazy`. |
| `memory-sql` | Persist and selectively recall project facts, decisions, tasks, and evidence through SQLite. |

## Use

Load the chosen skill through your environment's supported skill mechanism,
or provide its entrypoint directly. Keep linked reference documents available
and read them when the workflow calls for them. The directory name identifies
the skill.

Standard frontmatter supplies the skill's name and description, with license
and attribution where applicable. The remaining content describes the workflow
in prose. There are no bundled scripts, database schemas, hooks, or
harness-specific metadata files.

Use the execution capabilities available in the current environment. Some
tasks still need capabilities inherent to their purpose: memory-sql uses
SQLite, fusion needs analyses from the two selected models, and a required
independent review needs a separate reviewer. Report unavailable capabilities
without claiming the corresponding work or verification passed.

## Working in this repository

Before testing an edit, confirm which copy of the skill the environment
actually loads. A separately installed copy can hide changes made in this
checkout. Use the environment's supported way to load or refresh local
instructions and avoid divergent copies of the same skill.

Preserve each workflow's intent, evidence requirements, and authorization
boundaries when editing it. Describe capability requirements in ordinary
language and leave their implementation to the environment. Keep references
current and retain applicable license attribution.
