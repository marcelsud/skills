# Design it twice

Use this parallel agent pattern when the user wants alternative interfaces for a chosen deepening candidate. Ousterhout's "Design It Twice" assumes the first idea is unlikely to be the best.

Use **module**, **interface**, **seam**, and **adapter** as defined in [SKILL.md](SKILL.md).

## Process

### 1. Frame the problem space

Before spawning agents, explain the candidate's problem and constraints:

- Constraints every design must satisfy
- Dependencies and their categories from [DEEPENING.md](DEEPENING.md)
- A rough code sketch that makes the constraints concrete without proposing a design

Show this to the user, then start Step 2 immediately. The user can read while the agents work.

### 2. Spawn agents

When delegation is available, spawn at least three independent agents in parallel. Otherwise, produce alternatives in separate sequential passes. Every pass must produce a **radically different** interface.

Give each agent the same technical brief. Include file paths, coupling details, the dependency category from [DEEPENING.md](DEEPENING.md), and what belongs behind the seam. Then assign a different constraint to each agent:

- **Agent 1.** "Keep the interface to one to three entry points. Maximize capability per entry point."
- **Agent 2.** "Support many use cases and extensions."
- **Agent 3.** "Optimize for the most common caller. Make the default case trivial."
- **Agent 4, when relevant.** "Use ports and adapters for dependencies across seams."

Include [SKILL.md](SKILL.md) vocabulary and, when available, `CONTEXT.md` vocabulary in the brief so each pass names things consistently with the architecture language and the project's domain language.

Each agent outputs:

1. Interface types, methods, parameters, invariants, ordering rules, and errors
2. Usage example
3. Behavior hidden behind the seam
4. Dependency strategy and adapters from [DEEPENING.md](DEEPENING.md)
5. Tradeoffs, including how much each caller must learn

### 3. Present and compare

Present each design separately, then compare them in prose. Contrast depth, locality, and seam placement.

Recommend the strongest design and explain why. Combine parts only when the result is better than either original. The user wants a strong read, not a menu.
