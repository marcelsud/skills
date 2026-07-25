# Evidence and risk rubric

Version: `0.1.0`

Adapted from the [Cascade grading methodology](https://raw.githubusercontent.com/marcelsud/specs/refs/heads/main/grading-methodology.md). This reference adds diagnostic confidence, operational exposure, and a mechanical action cutoff. A repository's explicit policy remains authoritative.

## Contents

1. Finding eligibility
2. Severity
3. Diagnostic confidence
4. Operational exposure
5. Disposition matrix
6. Structured evidence
7. Consensus and calibration

## 1. Finding eligibility

A formal finding must answer `yes` to every applicable check:

| ID | Check |
| --- | --- |
| FE-1 | Is there an exact evidence location? |
| FE-2 | Is the defect claim falsifiable? |
| FE-3 | Is the relevant call, data, or lifecycle path reachable? |
| FE-4 | Are the required preconditions explicit? |
| FE-5 | Does the consequence map to a canonical category? |
| FE-6 | Is the confidence classification supported by cited evidence? |
| FE-7 | Is the exposure classification supported by defaults, usage, telemetry, or explicit reasoning? |
| FE-8 | Is the resolution condition binary and observable? |
| FE-9 | For diff review, is the liability introduced or measurably worsened by the change? |

Failure of FE-1 through FE-8 makes the observation a candidate, not a finding. Failure of FE-9 excludes it from a diff review but may leave it eligible for an explicitly requested repository audit.

Canonical consequence categories:

- correctness or data integrity;
- reliability;
- security or privacy;
- operability or observability;
- testing or test trust;
- maintenance or ownership cost.

## 2. Severity

- `blocker`: demonstrated consequence makes ordinary merge or release unsafe, including material security/privacy exposure, data-loss risk, broken core guarantee, or unbounded-resource risk.
- `material`: would change a reasonable merge, design, testing, or operational decision but does not independently make release unsafe.
- `cosmetic`: preference or refinement that would not change a reasonable decision. Omit it.

Incorrect behavior is not automatically a Blocker. Classify the demonstrated consequence, not the defect category or reviewer alarm.

## 3. Diagnostic confidence

- `confirmed`: reproduced by a failing test, runtime observation, incident, benchmark, or direct invariant violation with no unresolved factual assumption.
- `supported`: source, type, control-flow, or data-flow evidence establishes the defect; no material assumption remains, but it has not been reproduced at runtime.
- `speculative`: at least one material claim about reachability, state, API behavior, configuration, or consequence remains unverified. Omit it from the formal review by default.

Confidence answers whether the diagnosis is true. It does not describe how often the defect occurs.

## 4. Operational exposure

- `common`: occurs on a default, documented, or routine path without an unusual external failure.
- `plausible`: occurs in a supported configuration, ordinary edge case, or expected operational failure mode.
- `exceptional`: requires a rare but realistic condition or combination of conditions.
- `unreachable`: a guard, type, invariant, platform guarantee, or proven configuration excludes the path. Reject the candidate.
- `unknown`: available code and evidence cannot establish how often the preconditions occur. Do not silently treat unknown as rare.

Exposure answers how likely the preconditions are in the relevant environment. Use telemetry when available. Otherwise cite defaults, supported configurations, call paths, and the number and independence of required conditions. Never assign an unsupported percentage.

## 5. Disposition matrix

Apply rules from top to bottom:

1. Exposure `unreachable` -> `REJECT`.
2. Confidence `speculative` or severity `cosmetic` -> `OMIT`.
3. A documented hard project gate -> `ACT_NOW`.
4. Severity `blocker` -> `ACT_NOW`.
5. Material with exposure `common` or `plausible` -> `ACT_NOW`.
6. Material with exposure `unknown` -> `VERIFY_NOW`.
7. Material with exposure `exceptional` -> `TRACK`.

Disposition meanings:

- `ACT_NOW`: resolve before ordinary merge or release.
- `VERIFY_NOW`: gather the named missing evidence before deciding to merge.
- `TRACK`: do not block solely on this finding; accept only with explicit ownership and follow-up when project policy requires it.
- `OMIT`: exclude from findings and grading.
- `REJECT`: evidence disproves reachability; retain only in calibration data when useful.

Removing many lower-priority findings cannot cancel one `ACT_NOW` finding. A project hard gate can make an exceptional scenario blocking, especially when it violates an explicit security, data-integrity, compatibility, or resource-bound guarantee.

## 6. Structured evidence

Use this machine-readable classifier input:

```json
{
  "findings": [
    {
      "id": "F-1",
      "severity": "material",
      "confidence": "supported",
      "exposure": "plausible",
      "hard_gate": false
    }
  ]
}
```

The classifier derives disposition and the final decision. The reviewer remains responsible for FE-1 through FE-9 and the complete finding record required by `SKILL.md`.

## 7. Consensus and calibration

Independent reviewers receive the same issue/specification, diff and merge base, CI and ratchet evidence, acceptance evidence, and rubric version. They must not see each other's first pass.

Resolve disagreements by comparing the disputed binary check, exact source evidence, and governing clause. Do not average confidence, vote, or let the lower label win automatically. Escalate for human adjudication only when the disagreement changes the ship decision and factual verification cannot resolve it.

At calibration boundaries, regrade a fixed sample and record:

- disagreement by FE check and classification axis;
- candidates omitted as speculative;
- findings rejected as unreachable;
- false-positive and false-negative machine signals;
- disposition overrides and their decisive evidence.

Change thresholds only after repeated evidence of ambiguity or misclassification. Freeze the rubric version during substantive review.
