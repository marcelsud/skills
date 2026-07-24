---
name: fusion
description: Run two user-selected models independently on the same prompt, then have the current model reconcile their evidence, disagreements, and complementary insights into one answer.
argument-hint: '<model-a> <model-b> -- <prompt>'
disable-model-invocation: true
---

# Fusion

Run two independent candidate analyses in parallel, then synthesize them. The current model is the judge and final author; it MUST reason over both results rather than concatenate, vote, or summarize them.

## Invocation

Preferred syntax:

```text
/skill:fusion <model-a> <model-b> -- <prompt>
```

Example:

```text
/skill:fusion openai-codex/gpt-5.6-sol grok-4.5 -- Design a migration plan for this API.
```

Model selectors are single, non-empty tokens accepted by the task tool. A `:reasoning` suffix is allowed. Treat square brackets in usage documentation as notation, not required literal characters.

Parse the skill command's `User:` arguments as follows:

1. Everything before the first `--` is the selector section; everything after it is the prompt, preserved verbatim except for surrounding whitespace.
2. The selector section MUST contain exactly two model selectors.
3. For convenience, when `--` is absent, use the first two whitespace-delimited tokens as selectors and the remainder as the prompt.
4. Reject missing selectors or an empty prompt with this usage line and do not spawn agents:

```text
Usage: /skill:fusion <model-a> <model-b> -- <prompt>
```

Never silently replace a requested model or turn a selector into a fallback chain.

## Prepare the shared brief

Subagents do not inherit the conversation. Build one neutral shared brief containing:

- the user's prompt verbatim;
- only the minimum prior conversation and workspace facts required to understand references such as “this”, “that file”, or “the previous plan”;
- explicit user constraints and requested output format;
- no tentative conclusion from the current model.

Both subagents MUST receive the same brief and the same task instructions. They MUST NOT receive each other's identity, work, or output.

This is an analysis workflow. Tell both agents to remain read-only: they may inspect files, sources, and tools needed to ground the answer, but MUST NOT edit files, commit, push, open PRs, start persistent services, or create side effects. They may include proposed code or patches in their answer when the prompt asks for them.

## Run both models in parallel

Use **one** batched `task` call with exactly two items so the analyses run concurrently.

Required item fields:

| Field | Value |
| --- | --- |
| `name` | `FusionA` / `FusionB` |
| `agent` | omit (general-purpose task agent) |
| `model` | exact selector string for that item; never an array / fallback chain |
| `schemaMode` | `permissive` |
| `outputSchema` | identical schema below |
| `task` | identical assignment text for both items |

Shared `context` for the batch:

```text
# Goal
Run two independent read-only analyses of the same user prompt for a fusion judge.

# Constraints
- Remain read-only. Do not edit files, commit, push, open PRs, start services, or create side effects.
- Do not mention the fusion workflow, the other model, or expected consensus.
- Ground factual claims. Separate evidence, assumptions, and uncertainties.
- Put the user-facing reply in `answer`, following any requested format exactly.

# Contract
Return only the structured candidate object.
```

Identical `outputSchema` for both items:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["answer", "keyClaims", "evidence", "assumptions", "uncertainties"],
  "properties": {
    "answer": { "type": "string" },
    "keyClaims": { "type": "array", "items": { "type": "string" } },
    "evidence": { "type": "array", "items": { "type": "string" } },
    "assumptions": { "type": "array", "items": { "type": "string" } },
    "uncertainties": { "type": "array", "items": { "type": "string" } }
  }
}
```

Identical `task` text for both items (substitute the real prompt and any minimal brief notes):

```text
# Target
Solve the user prompt independently.

# User prompt (verbatim)
<PROMPT>

# Brief notes (only if needed for pronouns/file refs)
<OPTIONAL_MINIMAL_CONTEXT_OR_NONE>

# Change
None. Read-only analysis only.

# Acceptance
1. Solve the prompt directly.
2. Put the user-facing reply in `answer`, following any requested format exactly.
3. Ground claims with evidence when applicable.
4. Separate evidence, assumptions, and uncertainties.
5. Cover relevant constraints, edge cases, risks, and tradeoffs.
6. Do not mention fusion, the other model, or expected consensus.
7. Return a self-contained candidate; do not edit or mutate anything.
```

### Wait / failure rules

- If background jobs are enabled, wait for **both** results before writing the final answer.
- Do **not** yield a partial fusion.
- Use `hub wait` only when there is no other useful grounding work to perform.
- A transient execution failure MAY be retried once with the **same exact** selector.
- If a requested selector remains unavailable or either candidate cannot be obtained, report which selector failed and stop. Do not present the surviving candidate as a fusion.

## Fuse intelligently

After both candidates arrive, analyze them in this order:

1. **Normalize** — extract each candidate's proposed answer, claims, evidence, assumptions, uncertainties, constraints, and recommendations.
2. **Compare** — identify agreements, complementary contributions, direct contradictions, and omissions. Do this internally; do not dump a comparison table unless the user asks.
3. **Adjudicate** — rank support using this order:
   - user constraints and directly observed evidence;
   - authoritative sources and exact code/tool observations;
   - sound reasoning from stated premises;
   - model agreement only as a weak signal.
4. **Verify** — when a material factual conflict can be resolved with available tools, check it. Never choose by majority vote, confidence, verbosity, or model reputation. Do not spawn a third judge.
5. **Synthesize** — write a **new** answer that combines compatible strengths, removes duplication, repairs gaps, and rejects unsupported claims. The result must be more useful than either candidate alone, not a stitched transcript.
6. **Expose uncertainty** — if a material conflict remains unresolved, state the uncertainty at the exact decision point and explain what evidence would resolve it. Never invent consensus.
7. **Deliver** — answer the original prompt directly in its requested format and level of detail. Do not lead with process narration or “Agent A says…”. Mention candidate provenance only when the user asks for it.

Before presenting the result, check that every material recommendation is supported, every explicit user constraint is satisfied, and no contradiction between the candidates was silently ignored.
