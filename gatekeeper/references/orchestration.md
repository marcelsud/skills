# Orchestrated mode

Use orchestrated mode for tree depth 4 or more or work that will outlast one
sitting. Each leaf gets a fresh subagent context. The main session schedules
and verifies the leaves.

## The driver loop

You (the main session) are the driver. You do not implement leaves; you
plan, dispatch, verify, and integrate.

1. **Plan.** Write PLAN.md with the contract, dependency graph, tree, and
   gates file for each leaf and branch. Start from templates/PLAN.md. This is
   the only step where the whole task must fit in one head. Name every
   unit's dependencies and file ownership before work starts.
2. **Dispatch the ready set.** A unit is ready when every listed dependency
   is verified, its gates and brief exist, and it is neither running nor
   verified. Compute the complete ready set and spawn every ready leaf at
   once, in one fan-out. Do not launch one leaf when two or more are ready.
   Each subagent's entire brief is:
   - the contract section of PLAN.md, not the whole file or your history
   - its own gates file, verbatim
   - the instruction to work the four passes until every gate has evidence,
     then stop; if a gate is impossible, ABANDON it with a reason.
3. **Verify each return.** As each leaf returns, verify it at once. Do not
   wait for unrelated in-flight leaves if the harness reports completions
   separately. Run
   `node <skill-dir>/scripts/gate-check.mjs --verify gates/leaf-x.md`.
   This reruns every CHECK and reopens any gate that fails. Inspect each
   manual gate's evidence directly. Send the leaf back with every unmet gate
   named. A returned leaf unblocks nothing until parent verification passes.
4. **Replenish the ready set.** After each successful verification, append
   the event to PLAN.md, mark the unit verified, recompute the ready set, and
   dispatch every newly ready unit. Do this while unrelated siblings remain
   in flight. Never wait for a whole wave to finish before filling newly
   opened work.
5. **Integrate through the same scheduler.** A branch integration node
   becomes ready when all listed children are verified. Work its gates
   yourself or dispatch an integration leaf. Verify it, then recompute what
   it unblocks.
6. **Report.** Report only when the root gates pass. Paste the ledger, N of N,
   surface every ABANDON line, and re-measure every number you state.

## Parallelism

Eager scheduling is the default. Launch the whole ready set, verify
completions separately, and dispatch newly unblocked work at once. Serialize
only a real dependency. If the harness has a hard concurrency cap, fill
every slot and dispatch the next ready unit when a slot opens.

The plan must make ready leaves safe to run together. They own different
files, and the contract fixes shared interfaces before dispatch. If two
units need the same file or one consumes the other's output, record that
ordering as a dependency. Parallel work saves wall-clock time, but it never
weakens parent verification.

## Verification hierarchy

Use all three verification layers:

1. **Leaf self-check.** The leaf runs gate-check. This catches incomplete
   work but cannot validate the leaf's own judgment.
2. **Parent re-run.** The driver runs the checks again. This catches false
   self-certification and environment differences.
3. **Stop hook.** In Claude Code, the optional hook blocks completion while
   gates remain unmet.

Write a CHECK command for any judgment that the driver would otherwise
repeat by reading.

## Model and effort tiering

Use a cheaper model or lower reasoning effort for mechanical leaves such as
renames, fixture generation, and application of a fixed pattern. Keep design,
integration, and parent verification on the strongest available model. The
driver also stays on that model.

## When to stay solo

Stay solo for work under about half an hour. Use one `GATES.md` in one
session and skip subagent dispatch.
