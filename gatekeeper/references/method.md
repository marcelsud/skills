# The Depth Tree, v2

Leonxlnx created the Depth Tree. v1 assigned the full root budget to every
leaf and predicted effort of 2^(N-1) times the root budget. In six controlled
runs, tree 6 cost about 1.0 to 1.5 times tree 3 instead of 8 times.

v2 uses depth for decomposition. Per-leaf gates and fresh contexts control
completion.

## The rules

1. **Layer 1 is the task.** Split at natural joints, binary where useful,
   until layer N. Leaves contain the work. Higher layers decompose and
   integrate it.

2. **Keep each leaf substantial.** Give a leaf one deliverable, one gates
   file, and at least ten minutes of focused work. Merge smaller leaves.

3. **Set contracts before fan-out.** Record interfaces, data ownership,
   naming, and error conventions in PLAN.md. Two concurrent leaves cannot
   own the same file. Add a dependency when ownership must pass between
   leaves.

4. **Give leaves and branches gates.** Leaf gates verify a deliverable.
   Branch gates verify merged children, interface compatibility, end-to-end
   behavior, and sibling regressions.

5. **Use gates and review passes to finish a leaf.** Implement it, review it
   as a domain expert, find defects, and apply cheap refinements. Finish only
   when every gate has evidence and a complete pass finds no improvement.

## Where v2 enforces completion

| v1 said | v2 does |
|---|---|
| every leaf gets full budget T | every leaf gets a fresh context and its own gates |
| effort = 2^(N-1) x T | effort = whatever it takes to check every box with evidence |
| no report until done (prose) | stop-hook and ledger make early reports structurally visible |
| verify, do not trust yourself | CHECK commands run in the shell; parent re-runs them |

## Choosing N

- **Tree 2 or 3.** Use solo mode for a feature, bug hunt, or document. Work
  two to four leaves in one session.
- **Tree 4 or 5.** Use orchestrated mode for a subsystem, refactor, or
  serious review.
- **Tree 6 or 7.** Use orchestrated mode for a whole project. Give leaves
  different files, dispatch every ready leaf, and verify integration at each
  branch.

When the user gives no depth, pick the smallest N that separates the task's
deliverables. Add a layer only when a leaf still contains more than one
deliverable.
