# Evidence and issue-retention rubric

Version: `0.1.0`

Adapted from the sibling `grade-code-review` evidence and risk rubric. This reference adds duplicate and current-state checks and maps the evidence classes to issue-retention dispositions. A repository's explicit policy remains authoritative.

## Contents

1. Issue eligibility
2. Duplicate and current-state checks
3. Severity
4. Diagnostic confidence
5. Operational exposure
6. Disposition matrix
7. Structured evidence
8. Consensus and calibration

## 1. Issue eligibility

A retained issue must answer `yes` to every applicable check:

| ID | Check |
| --- | --- |
| IE-1 | Is there an exact source, test, trace, log, or external evidence location? |
| IE-2 | Is the problem claim falsifiable? |
| IE-3 | Is the relevant call, data, or lifecycle path reachable? |
| IE-4 | Are the required preconditions explicit? |
| IE-5 | Does the consequence map to a canonical category? |
| IE-6 | Is the confidence classification supported by cited evidence? |
| IE-7 | Is exposure supported by defaults, usage, telemetry, or explicit reasoning? |
| IE-8 | Is the resolution condition binary and observable? |
| IE-9 | Is the problem current at the frozen repository revision? |
| IE-10 | Is there no existing issue or pull request owning the same root cause and resolution? |

Failure of IE-1 through IE-8 makes the report unsubstantiated. Failure of IE-9 makes it resolved or stale. Failure of IE-10 makes it a duplicate. An unknown fact is not a `no`: use `VERIFY` when a targeted check can decide it.

Canonical consequence categories:

- correctness or data integrity;
- reliability;
- security or privacy;
- operability or observability;
- testing or test trust;
- maintenance or ownership cost.

## 2. Duplicate and current-state checks

A report is a duplicate only when an existing issue or pull request owns both the same root cause and substantially the same resolution. Shared symptoms, files, labels, or keywords are insufficient. Set `duplicate_of` to the owning issue or pull request identifier.

A report is not current only when evidence at the frozen revision proves that its claim is resolved. A merged fix or demonstrated invariant can establish this. An open pull request, planned work, failed reproduction without controlled preconditions, or old line numbers cannot.

`current` and `duplicate_of` describe tracker state, not severity. Check them before prioritizing a valid issue.

## 3. Severity

- `blocker`: demonstrated consequence demands immediate ownership, including material security/privacy exposure, data-loss risk, broken core guarantee, or unbounded-resource risk.
- `material`: would change a reasonable product, design, testing, or operational decision but does not independently demand emergency action.
- `cosmetic`: preference or refinement that would not change a reasonable decision. Filter it.

Incorrect behavior is not automatically a Blocker. Classify the demonstrated consequence, not the defect category or reporter alarm.

## 4. Diagnostic confidence

- `confirmed`: reproduced by a failing test, runtime observation, incident, benchmark, or direct invariant violation with no unresolved factual assumption.
- `supported`: source, type, control-flow, or data-flow evidence establishes the defect; no material assumption remains, but it has not been reproduced at runtime.
- `speculative`: at least one material claim about reachability, state, API behavior, configuration, or consequence remains unverified. Filter it. `VERIFY` is reserved for a supported material issue whose operational exposure is unknown.

Confidence answers whether the diagnosis is true. It does not describe how often the defect occurs.

## 5. Operational exposure

- `common`: occurs on a default, documented, or routine path without an unusual external failure.
- `plausible`: occurs in a supported configuration, ordinary edge case, or expected operational failure mode.
- `exceptional`: requires a rare but realistic condition or combination of conditions.
- `unreachable`: a guard, type, invariant, platform guarantee, or proven configuration excludes the path. Filter it.
- `unknown`: available evidence cannot establish how often the preconditions occur. Do not silently treat unknown as rare.

Exposure answers how likely the preconditions are in the relevant environment. Use telemetry when available. Otherwise cite defaults, supported configurations, call paths, and the number and independence of required conditions. Never assign an unsupported percentage.

## 6. Disposition matrix

Apply rules from top to bottom:

1. Non-null `duplicate_of` -> `FILTER_DUPLICATE`.
2. `current: false` -> `FILTER_RESOLVED`.
3. Exposure `unreachable` -> `FILTER_UNREACHABLE`.
4. Confidence `speculative` or severity `cosmetic` -> `FILTER_UNSUBSTANTIATED`.
5. A documented hard project gate -> `KEEP_ACTIONABLE`.
6. Severity `blocker` -> `KEEP_ACTIONABLE`.
7. Material with exposure `common` or `plausible` -> `KEEP_ACTIONABLE`.
8. Material with exposure `unknown` -> `VERIFY`.
9. Material with exposure `exceptional` -> `KEEP_TRACKED`.

Disposition meanings:

- `KEEP_ACTIONABLE`: retain with ordinary or urgent ownership according to project policy.
- `KEEP_TRACKED`: retain, but do not escalate solely on this report; exceptional exposure is not invalidity.
- `VERIFY`: gather the named missing evidence before retaining or filtering.
- `FILTER_DUPLICATE`: exclude in favor of the named owner.
- `FILTER_RESOLVED`: exclude because the frozen revision already resolves the claim.
- `FILTER_UNREACHABLE`: exclude because evidence disproves the required path.
- `FILTER_UNSUBSTANTIATED`: exclude because the report is speculative or cosmetic.

A project hard gate can make an exceptional scenario actionable, especially when it violates an explicit security, data-integrity, compatibility, or resource-bound guarantee.

## 7. Structured evidence

Use this classifier input:

```json
{
  "issues": [
    {
      "id": "I-1",
      "severity": "material",
      "confidence": "supported",
      "exposure": "plausible",
      "current": true,
      "duplicate_of": null,
      "hard_gate": false
    }
  ]
}
```

The classifier derives dispositions and summary counts. The reviewer remains responsible for IE-1 through IE-10 and the complete issue record required by `SKILL.md`.

## 8. Consensus and calibration

Independent reviewers receive the same issue set, repository revision, specification, CI and runtime evidence, existing issue and pull-request set, and rubric version. They must not see each other's first pass.

Resolve disagreements by comparing the disputed binary check, exact evidence, and governing clause. Do not average confidence or vote. Escalate for human adjudication only when factual verification cannot resolve a disposition that would suppress or close an issue.

At calibration boundaries, regrade a fixed sample and record:

- disagreement by IE check and classification axis;
- reports filtered as speculative, cosmetic, duplicate, resolved, or unreachable;
- valid reports incorrectly filtered;
- invalid reports incorrectly retained;
- hard-gate overrides and their decisive evidence.

Change thresholds only after repeated evidence of ambiguity or misclassification. Freeze the rubric version during substantive review.
