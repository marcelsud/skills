---
name: codebase-design
description: Define and apply a shared vocabulary for deep modules. Use when designing an interface, placing a seam, reducing caller-facing complexity, or keeping tests out of internals. Other architecture skills use these definitions.
---

# Codebase design

Put substantial behavior behind a small interface at a seam that callers already cross. Test through that interface. Use these terms throughout design and restructuring. Callers learn less, maintainers get locality, and tests avoid internals.

## Glossary

Use these terms exactly. Don't substitute "component," "service," "API," or "boundary." Consistent language matters.

**Module.** Anything with one interface and an implementation. It can be a function, class, package, or tier-spanning slice. _Avoid_: unit, component, service.

**Interface.** Everything a caller must know to use the module correctly. This includes the type signature, invariants, ordering constraints, error modes, required configuration, and performance characteristics. _Avoid_: API and signature, which refer only to types.

**Implementation.** The code inside a module. A Postgres repository can be a small adapter with a large implementation. An in-memory fake can be a large adapter with a small implementation. Use "adapter" when discussing the seam and "implementation" when discussing the code behind it.

**Depth.** The amount of behavior a caller or test can exercise compared with the interface it must learn. A deep module hides substantial behavior behind a small interface. A shallow module exposes nearly as much complexity as it implements.

**Seam.** Michael Feathers' term for a place where behavior can change without editing the code at that place. The interface lives at the seam. Choosing the seam is separate from choosing the implementation. _Avoid_: boundary, which is overloaded by DDD's bounded context.

**Adapter.** A concrete implementation of an interface at a seam. The term describes the role it fills, not the code inside it.

**Locality.** Change and verification stay in one module instead of spreading across callers. Fix a bug once.

## Deep vs shallow

**Deep module** = small interface + lots of implementation:

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
└─────────────────────┘
```

**Shallow module** = large interface + little implementation (avoid):

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

When designing an interface, ask:

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

## Principles

- **Depth belongs to the interface, not the implementation.** A deep module may contain small, mockable, swappable parts. Those parts stay private. A module may have internal seams for its own implementation and tests, plus the external seam at its interface.
- **The deletion test.** Imagine deleting the module. A pass-through's complexity disappears. A useful module's complexity reappears across its callers.
- **Tests use the interface.** Callers and tests cross the same seam. If a test must bypass the interface, the module probably has the wrong shape.
- **One adapter makes a hypothetical seam. Two adapters make a real one.** Add a seam only when something varies across it.

## Designing for testability

Design interfaces that tests can call directly:

1. **Accept dependencies, don't create them.**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **Return results, don't produce side effects.**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **Keep the interface small.** Fewer methods need fewer tests. Fewer parameters need less setup.

## Rejected framings

- **Implementation-lines divided by interface-lines.** This rewards padding the implementation. Depth instead compares hidden behavior with what callers must learn.
- **The TypeScript `interface` keyword or a class's public methods.** Too narrow. An interface includes every fact a caller must know.
- **Boundary.** Overloaded by DDD's bounded context. Say **seam** or **interface**.

## Going deeper

- **Deepen a cluster based on its dependencies.** See [DEEPENING.md](DEEPENING.md) for dependency categories, seam discipline, and replacement testing.
- **Explore alternative interfaces.** See [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) for parallel design passes and comparison by depth, locality, and seam placement.
