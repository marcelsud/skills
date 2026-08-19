# Deepening

How to deepen a cluster of shallow modules based on its dependencies. Uses **module**, **interface**, **seam**, and **adapter** as defined in [SKILL.md](SKILL.md).

## Dependency categories

When assessing a candidate for deepening, classify its dependencies. The category determines how the deepened module is tested across its seam.

### 1. In-process

Pure computation or in-memory state with no I/O. Merge the modules and test the new interface directly. No adapter is needed.

### 2. Local-substitutable

Dependencies with local test replacements, such as PGLite for Postgres or an in-memory filesystem. Deepen only when a replacement exists. Run it in the test suite. Keep this seam internal instead of exposing a port in the module's interface.

### 3. Remote but owned (Ports & Adapters)

Services you own but call over a network. Define a **port** at the seam. The deep module owns the logic and accepts the transport as an **adapter**. Tests use an in-memory adapter. Production uses an HTTP, gRPC, or queue adapter.

Recommended wording: *"Define a port at the seam. Use an HTTP adapter in production and an in-memory adapter in tests. The logic stays in one deep module even though it runs across a network."*

### 4. True external (Mock)

Third-party services such as Stripe or Twilio. The deepened module accepts the external dependency through a port. Tests provide a mock adapter.

## Seam discipline

- **One adapter makes a hypothetical seam. Two adapters make a real one.** Add a port only when at least two adapters are justified, usually production and test. A single-adapter seam is only indirection.
- **Keep internal seams private.** A deep module may have internal seams for its implementation and tests, plus the external seam at its interface. Do not expose an internal seam just because tests use it.

## Replace shallow tests

- Delete old unit tests for shallow modules once tests at the deepened interface cover their behavior.
- Test observable outcomes through the deepened interface, not internal state.
- Tests should survive internal refactors. A test that changes with the implementation is bypassing the interface.
