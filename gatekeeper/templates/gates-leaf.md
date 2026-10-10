# Gates: <leaf or task name>

Scope: <one-line deliverable>

- [ ] G1: <observable outcome>
  CHECK: <command that verifies it>
  EXPECT: <required substring or /regex/>
  EVIDENCE: pending

- [ ] G2: <another runnable outcome>
  CHECK: <command>
  EXPECT: <substring or /regex/>
  EVIDENCE: pending

- [ ] G3: <manual outcome when no command applies>
  EVIDENCE: pending

<!--
Rules are defined in references/gates.md.
- Use one box per outcome.
- gate-check checks a box only when CHECK output matches EXPECT.
- Pending evidence keeps a gate unmet.
- Record only the output that decides the gate.
- Keep impossible gates and add `ABANDON: G<n> <reason>`.
- List abandoned gates in the final report.
-->
