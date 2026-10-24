---
name: prep-pr
description: Check an implemented change for pull request readiness, including scope, contracts, maintainability, validation, and review handoff. Use when preparing a PR, performing an author self-review, or assessing readiness for review.
---

# Prepare a PR

Verify that the implementation delivers the intended behavior and gives reviewers enough evidence to assess it.

Use the development brief or agreed acceptance criteria when available. Otherwise derive the intended behavior from the request and repository context.

Apply relevant checks proportionally. Respect read-only and draft-only requests. Publishing requires authorization. This skill does not replace any independent review required by the repository.

## Reassess the premise and solution

Review the change with fresh eyes, including changes you implemented yourself. Treat completed code and passing tests as evidence to evaluate, rather than proof that the approach is appropriate.

- Confirm that the change addresses the original problem and satisfies the intended outcome.
- Revisit assumptions that materially influenced the implementation.
- Look for counterexamples, regressions, unnecessary complexity, and simpler solutions.
- Check whether tests demonstrate the desired behavior or merely confirm the chosen implementation.
- Distinguish defects and unmet requirements from preferences and optional improvements.

Raise concerns with concrete evidence and explain their practical impact. Recommend a proportionate correction; reserve redesign proposals for problems that justify them.

Be candid and collaborative. Acknowledge uncertainty, explain tradeoffs, and avoid presenting personal preferences as requirements. Do not reopen settled decisions without a material correctness issue or new evidence.

## Check the actual change

Read applicable repository instructions and inspect the diff against the intended base. Use CodeGraph first when the repository is indexed and the tool is available; otherwise use the available repository search tools.

- Confirm that the implementation satisfies the agreed scope.
- For refactors, verify preservation of defaults, serialization, errors, and side effects.
- Identify intentional behavior changes and explain them.
- Remove unrelated edits, unused wiring, and speculative structures within the authorized scope. Preserve unrelated user work.
- Keep independently useful changes separable when that improves review.

## Verify contracts and correctness

Trace changed data through callers, persistence, and emitted events.

- Verify identifiers, currencies, units, timezones, and timestamps retain their meaning.
- Keep transport mapping and adapter-specific behavior at their boundaries.
- Enforce required data without substituting plausible defaults for invalid input.
- Preserve genuine optionality and use existing domain types and conversion helpers.
- Check state transitions, terminal states, and update precedence.
- Verify repeated operation keys cannot silently accept inconsistent payloads.
- Check retries and redelivery for duplicate writes, notifications, charges, and external calls.
- Confirm failure handling matches the intended business behavior and exposes unexpected errors.

## Check maintainability and operations

- Reuse production logic and shared constants; avoid copies that can drift.
- Follow established DAO, dependency injection, and configuration patterns.
- Justify new wrappers, exception types, and layers by their actual purpose.
- Remove stale comments and use names that remain meaningful after rollout.
- For changed queries or workers, assess index coverage, expected volume, batching, limits, leases, and recovery as applicable.
- Check dependent consumers before removing metrics, configuration, or contract fields.
- Verify infrastructure, dependency versions, migrations, and deployment ordering are accounted for.

## Verify meaningful behavior

Run checks appropriate to the change. Reuse existing passing evidence unless new changes or unresolved concerns justify another run.

- Cover material behavior changes and discovered bugs with meaningful regression tests.
- Include relevant missing-data, retry, concurrency, and configuration cases.
- Assert observable outcomes and exact arguments where they determine correctness.
- Compare structured data semantically when formatting is irrelevant.
- Avoid duplicate scenarios and tests that merely mirror implementation details.
- Name tests for the behavior they demonstrate.

Assess automated feedback against the actual code and intended behavior. Separate actionable defects from optional suggestions and future work.

## Prepare the handoff

Describe the concrete problem and resulting behavior, with a before-and-after example when useful.

Include consequential decisions, compatibility changes, delivery dependencies, completed validation, and material limitations.

Distinguish local checks, CI results, and deployed verification. Do not imply that one proves another.

Report remaining issues in priority order with evidence and proposed actions. State readiness only to the extent supported by completed checks, and identify any additional ownership review needed.
