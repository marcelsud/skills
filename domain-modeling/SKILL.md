---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model.
---

# Domain modeling

Build the domain model while you design. Challenge ambiguous terms, test them with edge cases, and record accepted language and decisions as soon as they settle. Reading `CONTEXT.md` for vocabulary does not invoke this skill. Use it when the model itself changes.

## File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files only when you have something to write. Create the first `CONTEXT.md` when a term is resolved. Create `docs/adr/` when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with `CONTEXT.md`, say so immediately. "Your glossary defines 'cancellation' as X. You seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses a vague or overloaded term, propose one precise term. "When you say 'account,' do you mean Customer or User? Those are different."

### Discuss concrete scenarios

When discussing domain relationships, test them with specific scenarios. Choose edge cases that force precise distinctions between concepts.

### Cross-reference with code

When the user states how something works, check the code. If it disagrees, say so. "The code cancels entire Orders. You said partial cancellation is possible. Which is right?"

### Update CONTEXT.md inline

Update `CONTEXT.md` as soon as a term is resolved. Do not batch the edits. Follow [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` must contain no implementation details. It is not a specification, scratch pad, or place for implementation decisions. It is only a glossary.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse.** Changing the decision later would cost enough to matter.
2. **Surprising without context.** A future reader would ask why the code works this way.
3. **A real tradeoff.** You chose among genuine alternatives for specific reasons.

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
