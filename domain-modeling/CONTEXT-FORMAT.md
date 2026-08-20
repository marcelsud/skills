# CONTEXT.md format

## Structure

```md
# {Context name}

{One or two sentences describing this context and why it exists.}

## Language

**Order.**
{A one or two sentence definition}
_Avoid_: Purchase, transaction

**Invoice.**
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer.**
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## Rules

- **Pick one term.** When several words name the same concept, choose one and list the others under `_Avoid_`.
- **Keep definitions tight.** Use at most two sentences. Define what the term is.
- **Include only domain terms.** Exclude timeouts, error types, utility patterns, and other programming concepts. Before adding a term, ask whether it is specific to this domain.
- **Group related terms when useful.** Keep a flat list when every term belongs to one area.

## Single-context and multi-context repositories

**Single context.** Put one `CONTEXT.md` at the repository root.

**Multiple contexts.** Put a `CONTEXT-MAP.md` at the root. List each context, its location, and its relationships:

```md
# Context map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md). Receives and tracks customer orders.
- [Billing](./src/billing/CONTEXT.md). Generates invoices and processes payments.
- [Fulfillment](./src/fulfillment/CONTEXT.md). Manages warehouse picking and shipping.

## Relationships

- **Ordering to Fulfillment.** Ordering emits `OrderPlaced` events. Fulfillment consumes them to start picking.
- **Fulfillment to Billing.** Fulfillment emits `ShipmentDispatched` events. Billing consumes them to generate invoices.
- **Ordering and Billing.** Share `CustomerId` and `Money`.
```

Infer the structure from the repository:

- If `CONTEXT-MAP.md` exists, read it to find the contexts.
- If only a root `CONTEXT.md` exists, use a single context.
- If neither exists, create a root `CONTEXT.md` when the first term is resolved.

For multiple contexts, infer where the current topic belongs. Ask only when the repository cannot answer.
