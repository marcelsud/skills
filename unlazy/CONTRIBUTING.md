# Contributing

Unlazy is deliberately small: one skill file, reference documents, templates,
and three zero-dependency scripts.

## Accepted changes

- **Research updates.** Add recent papers or benchmarks to the README with a
  link and one claim supported by the source.
- **Enforcement rules.** Cite the failure mode and state an action the agent
  can follow.
- **Portability fixes.** Include the affected agent and version.
- **Prose fixes.** Prefer direct, shorter instructions.

## Ground rules

1. **Keep enforcement structural.** Gates, commands, and evidence establish
   completion. Prose alone does not.
2. **Preserve the gate format.** Format changes must update
   `gate-check.mjs`, `stop-hook.mjs`, `references/gates.md`, and the
   templates in one PR.
3. **Source behavioral claims.** Cite research from about the last two years
   or provide a reproducible measurement.
4. **Use no em or en dashes.** Use sentence breaks, commas, or colons.
5. **Keep valid frontmatter.** `name` and `description` must follow the agent
   skills format.
6. **Keep scripts dependency-free.** Use the Node 16+ standard library and
   support Windows and POSIX.

## Submitting changes

Open an issue for a disputed change or a pull request for a clear fix. There
is no build step. For script changes, test passing and failing CHECK commands,
regex EXPECT, manual gates, ABANDON, `--verify` success and failure, empty
gate files, and malformed checkboxes. Also test the Stop hook's block,
six-stop release, progress reset, parse-error block, and no-gates paths.
Test installer setup, repeated setup, and uninstall.
