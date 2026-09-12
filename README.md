# skills

Agent skills maintained by [@marcelsud](https://github.com/marcelsud). Each
directory is one skill: `SKILL.md` plus optional `references/`, `templates/`,
`scripts/`, and `agents/` files.

## Skills

| Skill | Purpose |
| --- | --- |
| `align-json-examples` | Format and vertically align JSON or JSONC examples in Markdown and chat. |
| `codebase-design` | Shared vocabulary for deep modules: interface, depth, seam, adapter, locality. |
| `domain-modeling` | Maintain `CONTEXT.md` and `docs/adr/`; pin down the project's language. |
| `fusion` | Run two user-selected models on one prompt and reconcile the answers. |
| `grade-code-review` | Grade code review findings by severity, confidence, and exposure. |
| `grade-issue-review` | Triage issue batches: duplicates, resolved reports, unsupported claims. |
| `improve-codebase-architecture` | Find deepening candidates and present the HTML report. |
| `make-no-mistakes` | Gate changes: intent, review, test, document, lint, then ship. |
| `omp-unlazy-workers` | Drive unlazy completion gates with model-selected worker sessions. |
| `omp-worker` | Delegate to fresh OMP sessions with explicit model selectors. |
| `sonarqube-code-analysis` | Local SonarQube scans turned into evidence-backed findings. |
| `unlazy` | Completion gates and the Depth Tree for long tasks. Fork of `Leonxlnx/unlazy`. |

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
