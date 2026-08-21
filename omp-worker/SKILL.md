---
name: omp-worker
description: Run fresh OMP coding workers with an explicit model selector. Use for /skill:omp-worker, "use model X for this", model-specific delegation, parallel workers, staged model pipelines, or independent model review. Requires the worker tool from github:marcelsud/omp-extensions.
argument-hint: '<model> -- <prompt> | parallel <model...> -- <prompt> | pipeline <model...> -- <prompt>'
---

# OMP Worker

Delegate an assignment to fresh OMP sessions whose models are selected per call. Use the `worker` tool directly for one worker and Python `parallel(...)` or `pipeline(...)` for orchestration.

## Preflight: verify the extension first

Before parsing arguments or starting any worker, check whether the current OMP tool registry contains `worker`.

- **Tool present:** the extension is loaded; continue.
- **Tool absent:** if `bash` is available, run `omp plugin list --json` and inspect the `npm` entry named `@marcelsud/omp-extensions`.
  - Missing entry: stop and give `omp plugin install github:marcelsud/omp-extensions`.
  - Entry has `enabled: false`: stop and give `omp plugin enable @marcelsud/omp-extensions`.
  - Entry has `enabled: true`: stop and tell the user to restart OMP so the registered tool enters the session.
  - Command failure or unreadable output: stop, report that installation could not be verified, and give `omp plugin list`.
- **Tool and `bash` both absent:** stop and ask the user to verify installation with `omp plugin list`.

Never infer installation from the skill being present: skills and extensions are discovered independently. Never install or enable an in-process plugin without permission.

Parallel and pipeline modes also require Python `eval`. If Python eval is unavailable, report that prerequisite; do not silently serialize or substitute a different orchestration path.

## Invocation

Supported forms:

```text
/skill:omp-worker <model> -- <prompt>
/skill:omp-worker parallel <model-a> <model-b> ... -- <prompt>
/skill:omp-worker pipeline <model-a> <model-b> ... -- <prompt>
```

Examples:

```text
/skill:omp-worker @smol -- inspect package.json and summarize its scripts
/skill:omp-worker parallel @smol @slow -- review the current diff for correctness
/skill:omp-worker pipeline @smol @slow -- inspect the authentication flow, then verify the inspection
```

Parse the arguments as follows:

1. `parallel` or `pipeline`, when present as the first token, selects the mode. Otherwise use single-worker mode.
2. Everything before the first `--` after the optional mode is the model-selector list.
3. Everything after `--` is the assignment, preserved except for surrounding whitespace and credential redaction.
4. Single mode requires exactly one selector. Parallel mode requires at least two. Pipeline mode requires at least two.
5. Selectors are non-empty OMP model patterns or role aliases such as `@smol`, `@slow`, or `provider/model-id`.
6. Never silently replace a requested selector or turn it into a fallback chain.

On invalid arguments, return only the applicable usage line and do not start workers.

## Protect credentials

Before delegating, replace API keys, access tokens, passwords, authorization headers, cookies, private keys, credential-bearing URLs, and user-identified secrets with stable placeholders such as `<REDACTED_SECRET_1>`. Preserve enough surrounding structure for the worker to reason about the assignment.

Do not delegate a real secret to another model. If the work requires the secret value itself, stop and request a non-secret surrogate.

Every worker prompt must prohibit reading credential files, secret stores, or environment values unless the user explicitly authorized that access. Explicit secret access is allowed only in single-worker mode. Reject parallel or pipeline mode when any worker needs secret access because those modes forward outputs across model boundaries without a parent inspection point.

## Single worker

Call the `worker` tool directly. Supply the requested selector exactly:

```json
{
  "prompt": "<SANITIZED_ASSIGNMENT>",
  "model": "<MODEL_SELECTOR>",
  "label": "<SHORT_LABEL>"
}
```

Use the direct tool for one worker unless the user needs the concrete model behind an alias. Tool-result metadata is reliably available through Python, so use one `tool.worker(...)` Python call when resolved model identity must be reported. Return the worker's substantive result, then verify any factual or code-completion claim required by the parent task.

## Parallel workers

Use parallel mode only when every worker is independent. For editing work, create one ownership-specific prompt per worker containing its exact files and shared interface contract. If ownership cannot be expressed as independent prompts, reject parallel editing and use pipeline mode or serialize the real dependency.

Run one Python `parallel(...)` call:

```python
safety = (
    "Do not read credential files, secret stores, or environment values. "
    "Never include a secret in your response; keep redaction placeholders."
)
jobs = [
    {
        "model": "<MODEL_A>",
        "label": "Worker A",
        "prompt": "<SANITIZED_ASSIGNMENT + EXACT_SCOPE_A>",
    },
    {
        "model": "<MODEL_B>",
        "label": "Worker B",
        "prompt": "<SANITIZED_ASSIGNMENT + EXACT_SCOPE_B>",
    },
]


def run_job(job):
    try:
        return {
            "ok": True,
            "model": job["model"],
            "result": tool.worker({
                "prompt": f"{job['prompt']}\n\n{safety}",
                "model": job["model"],
                "label": job["label"],
            }),
        }
    except Exception as error:
        return {
            "ok": False,
            "model": job["model"],
            "error": str(error),
        }


results = parallel([
    lambda job=job: run_job(job)
    for job in jobs
])
display(results)
```

Each result is a tagged record:

```python
{
    "ok": True,
    "model": "requested-selector",
    "result": {
        "text": "worker final response",
        "details": {
            "model": "resolved-provider/resolved-model",
            "durationMs": 1234,
            "label": "optional label",
        },
    },
}
```

Failures instead contain `{"ok": False, "model": "<requested-selector>", "error": "<message>"}`. Inspect every record. If any failed, the parallel operation failed: report every failed selector and error, and do not present successful siblings as completion.

When all succeeded, judge `record["result"]["text"]` against the user's acceptance criteria. Do not concatenate, vote, or treat agreement as proof. Resolve contradictions from evidence. Report the concrete model in `record["result"]["details"]["model"]` when model identity matters.

## Staged pipeline

Pipeline order is the selector order. Stage 1 receives the original assignment. Every later stage receives the preceding stage's text plus the original assignment and is told exactly what transformation or verification it owns. Reject pipeline mode if any stage needs credential access.

Use one Python `pipeline(...)` call:

```python
models = ["<MODEL_A>", "<MODEL_B>"]
assignment = "<SANITIZED_ASSIGNMENT>"
safety = (
    "Do not read credential files, secret stores, or environment values. "
    "Never include a secret in your response; keep redaction placeholders."
)


def run_stage(prompt, model, label):
    try:
        return tool.worker({
            "prompt": f"{prompt}\n\n{safety}",
            "model": model,
            "label": label,
        })
    except Exception as error:
        raise RuntimeError(f"Worker {model} failed: {error}") from error


def first_stage(_):
    return run_stage(assignment, models[0], "Worker stage 1")


def next_stage(previous, model, stage):
    return run_stage(
        (
            f"Original assignment:\n{assignment}\n\n"
            f"Previous stage output:\n{previous['text']}\n\n"
            "Verify and improve the previous output. Return a complete result."
        ),
        model,
        f"Worker stage {stage}",
    )


stages = [first_stage]
for stage, model in enumerate(models[1:], start=2):
    stages.append(lambda previous, model=model, stage=stage: next_stage(previous, model, stage))

result = pipeline([None], *stages)[0]
display(result)
```

A pipeline has a barrier between stages. It is not an eager DAG scheduler. Use it for a real ordered dependency, not merely to force extra model calls.

When the assignment requires stage-specific behavior, replace the generic "Verify and improve" instruction with the explicit contract, for example `inspect -> implement -> review` or `draft -> fact-check -> final`.

## Failure rules

- A missing or unauthenticated model is a failure. Surface the selector and error; never substitute another model.
- A worker error aborts its call. Do not present partial or older output as success.
- Do not retry unchanged input automatically. Retry only after fixing an actionable cause or when the user requested retry behavior.
- Worker completion is not parent verification. Run the observable check required by the original task.
- For analysis-only work, explicitly tell every worker to remain read-only. Workers otherwise have editing and execution tools.
- Never parallelize overlapping writes.

## Completion

Return only after every requested worker or pipeline stage has completed, contradictions are resolved or stated, secrets remain redacted, and the parent task's verification requirement has been met. Include `details["model"]` when the user requires the concrete model identity; never infer an alias's resolution from memory.
