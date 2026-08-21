# Changelog

## Unreleased

- The orchestrated driver dispatches every ready leaf, verifies returns
  separately, and dispatches newly unblocked work without waiting for a wave.
- PLAN.md now records dependencies and file ownership for scheduling.
- User-facing prose now uses shorter, direct instructions.
- `gate-check.mjs --verify` reruns every CHECK during parent verification.
- Gate files with no valid gates or malformed checkboxes fail closed.
- Explicit gate-file arguments work with and without `--timeout`.

## 2.0.0 (2026-08-10)

v2 added gate files, command checks, and an optional Claude Code Stop hook.
The design follows a controlled six-run test described in the README.

### Changed

- The Depth Tree now controls decomposition rather than predicted effort.
  Tree 6 cost about 1.0 to 1.5 times tree 3 in the test.
- Acceptance criteria live in `GATES.md` or `gates/*.md`.
- Final reports re-measure every stated number.

### Added

- `scripts/gate-check.mjs` runs CHECK commands, matches EXPECT, and records
  short evidence.
- `scripts/stop-hook.mjs` blocks Claude Code while gates remain unmet. It
  releases after six unchanged blocked stops or an ABANDON line.
- `scripts/install-hooks.mjs` installs or removes the hook from Claude Code
  settings.
- Orchestrated mode gives each leaf a fresh subagent and gates file. The
  parent reruns leaf checks.
- Reference files document gates, orchestration, the Depth Tree, and token
  controls.

v2 retains the four review passes, contracts before fan-out, explicit
handover for blocked gates, and measured full-sweep counts.

## 1.0.0 (2026-08-10)

Initial release.

- `SKILL.md` introduced the Depth Tree method.
- Nine rules cited recent research on incomplete execution and long-task
  degradation.
- The README documented installation, the method, and its sources.
