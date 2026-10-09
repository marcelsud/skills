---
name: fusion
description: Run two user-selected models independently on the same prompt. The current model combines their evidence, resolves disagreements, fills gaps, and returns one answer.
argument-hint: '<model-a> <model-b> -- <prompt>'
disable-model-invocation: true
---

# Fusion

Run two candidate analyses in parallel, then reconcile them. The current model judges the evidence and writes the final answer. It must not concatenate, vote, or summarize the candidates.

## Invocation

Preferred syntax:

```text
/skill:fusion <model-a> <model-b> -- <prompt>
```

Example:

```text
/skill:fusion openai-codex/gpt-5.6-sol grok-4.5 -- Design a migration plan for this API.
```

Model selectors are single, non-empty model patterns or role aliases accepted by the `worker` tool, such as `@slow` or `provider/model-id`. A `:reasoning` suffix is allowed. Treat square brackets in usage documentation as notation, not required literal characters.

Parse the skill command's `User:` arguments as follows:

1. Everything before the first `--` is the selector section. Everything after it is the prompt, preserved exactly except for surrounding whitespace and required credential redactions.
2. The selector section MUST contain exactly two model selectors.
3. For convenience, when `--` is absent, use the first two whitespace-delimited tokens as selectors and the remainder as the prompt.
4. Reject missing selectors or an empty prompt with this usage line and do not spawn agents:

```text
Usage: /skill:fusion <model-a> <model-b> -- <prompt>
```

Never silently replace a requested model or turn a selector into a fallback chain.

## Redact credentials before delegation

The raw prompt and conversation context may contain credentials. Before placing either into a subagent `context` or `task`, create one sanitized copy:

- Replace secret values with stable placeholders such as `<REDACTED_SECRET_1>`.
- Treat API keys, access tokens, passwords, authorization headers, cookies, private keys, credential-bearing URLs/DSNs, and values the user identifies as secret as sensitive.
- Preserve surrounding structure so the candidates can still reason about the problem.
- Apply the same replacements to both candidate briefs.
- Never send a raw secret to a subagent or restore a redacted value in candidate or final output.

If the task cannot be solved without delegating an actual secret value, stop the fusion and explain that a non-secret surrogate is required.

## Prepare the shared brief

Fresh workers do not inherit the conversation. Build one neutral shared brief containing:

- the user's prompt after applying the credential-redaction rules above;
- only the prior conversation and workspace facts needed to understand references such as "this," "that file," or "the previous plan";
- explicit user constraints and requested output format;
- no tentative conclusion from the current model.

Both workers MUST receive the same sanitized brief and the same assignment. Neither may receive the other's identity, work, or output.

This is an analysis workflow. Tell both agents to remain read-only. They may inspect files, sources, and tools needed to ground the answer. They must not edit files, commit, push, open PRs, start persistent services, or create side effects. Proposed code or patches are allowed when the prompt asks for them. Credentials must stay redacted.

## Run both models in parallel

Dispatch one `worker` call per selector in the same assistant message so both
analyses run concurrently.

Required `worker` fields:

| Field | Value |
| --- | --- |
| `prompt` | the shared brief below; identical for both calls |
| `model` | exact selector for that call; never an array, fallback chain, or substitute |
| `label` | `FusionA` / `FusionB` |

Preflight: the active tool registry must contain `worker`. If it is absent,
stop and give `omp plugin install github:marcelsud/omp-extensions`. Run
`omp plugin list --json` only when you must distinguish a missing entry from a
disabled one; never install or enable a plugin without permission.

When Python `eval` is available, one `parallel(...)` cell is equivalent and
also reports each resolved model:

```python
brief = "<SHARED_BRIEF>"
results = parallel([
    lambda model=model, label=label: tool.worker(
        {"prompt": brief, "model": model, "label": label}
    )
    for model, label in [("<MODEL_A>", "FusionA"), ("<MODEL_B>", "FusionB")]
])
display(results)
```

Shared brief, part 1 (identical for both calls):

```text
# Goal
Run two independent read-only analyses of the same user prompt for a fusion judge.

# Constraints
- Remain read-only. Do not edit files, commit, push, open PRs, start services, or create side effects.
- Do not mention the fusion workflow, the other model, or expected consensus.
- Ground factual claims. Separate evidence, assumptions, and uncertainties.
- Put the user-facing reply in `answer`, following any requested format exactly.
- Never reproduce credentials or secrets; retain the supplied redaction placeholders.

# Contract
Return only the structured candidate object.
```

The `worker` tool returns text, so this JSON contract travels inside the prompt. Include it verbatim in both calls:

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

Shared brief, part 2 (substitute the sanitized prompt and any sanitized minimal brief notes):

```text
# Target
Solve the user prompt independently.

# User prompt (credential-redacted when needed)
<SANITIZED_PROMPT>

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
8. Never reproduce or infer redacted credential values.
```

### Wait / failure rules

- Both calls must return before you write the final answer. Do not yield a partial fusion.
- Parse each candidate's `text` as the JSON contract above. If a candidate returns prose instead, use that text and treat the structured fields as unavailable.
- A transient execution failure MAY be retried once with the **same exact** selector.
- If a requested selector remains unavailable or either candidate cannot be obtained, report which selector failed and stop. Do not present the surviving candidate as a fusion.
- Report `details.model` per candidate only when the user asks which concrete models answered.

## Reconcile the candidates

Work through both results in this order:

1. **Normalize.** Extract each proposed answer, claim, piece of evidence, assumption, uncertainty, constraint, and recommendation.
2. **Compare.** Find agreements, additions, contradictions, and omissions. Keep the comparison internal unless the user asks for it.
3. **Judge.** Rank support in this order:
   - user constraints and directly observed evidence;
   - authoritative sources and exact code or tool observations;
   - sound reasoning from stated premises;
   - model agreement as a weak signal only.
4. **Verify.** Use available tools to resolve material factual conflicts. Never choose by majority vote, confidence, verbosity, or model reputation. Do not spawn a third judge.
5. **Draft.** Write a new answer that keeps supported contributions, removes duplication, fills gaps, and rejects unsupported claims. Do not stitch the transcripts together.
6. **State unresolved conflicts.** Put remaining uncertainty at the exact decision point and name the evidence needed to resolve it. Never invent consensus.
7. **Deliver.** Answer the original prompt in its requested format and level of detail. Do not restore a redacted credential. Do not narrate the workflow or write "Agent A says." Mention the candidates only when the user asks.

Before presenting the answer, check every recommendation against its evidence and every explicit user constraint against the draft. Resolve or state candidate contradictions. Confirm that no credential value appears.
