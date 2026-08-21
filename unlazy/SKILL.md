---
name: unlazy
description: Completion discipline for substantial tasks. Use when work returns half done, an agent reports completion too early, the output must be exhaustive, or a long run keeps stalling near the end. Also use for /unlazy, "tree N", "gates", or "do not stop until it is done". v2 records acceptance criteria in gate files and checks them with commands. Its Depth Tree splits work into independently verified leaves.
license: MIT
metadata:
  author: Leonxlnx
  source: https://github.com/Leonxlnx/unlazy
  version: 2.0.0
---

# Unlazy

Use this skill to prevent incomplete delivery, narrowed scope, and inaccurate
final reports during substantial work.

Tests of v1 found that instructions increased effort but did not prevent
wrong report counts or early completion. v2 records acceptance criteria in
files and checks them with commands. Completion comes from the ledger, not
the agent's confidence.

## Rule zero: gates before work

Before real work, write the acceptance gates to `GATES.md` in the working
directory. Use [templates/gates-leaf.md](templates/gates-leaf.md). Add one
checkbox per required outcome. Add `CHECK:` and `EXPECT:` lines whenever a
command can verify the outcome.

The file preserves the original acceptance criteria through long sessions.

Run the checker. Completion requires every box to have evidence.

```
node <this-skill-dir>/scripts/gate-check.mjs GATES.md
```

Check manual gates by replacing `EVIDENCE: pending` with a measurement,
deciding output, or an exact `file:line`. A checked box with pending evidence
is still unmet.

If a gate becomes impossible, keep it in the file and add
`ABANDON: <gate id> <reason>`. Include every abandoned gate in the final
report.

## Pick a mode

**Solo** (default). Use one `GATES.md` for work under about half an hour or tree depth 3 or less. Finish every gate, then include the ledger in the report.

**Orchestrated**. Use this for tree depth 4 or more, or any build that will
outlast one sitting. Decompose it with
[references/method.md](references/method.md). Write `PLAN.md`, including the
dependency graph, plus one gates file per leaf under `gates/`. The driver
launches every ready leaf in one fan-out. When a leaf returns, the driver
uses `gate-check.mjs --verify` to rerun every CHECK and inspects manual
evidence. Only a verified leaf unblocks dependents, which dispatch even while
other leaves remain in flight. Read
[references/orchestration.md](references/orchestration.md) before dispatch.

## The Depth Tree, v2

Leonxlnx created the Depth Tree. v2 uses it only for decomposition.

1. **Split at natural joints.** Layer 1 is the task. Leaves contain the work.
2. **Keep leaves substantial.** Each leaf should contain at least ten minutes
   of focused work and one deliverable. Merge leaves that are smaller.
3. **Fix contracts before dispatch.** Record shared interfaces, ownership,
   and naming in `PLAN.md`.
4. **Verify branches.** Give each internal node integration gates for merged
   children, interfaces, and end-to-end checks.
5. **Finish from evidence.** A leaf is done after its gates pass and a full
   review finds no further change.

Use tree 2 or 3 for a feature, bug hunt, or document in solo mode. Use tree 4
or 5 for a subsystem or serious refactor. Use tree 6 or 7 for a whole
project, with disjoint leaves and eager dispatch of every ready unit.

## Work each leaf in passes

1. **Implement the whole deliverable.** Leave no placeholders or unfinished
   paths.
2. **Review it as a domain expert.** Replace shortcuts that weaken the
   required outcome.
3. **Find and fix defects.** Check edge cases, correctness, and performance.
4. **Apply cheap refinements.** Improve details that need no new scope.

Stop only after a complete pass finds no improvement and every gate has
evidence.

## Report audit

The controlled runs most often failed in the final report. The work was
correct, but counts stated from memory were wrong.

Re-measure every number before reporting it, or mark it unverified. Include
the ledger and its checked count.

## Behavioral rules

Keep these rules from v1:

- **Do not report with open gates.** Open the gates file and work the next
  unmet gate.
- **Check before concluding.** Run gate-check, then try to disprove the
  evidence for one passed gate.
- **Finish the current approach.** Before switching, state what remains and
  why the new approach is better.
- **Run cheap, reversible actions.** Observe the result instead of predicting
  it.
- **Record limits.** If an external limit blocks completion, list the
  remaining gates and add an ABANDON reason to each blocked gate.
- **Count complete sweeps.** If the task names 80 files, open all 80 and
  report the measured count. Declare any sampling.

## Token economy

Keep the checks cheap:

- Run shell commands instead of re-reading completed work.
- Record only the output that decides the gate.
- Give a leaf only the contract and its gates file.
- Append to the `PLAN.md` status log.
- Use a cheaper model for mechanical leaves when the runtime permits it.
- Stay solo for work under about half an hour.

## Hard enforcement (Claude Code, optional)

For Claude Code, the optional Stop hook blocks the turn while `GATES.md` or
`gates/*.md` has unchecked boxes or pending evidence. An ABANDON line
releases the corresponding gate.

The hook changes runtime behavior. Never install it without asking. Offer it
once when the task needs hard enforcement:

```
node <this-skill-dir>/scripts/install-hooks.mjs
```

Tell the user what the hook does and how to remove it with `--uninstall`.
The rest of the skill works in any runtime that reads markdown.

## What this skill does not cover

Use normal effort for conversation, factual questions, and trivial edits. A
one-line fix does not need a gates file. Use the tree only when the task
benefits from explicit decomposition and verification.
