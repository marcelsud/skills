# Gate file format

`gate-check.mjs` and `stop-hook.mjs` parse the format below. Keep the field
names and indentation exact.

## Format

```markdown
# Gates: <scope name>

Scope: <one line>

- [ ] G1: <outcome>
  CHECK: <shell command>
  EXPECT: <substring or /regex/>
  EVIDENCE: pending

- [ ] G2: <manual outcome>
  EVIDENCE: pending

ABANDON: G2 <reason, only if a gate had to be surrendered>
```

## Parsing rules

- A gate starts at a line matching `- [ ]` or `- [x]` (case-insensitive x).
- Indented `CHECK:`, `EXPECT:`, `EVIDENCE:` lines up to the next gate belong
  to the gate above them.
- `EXPECT:` matches a plain substring in combined stdout and stderr. Text
  wrapped in slashes is a JavaScript regular expression, for example
  `/8\/8 passed/`.
- `ABANDON: G<n> <reason>` marks that gate resolved without passing it. The
  final report must list the gate and reason.
- A present gate file must contain at least one valid gate. An empty gate
  file or malformed checkbox is a parse error. The checker exits 2, and the
  Stop hook blocks.

## Checker modes

- No mode flag runs unchecked gates and checked gates with pending evidence.
- `--status` reports state without running CHECK commands.
- `--verify` reruns every CHECK. A failed rerun unchecks the gate and records
  the failed verification as evidence.

## When a gate is unmet

A gate is unmet when:

1. Its box is unchecked and no ABANDON line names it.
2. Its box is checked but `EVIDENCE:` still reads `pending`.

## Writing good gates

- **State outcomes.** "All 8 planets are clickable" is checkable. "Work on
  planet interaction" is not.
- **Use commands when possible.** A CHECK command gives the same result when
  the parent reruns it. If no command can observe the outcome, make the gate
  more specific or record manual evidence.
- **Match decisive output.** Use a line that appears only on success, such as
  `8/8 passed`, rather than a generic line such as `done`.
- **Keep evidence short.** Record the deciding output or cite `file:line`.
- **Use five to twelve gates per leaf.** Fewer may omit requirements. More
  usually means the leaf contains multiple deliverables.

## Numbers rule

Give every reported number a CHECK command that measures it. The v1 tests
found incorrect final counts stated from memory.
