# ADR format

ADRs live in `docs/adr/` and use sequential numbering such as `0001-slug.md` and `0002-slug.md`.

Create `docs/adr/` only when the first ADR is needed.

## Template

```md
# {Short title of the decision}

{One to three sentences covering the context, decision, and reason.}
```

An ADR can be one paragraph. Record the decision and its reason. Do not add sections just to fill them in.

## Optional sections

Include these only when they help a future reader. Most ADRs do not need them.

- **Status frontmatter.** Use `proposed`, `accepted`, `deprecated`, or `superseded by ADR-NNNN` when decisions may be revisited.
- **Considered options.** Include rejected alternatives worth remembering.
- **Consequences.** Include downstream effects that are not obvious.

## Numbering

Scan `docs/adr/` for the highest existing number and increment by one.

## When to offer an ADR

All three of these must be true:

1. **Hard to reverse.** Changing the decision later would cost enough to matter.
2. **Surprising without context.** A future reader would ask why the code works this way.
3. **A real tradeoff.** You chose among genuine alternatives for specific reasons.

Skip an easy-to-reverse or obvious decision. If there was no real alternative, there is nothing to record.

### What qualifies

- **Architectural shape.** Examples include a monorepo or an event-sourced write model with a Postgres read model.
- **Integration between contexts.** For example, Ordering and Billing communicate through domain events instead of synchronous HTTP.
- **Technology choices with lock-in.** Record a database, message bus, auth provider, or deployment target when replacing it would take months. Skip ordinary libraries.
- **Ownership and scope.** Record which context owns data and how other contexts refer to it. Explicit exclusions matter.
- **Deliberate departures from the obvious path.** Record manual SQL instead of an ORM when the reason should stop a future engineer from "fixing" it.
- **Constraints hidden from the code.** Examples include compliance restrictions and partner latency limits.
- **Rejected alternatives that will recur.** If GraphQL lost to REST for a subtle reason, record it before someone proposes GraphQL again.
