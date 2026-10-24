---
name: fusion
description: Run two user-selected models independently on the same prompt, then combine their evidence, resolve disagreements, and return one answer. Use when the user requests a fusion of two models.
---

# Fusion

Obtain two independent analyses of the same request, then judge their evidence
and write one answer. Agreement alone is weak evidence.

## Establish the request

Identify the user's prompt, the two requested models, relevant conversation
context, constraints, and expected output. Ask for a missing model or prompt.
Preserve the requested model choices; never silently substitute another model.

Use an authorized way to obtain a separate analysis from each model. If a
requested model is unavailable, explain what is missing. The user may supply
its analysis or authorize another route. Do not simulate independent models
with two passes of your own reasoning or present one analysis as a fusion.

## Prepare one shared brief

Create one neutral brief containing the request, the minimum context needed
to resolve its references, the user's constraints, and the expected output.
Exclude your tentative conclusion and give both models the same brief.

Before sharing anything, replace credentials and other secrets with stable
redactions. Preserve surrounding structure, use the same redactions in both
briefs, and never restore or infer the secret values in any output. If the
task requires sharing an actual secret, explain that a non-secret surrogate
is needed.

Ask each model to solve the request independently and return a self-contained
answer with its key claims, evidence, assumptions, and uncertainties. Neither
receives the other's answer or your emerging conclusion.

Keep both analyses read-only. They may inspect permitted sources and propose
changes, but this workflow does not authorize editing files, publishing,
starting services, or contacting others.

## Obtain both analyses

Run the analyses concurrently when supported. Sequential execution is also
valid if the briefs and contexts remain independent. Wait for both results
before synthesizing. A transient failure may be retried once with the same
requested model. If either analysis remains unavailable, report the limitation
and stop without claiming a completed fusion.

## Reconcile the evidence

Extract each answer's claims, evidence, assumptions, uncertainties, and
recommendations. Identify agreements, additions, omissions, and contradictions.

Resolve disagreements using the user's constraints and observed evidence,
then authoritative sources, then sound reasoning. Model confidence and model
agreement do not establish truth. Verify material factual conflicts using
available sources; do not add a third model as a judge.

Write a new answer that retains supported contributions, removes duplication,
and fills meaningful gaps. Do not concatenate or vote on the two answers.
State unresolved uncertainty where it affects a decision and identify the
evidence needed to resolve it.

## Deliver

Answer the original request in its requested format and level of detail.
Check every recommendation against its evidence and every explicit constraint
against the final answer. Confirm that no credential value appears.

Keep the comparison internal unless the user asks for it. Identify the actual
models only when known; never claim a requested model ran without evidence.
