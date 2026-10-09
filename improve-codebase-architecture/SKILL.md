---
name: improve-codebase-architecture
description: Find shallow modules and poor seam placement, present candidates in a visual HTML report, and interview the user about the selected candidate. Use when the user wants smaller interfaces, better locality, or tests that avoid internals.
---

# Improve codebase architecture

Find architectural friction. Propose refactors that hide more behavior behind smaller interfaces and make those interfaces easier to test.

Use the project's domain model and the shared design vocabulary:

- Use `$codebase-design` for **module**, **interface**, **depth**, **seam**, **adapter**, and **locality**. Apply its deletion test, its "tests use the interface" rule, and its two-adapter rule; its `DEEPENING.md` defines the dependency categories. Use these terms instead of "component," "service," "API," or "boundary."
- When present, use `CONTEXT.md` to name domain concepts and read ADRs in `docs/adr/` before reopening a recorded decision.

## Process

### 1. Explore

**Start with scope.** Deepening pays off only in code likely to change again, so prioritize recently changed areas.

- If the user names a module, subsystem, or pain point, use that scope and skip the history analysis.
- Otherwise, review recent commits until repeated paths emerge. Start there. Widen the search only when the history has no clear concentration.

Read the project's domain glossary and relevant ADRs first when they exist.

Trace calls with the available repository search, history, and test tools. Record specific friction:

- Understanding one concept requires reading many small modules.
- A module is shallow because its interface nearly matches its implementation.
- Pure functions exist only for testing while bugs remain in their callers.
- Tightly coupled modules expose details across their seams.
- Tests bypass the interface or do not exist.

Apply the **deletion test**. If deleting the module spreads its complexity across callers, it has depth. If the complexity disappears or moves intact, the module is shallow.

### 2. Present candidates as an HTML report

Write a self-contained HTML file in the OS temp directory so the report does not enter the repository. Use `$TMPDIR`, then `/tmp` on Unix or `%TEMP%` on Windows. Name the file `<tmpdir>/architecture-review-<timestamp>.html`. Open it with `xdg-open` on Linux, `open` on macOS, or `start` on Windows. Give the user its absolute path.

Use Tailwind for layout. Use Mermaid for call graphs, dependencies, and sequences. Use CSS or inline SVG for mass diagrams and cross-sections. Every candidate needs a before-and-after diagram.

For each candidate, render a card with:

- **Files.** Name the files and modules involved.
- **Problem.** State the concrete friction in one sentence.
- **Solution.** State what changes in plain English.
- **Wins.** At most six words per bullet, such as "Tests hit one interface."
- **Before and after.** Draw the current and proposed structures side by side.
- **Recommendation strength.** Use `Strong`, `Worth exploring`, or `Speculative`.
- **Dependency category.** Use `in-process`, `local-substitutable`, `ports & adapters`, or `mock`.

Finish with a **Top recommendation** section. Name the candidate you would tackle first and explain why.

Use `CONTEXT.md` terms for the domain and `$codebase-design` terms for architecture. If `CONTEXT.md` defines "Order," say "the Order intake module," not "FooBarHandler" or "Order service."

**ADR conflicts.** Include a conflicting candidate only when the friction justifies reopening the ADR. Mark the conflict in the card. For example, write *"Contradicts ADR-0007. Reopen it because..."* Do not list theoretical refactors that an ADR already rejects.

See [HTML-REPORT.md](HTML-REPORT.md) for the HTML template, diagram patterns, and style rules.

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Interview the user

After the user picks a candidate, ask one decision at a time about constraints, dependencies, the new module, what belongs behind the seam, and which tests survive. Resolve repository facts yourself. Recommend an answer with every question, then wait. Do not implement until both sides agree on the design.

When a decision changes the domain model, use `$domain-modeling`:

- Add a term to `CONTEXT.md` when the new module uses a domain concept that is not recorded. Create the file only when needed.
- Update a fuzzy term in `CONTEXT.md` as soon as it is resolved.
- If the user rejects a candidate for a reason that should constrain future reviews, offer to record an ADR. Skip temporary reasons such as "not worth it right now" and reasons obvious from the code.
- Use `$codebase-design` and its design-it-twice pattern to explore alternative interfaces.
