---
name: gatekeeper
description: Keep substantial tasks tied to explicit acceptance criteria and verified evidence. Use when work returns half done, reports completion too early, needs exhaustive coverage, or benefits from a depth tree of independently verifiable deliverables.
license: MIT
metadata:
  author: Leonxlnx
  maintainer: marcelsud
  source: https://github.com/marcelsud/skills/tree/main/gatekeeper
  upstream: https://github.com/Leonxlnx/unlazy
---

# Gatekeeper

Prevent incomplete delivery, narrowed scope, and inaccurate final reports by
tracking required outcomes and checking their evidence before declaring success.
Use normal effort for conversation, factual questions, and trivial edits.

## Establish completion criteria

Before substantial work, translate the user's intent into observable outcomes.
For each outcome, record how it will be checked, what success means, its current
status, and the evidence observed. Use an existing task record, a conversation
checklist, or a project document appropriate to the task. No particular filename
or record format is required.

Preserve the original scope and acceptance criteria through later sessions.
A completed status without decisive evidence remains an unmet criterion.
Read [gates.md](references/gates.md) when defining or assessing criteria.

## Choose the smallest useful decomposition

Work alone for a focused task. For a larger task, split it at natural boundaries
until each leaf has one substantial deliverable and a clear completion check.
Parent branches own integration checks across their children. Use depth to
separate deliverables, not as a multiplier for effort.

When a depth is requested, treat the root as the first layer and preserve that
structure where it remains useful. Read [method.md](references/method.md) for
the Depth Tree approach created by Leonxlnx.

## Coordinate work when useful

Identify shared interfaces, dependencies, and ownership before work begins.
Work independent leaves concurrently only when authorized and supported.
Otherwise process them sequentially in dependency order.

Give each participant the shared contract, their own deliverable, and its
acceptance criteria. Verify each returned result before allowing dependent
work to rely on it. If no separate participant is available, perform and check
the work directly without claiming independent verification.

Read [orchestration.md](references/orchestration.md) when coordinating multiple
deliverables or participants. No specific delegation interface is required.

## Complete each deliverable

Implement the whole deliverable, review it against the agreed requirements,
and check reachable defects, edge cases, and affected related behavior. Resolve
blocker and material findings before marking the deliverable complete.

Run the smallest meaningful checks that establish the required outcomes.
Inspect direct evidence when execution cannot establish them. A failed check
reopens the corresponding criterion. Recheck integration after related
deliverables change.

Stop refinement when the required outcomes are evidenced and remaining
observations are cosmetic. Do not let optional improvements expand the task.

## Handle limits explicitly

When an external limit prevents an outcome, keep that outcome visible with
the blocker, evidence, and decision needed to continue. A blocked or waived
criterion is not a passed criterion. Do not drop requirements or waive them
on the user's behalf to obtain a completed status.

Before changing approaches, identify what remains and why the new approach
better serves the same intent. Preserve useful work and unrelated changes.

## Audit the report

Check every required outcome against its evidence before reporting completion.
Re-measure every reported number or mark it unverified. For exhaustive tasks,
compare the expected inventory with the inspected inventory and disclose any
sampling or omissions.

Report verified outcomes, remaining blockers or explicit user waivers, and
the actual scope checked. Do not claim the task is complete while a required
outcome remains unmet.

Keep evidence and context concise using [token-economy.md](references/token-economy.md).
