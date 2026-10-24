# skills

Agent skills maintained by [@marcelsud](https://github.com/marcelsud). Each
directory is one skill: `SKILL.md` plus optional `references/`, `templates/`,
`scripts/`, and `agents/` files.

## Skills

| Skill | Purpose |
| --- | --- |
| `fusion` | Run two user-selected models on one prompt and reconcile the answers. |
| `gatekeeper` | Completion gates and the Depth Tree for long tasks. Fork of `Leonxlnx/unlazy`. |
| `memory-sql` | Persist and selectively recall project facts, decisions, tasks, and evidence through SQLite. |
| `prep-dev` | Examine the premise and clarify implementation through a short interview. |
| `prep-pr` | Assess implemented changes and prepare an evidence-backed review handoff. |
| `sheriff` | Review code changes and triage issues by evidence and risk. |
| `spec-gap` | Compare code with product requirements; score coverage and identify gaps and extras. |
| `unit-tests` | Evaluate test relevance and protect business use cases and domain invariants in any language. |
| `warden` | Gate changes: intent, review, test, document, lint, then ship. |

## Install

```bash
npx skills add marcelsud/skills --skill <name> -g -y
```

Install one skill at a time. The published repository is the source; the
package name is the directory name.

## Working in this repository

Nothing here is loaded automatically. Agents resolve skills by name from their
own roots, and an installed copy of the same name can win over this checkout, so
a local edit stays invisible until the installed copy is replaced. To run from
the checkout directly, link the skill directory instead of copying it:

```bash
ln -sfn "$PWD/<name>" "$HOME/.agents/skills/<name>"
```

Before debugging an instruction that appears not to work, confirm which copy an
agent resolves (in OMP, a read of `skill://<name>` shows the loaded text and its
frontmatter). Keep one copy per skill name: two installed copies diverge
silently, and the shadowed one keeps looking current here.
