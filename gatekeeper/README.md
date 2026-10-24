<div align="center">

# gatekeeper

**Completion gates for long AI-agent tasks.**

v2 writes acceptance gates to files, runs their checks as commands, and can
block Claude Code from stopping while gates remain unmet.

The markdown workflow works with Claude Code, OpenAI Codex, Cursor, and other
agents that read `SKILL.md`. The optional Stop hook works only in Claude Code.

[Use it](#use-it) · [What changed in v2](#what-changed-in-v2-and-why) · [How it works](#how-it-works) · [The method](#the-depth-tree-v2) · [Cost](#cost) · [Research](#the-research)

</div>

---

## Use it

Install the skill, then invoke it in plain language. It can also trigger from its description.

```
/gatekeeper tree 5 refactor the payment module
```

```
tree 3 build the landing page and do not stop until every gate is checked
```

`tree N` sets decomposition depth. Each leaf has one deliverable and one gates file. Use tree 2 or 3 for a feature or bug hunt, tree 4 or 5 for a subsystem, and tree 6 or 7 for a whole project. In orchestrated mode, the driver dispatches every ready leaf, verifies each return, and immediately dispatches newly unblocked work.

### Install

Use the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add marcelsud/skills --skill gatekeeper
```

Add `-g` for a user-level install. Target one agent when needed:

```bash
npx skills add marcelsud/skills --skill gatekeeper --agent claude-code
npx skills add marcelsud/skills --skill gatekeeper --agent codex
```

The CLI also accepts the skill directory directly:

```bash
npx skills add https://github.com/marcelsud/skills/tree/main/gatekeeper
```

Without the CLI, copy the `gatekeeper/` directory into the agent's skills
directory. Gates and scripts require Node 16 or later.

### Hard mode (Claude Code, optional)

In Claude Code, the optional Stop hook blocks the turn while gates remain unmet.

```bash
node <path-to-skill>/scripts/install-hooks.mjs            # this project only (settings.local.json)
node <path-to-skill>/scripts/install-hooks.mjs --global   # every project
node <path-to-skill>/scripts/install-hooks.mjs --uninstall
```

The hook scans files without a model call. After six blocked stops with no gate-file change, it releases the turn with a warning. An `ABANDON: <gate> <reason>` line also releases that gate. Add `.gatekeeper-hook-state.json` to `.gitignore`.

### Or let your agent install it

Paste this to Claude Code, Codex, Cursor or any agent with shell access:

```
Install the "gatekeeper" skill from
https://github.com/marcelsud/skills/tree/main/gatekeeper so it is available in
future sessions.

Try `npx skills add marcelsud/skills --skill gatekeeper -y` first. If that is
unavailable, copy the repository's `gatekeeper/` directory into your skills
directory.

Then confirm it worked: show me the installed path and the first line of the
skill's description. Do not tell me it is installed unless you have actually
verified the file is on disk.
```

## What changed in v2, and why

The original single-file skill is preserved unchanged on the [v1 branch](https://github.com/Leonxlnx/unlazy/tree/v1) if you want the instructions-only version with zero moving parts.

v1 was tested in six fresh sessions. The test used two build tasks, three
conditions, one model, and the same prompt body. Independent agents reviewed
the code, reran checks, and exercised the result in a browser.

| Finding | Change in v2 |
|---|---|
| Baselines had no placeholders or console errors | Remove rules aimed only at visible stubs |
| Skill runs used 1.6 to 3.9 times more output and fixed 4 to 10 defects before delivery | Keep the review passes and gates |
| Tree 6 cost 1.0 to 1.5 times tree 3 | Use depth for decomposition, not effort arithmetic |
| One baseline failed live testing after claiming the case worked | Require runnable CHECK and EXPECT gates |
| Every skill run reported 1 to 3 wrong numbers | Re-measure report numbers |

v2 verifies completion at five levels:

1. `SKILL.md` defines the work rules.
2. Gate files preserve the acceptance criteria.
3. `gate-check.mjs` runs repeatable checks.
4. The parent uses `gate-check.mjs --verify` to rerun every leaf CHECK.
5. The optional Stop hook blocks completion while gates remain unmet.

## How it works

Before real work starts, the agent writes its acceptance gates to a file:

```markdown
# Gates: pricing section

- [ ] G1: three tiers render with real copy
  CHECK: node check.js pricing --tiers
  EXPECT: 3/3 tiers ok
  EVIDENCE: pending

- [ ] G2: annual toggle changes both price and label
  CHECK: node check.js pricing --toggle
  EXPECT: toggle ok
  EVIDENCE: pending
```

`gate-check.mjs` runs each CHECK command. It checks a box only when EXPECT
matches and records the deciding output. `--verify` reruns every CHECK for
parent verification and reopens failed gates. Pending evidence keeps a gate
open. A present gate file with no valid gates or a malformed checkbox is a
parse error, and the Stop hook blocks on the same condition.

The final report includes the completed ledger and re-measured counts.

For tree 4 or more, `PLAN.md` records contracts, dependencies, and file
ownership. Each leaf and branch gets a gates file. The driver launches every
ready leaf, verifies each return with `--verify`, and dispatches newly
unblocked work without waiting for unrelated leaves.

## The Depth Tree, v2

Created by [Leonxlnx](https://github.com/Leonxlnx).

1. **Split at natural joints.** Leaves contain work. Branches decompose and
   integrate it.
2. **Keep leaves substantial.** Give each leaf at least ten minutes of work,
   one deliverable, and one gates file.
3. **Set contracts before fan-out.** Record interfaces, dependencies, and
   file ownership in PLAN.md.
4. **Verify branches.** Branch gates test merged children and end-to-end
   behavior.
5. **Finish from evidence.** Every gate must pass, and a complete review must
   find no further change.

See [references/method.md](references/method.md),
[references/gates.md](references/gates.md), and
[references/orchestration.md](references/orchestration.md).

## Cost

The controlled runs measured:

- Solo gate discipline added a few hundred prompt tokens and produced 1.5 to
  4 times the baseline output on the tested tasks.
- The Stop hook uses no model calls.
- Orchestrated cost grows with leaf count. Use it only for substantial work.
- Command checks replace repeated model review.

## What is in the repo

```
SKILL.md                       the skill: rule zero, modes, tree v2, report audit
references/
  method.md                    the Depth Tree v2 in full
  gates.md                     gate file format spec and writing guide
  orchestration.md             ready-set dispatch and parent verification
  token-economy.md             measured cost controls
templates/
  PLAN.md                      contract + dependency graph + tree + status log
  gates-leaf.md                per-leaf gates
  gates-node.md                per-branch integration gates
scripts/
  gate-check.mjs               runs CHECK commands, flips boxes, records evidence
  stop-hook.mjs                Claude Code Stop hook: blocks stop while gates unmet
  install-hooks.mjs            idempotent hook install/uninstall
```

All scripts are zero-dependency Node 16+, tested on Windows and POSIX shells.

## Why the skill exists

Recent work measures several completion failures:

- Detailed multi-part prompts often receive partial responses
  ([Quantifying Laziness, arXiv 2512.20662](https://arxiv.org/abs/2512.20662)).
- Reasoning models stop useful lines of thought early
  ([Thoughts Are All Over the Place, arXiv 2501.18585](https://arxiv.org/abs/2501.18585)).
  They can also spend too much compute before acting
  ([When More Thinking Hurts, arXiv 2604.10739](https://arxiv.org/abs/2604.10739)).
- Coding-agent quality falls during long iterative work
  ([SlopCodeBench, arXiv 2603.24755](https://arxiv.org/abs/2603.24755)).
- Agents may stop early when they misjudge their remaining context
  ([Context Anxiety](https://inkeep.com/blog/context-anxiety)).

The project's six-run test found correct work paired with premature completion
and inaccurate report counts. Gate files address early completion. The report
audit addresses inaccurate counts.

Effort also responds to structure. Budget forcing improved competition-math
scores in the s1 study
([arXiv 2501.19393](https://arxiv.org/abs/2501.19393)). Aider measured fewer
lazy coding responses after switching to unified diffs
([results](https://aider.chat/docs/unified-diffs.html)).

## The research

Sources are listed by date, newest first.

- [Fortune: Advanced AI is showing signs of laziness](https://fortune.com/2026/07/28/advanced-ai-models-laziness-open-ai-anthropic/) (July 2026)
- [When More Thinking Hurts: Overthinking in LLM Test-Time Compute Scaling](https://arxiv.org/abs/2604.10739) (April 2026)
- [SlopCodeBench: How Coding Agents Degrade Over Long-Horizon Iterative Tasks](https://arxiv.org/abs/2603.24755) (March 2026)
- [METR Time Horizon 1.1](https://metr.org/blog/2026-1-29-time-horizon-1-1/) (January 2026)
- [Quantifying Laziness, Decoding Suboptimality, and Context Degradation in LLMs](https://arxiv.org/abs/2512.20662) (December 2025)
- [OptimalThinkingBench: Evaluating Over and Underthinking in LLMs](https://arxiv.org/abs/2508.13141) (ICLR 2026, August 2025)
- [Context Anxiety: How AI Agents Panic About Their Perceived Context Windows](https://inkeep.com/blog/context-anxiety) (2025)
- [Measuring AI Ability to Complete Long Tasks](https://arxiv.org/abs/2503.14499) (METR, March 2025)
- [Thoughts Are All Over the Place: On the Underthinking of o1-Like LLMs](https://arxiv.org/abs/2501.18585) (January 2025)
- [s1: Simple test-time scaling](https://arxiv.org/abs/2501.19393) (January 2025)
- ["Should I Give Up Now?" Investigating LLM Pitfalls in Software Engineering](https://arxiv.org/abs/2411.09916) (2024, updated 2025)
- [Unified diffs make GPT-4 Turbo 3x less lazy](https://aider.chat/docs/unified-diffs.html) (aider)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request. Behavioral claims need current sources, and changes must keep enforcement structural.

## License

[MIT](LICENSE)
