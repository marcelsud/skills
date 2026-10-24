# Gates: <branch name> (integration)

Scope: integrate <child leaves or branches>

- [ ] N1: parent verification passes every child gates file
  CHECK: node <skill-dir>/scripts/gate-check.mjs --verify gates/leaf-<a>.md gates/leaf-<b>.md
  EXPECT: ALL MET
  EVIDENCE: pending

- [ ] N2: interfaces match the contract in PLAN.md
  CHECK: <build / typecheck / import test command>
  EXPECT: <success marker>
  EVIDENCE: pending

- [ ] N3: integrated behavior passes end to end
  CHECK: <integration test, smoke command, or request sequence>
  EXPECT: <success marker>
  EVIDENCE: pending

- [ ] N4: targeted checks pass for affected siblings
  CHECK: <targeted re-run of affected sibling checks>
  EXPECT: <success marker>
  EVIDENCE: pending

<!--
Re-run child checks before marking N1. Do not rely on child reports.
See references/orchestration.md.
-->
