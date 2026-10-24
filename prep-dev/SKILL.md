---
name: prep-dev
description: Prepare substantive implementation work through repository research and a short interview about behavior, contracts, scope, and validation. Use before coding when consequential decisions remain unclear, or when explicitly asked to interview or plan implementation.
---

# Prepare Development

Establish enough shared understanding to implement a focused change with clear acceptance criteria. Keep this proportional to the task. A small, well-specified fix may need no interview.

## Examine the premise

Start with constructive skepticism. Establish whether the stated problem exists, whether the proposed cause explains it, and whether the suggested change addresses that cause.

- Separate observed facts, assumptions, and proposed solutions.
- Look for counterexamples, existing capabilities, and a simpler way to achieve the intended outcome.
- Check whether the request addresses a symptom or introduces complexity disproportionate to the problem.
- Investigate questions the repository or available evidence can answer before asking the user.
- If a consequential premise remains uncertain, make it an early interview question. Explain what decision depends on the answer.

Raise concerns respectfully and specifically: state the observation, explain its consequence, and suggest an alternative or a way to verify it. Match confidence to evidence.

Challenge the approach while preserving the user's underlying goal. When the evidence supports the premise, move forward. Avoid manufacturing objections or reopening settled decisions without new evidence.

## Gather context first

Read the request, applicable repository instructions, and relevant implementation and tests. Use CodeGraph first when the repository is indexed and the tool is available; otherwise use the available repository search tools.

Identify existing capabilities, conventions, callers, and constraints before proposing new structures. Do not ask the user questions the available evidence already answers.

Honor analysis-only and draft-only boundaries.

## Run a short interview

Ask only questions whose answers could materially change implementation.

Prefer one round of up to three concise questions. Offer concrete options and a recommendation when useful. Ask a follow-up only when a consequential ambiguity remains.

Select from these topics according to the change:

- **Outcome:** What should happen, for whom, and what observable result establishes success?
- **Scope:** Which cases belong in this change? What existing behavior must remain?
- **Contracts:** Who owns the data and logic? Which identifiers, fields, units, timestamps, and failure semantics cross boundaries?
- **State and retries:** What transitions are allowed? What should repeated, concurrent, or out-of-order requests do?
- **Failure behavior:** Which failures should propagate, retry, or degrade gracefully? What must remain visible to operators?
- **Delivery:** Which consumers, migrations, infrastructure changes, or rollout steps must be coordinated?
- **Validation:** Which regression or end-to-end scenario would demonstrate the intended behavior?

Explain the consequence of each question. Avoid generic questionnaires and asking the user to choose routine implementation details.

Use the available question tool when appropriate; otherwise ask in conversation. Continue independent research while waiting, but do not implement behavior that depends on an unanswered required question. Silence is not an answer.

## Resolve routine design choices

Use repository conventions and evidence to choose ordinary implementation details.

Prefer existing business logic, shared helpers, and established library patterns. Keep transport and adapter details at their boundaries.

Consider early whether the design needs:

- Required versus optional fields and explicit domain types.
- Separate concepts that may have different lifecycles.
- Payload consistency checks for repeated operation keys.
- Transaction boundaries and reliable side effects.
- Batching, bounded work, index support, and failure detection.

Do not add speculative abstractions or unsupported future variants. Record meaningful assumptions rather than expanding scope.

## Produce a development brief

Summarize only what the work needs:

- Intended behavior and acceptance criteria.
- Scope and compatibility constraints.
- Proposed approach and affected components.
- Important contract, state, and failure decisions.
- Validation approach and delivery dependencies.
- Remaining assumptions or blockers.

Separate decisions from recommendations and unresolved questions. Return the brief in conversation unless the user or repository instructions specify a file.

When implementation is already authorized, proceed after required questions are resolved. Do not add a separate approval gate. When the request is preparation-only, deliver the brief and stop before editing code.
