# Issue triage

Investigate broadly, retain narrowly. Filter an issue unless the current repository state supports a falsifiable, decision-relevant problem. Separate defect severity from confidence that it exists and exposure of its preconditions.

Read [rubric.md](rubric.md) completely before grading. Apply a repository-provided issue policy when it is stricter or explicitly authoritative; record its version.

## Gather frozen inputs

Collect the issue set, repository revision, issue bodies and linked evidence, applicable specification or acceptance criteria, tests and CI evidence, existing open and closed issues, active pull requests, and project policy. Freeze the issue IDs and repository revision for the review. Do not invent missing context; mark it unknown.

Review each issue against the current repository state. A report may describe baseline code; unlike diff review, it need not prove which change introduced the defect unless it claims a regression. Do not expand into unrelated repository findings.

## Review workflow

1. Normalize each issue into one falsifiable claim. Split bundled reports only when their claims have independent causes or resolutions.
2. Search existing issues and pull requests for the same root cause and resolution. Similar symptoms alone do not prove duplication.
3. Falsify the claim against the frozen revision. Trace callers, data flow, guards, types, lifecycle cleanup, failure paths, configuration defaults, and tests. Reproduce it when practical.
4. Determine whether the issue is current. A merged fix, proven invariant, unsupported configuration, or unreachable path filters it; a merely proposed fix does not.
5. Admit an issue only when it has:
   - an exact `file:line`, test, trace, log, or other evidence location;
   - a falsifiable problem statement;
   - a reachable path and explicit preconditions;
   - a concrete consequence in a canonical category;
   - evidence for confidence and exposure;
   - a binary resolution condition;
   - no existing issue or pull request owning the same root cause and resolution.
6. Test every admitted issue against the documented project gates and record `hard_gate` in the issue record. A documented security, data-integrity, resource-bound, or compatibility gate is classifier input, not a later override.
7. Classify severity, confidence, and exposure independently using the rubric. Never convert intuition into a percentage.
8. Run `python3 <skill-directory>/scripts/classify_issues.py <issues.json>` to derive dispositions mechanically. Do not select a disposition first and reverse-engineer its inputs.
9. Return retained issues first, verification cases second, and filtered issues last. Preserve original issue IDs and state the evidence for every filter action.

## Output contract

For every reviewed issue, emit:

```yaml
id: I-1
severity: blocker | material | cosmetic
confidence: confirmed | supported | speculative
exposure: common | plausible | exceptional | unreachable | unknown
current: true
duplicate_of: null
hard_gate: true
disposition: KEEP_ACTIONABLE | KEEP_TRACKED | VERIFY | FILTER_DUPLICATE | FILTER_RESOLVED | FILTER_UNREACHABLE | FILTER_UNSUBSTANTIATED
location: path/to/file.ts:42
claim: "Falsifiable description of the problem"
preconditions:
  - "Required runtime condition"
consequence_category: reliability
consequence: "Decision-relevant impact"
evidence:
  - "Source, test, trace, metric, or invariant"
resolution: "Binary condition that closes the issue"
```

`duplicate_of` must name the owning issue or pull request when disposition is `FILTER_DUPLICATE`. `current: false` requires evidence that the problem is already resolved at the frozen revision. For `VERIFY`, name the exact missing evidence and the command, observation, or owner needed to obtain it.

The classifier returns summary counts and each issue's disposition. `KEEP_ACTIONABLE` and `KEEP_TRACKED` remain in the tracker. `VERIFY` remains undecided and must not be presented as valid or filtered. Every `FILTER_*` disposition is excluded from the accepted issue set; close an already-created issue only when the user requested side effects and the evidence is recorded.

## Quality rules

- Never retain a speculative or cosmetic report as an issue.
- Never call two reports duplicates based only on similar titles or symptoms.
- Never filter a current defect merely because its exposure is exceptional.
- Never treat an open pull request as proof that the issue is resolved.
- Never weaken a test, assertion, type check, or CI gate to make a report disappear.
- Never add new issues discovered during this review unless the user explicitly requested a repository audit.
- Record rejected and adjudicated reports for calibration when the workflow supports it.

## Independent consensus

For a high-impact cleanup or automated closure batch, run two reviewers in separate contexts against identical frozen inputs. Do not reveal either first-pass result to the other. Reconcile only disagreeing facts and rubric clauses. Require agreement on every disposition that would close or suppress an issue. If independent execution is unavailable, label the result as a single-review assessment.

## Do not retain

- naming, formatting, or equivalent implementation preferences;
- a hypothetical failure without a demonstrated reachable path;
- a duplicate already owned by an issue or pull request with the same root cause and resolution;
- a report already resolved at the frozen revision;
- file length, raw churn, coverage, duplication, or complexity alone;
- an unsupported feature request presented as a defect;
- manually chosen letter grades or numeric likelihood estimates.

## Issue eligibility

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

Failure of IE-1 through IE-8 makes the report unsubstantiated. Failure of IE-9 makes it resolved or stale. Failure of IE-10 makes it a duplicate. An unknown fact is not a `no`. Use `VERIFY` when one targeted check can decide it.

## Duplicate and current-state checks

A report is a duplicate only when an existing issue or pull request owns both the same root cause and substantially the same resolution. Shared symptoms, files, labels, or keywords are insufficient. Set `duplicate_of` to the owning issue or pull request identifier.

A report is not current only when evidence at the frozen revision proves that its claim is resolved. A merged fix or demonstrated invariant can establish this. An open pull request, planned work, failed reproduction without controlled preconditions, or old line numbers cannot.

`current` and `duplicate_of` describe tracker state, not severity. Check them before prioritizing a valid issue.

## Disposition matrix

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

## Structured evidence

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

## Consensus and calibration

Independent reviewers receive the same issue set, repository revision, specification, CI and runtime evidence, existing issue and pull-request set, and rubric version. They must not see each other's first pass.

Resolve disagreements by comparing the disputed binary check, exact evidence, and governing clause. Do not average confidence or vote. Escalate for human adjudication only when factual verification cannot resolve a disposition that would suppress or close an issue.

During calibration, regrade a fixed sample and record:

- disagreement by IE check and classification axis;
- reports filtered as speculative, cosmetic, duplicate, resolved, or unreachable;
- valid reports incorrectly filtered;
- invalid reports incorrectly retained;
- hard-gate overrides and their decisive evidence.

Change thresholds only after repeated evidence of ambiguity or misclassification. Freeze the rubric version during substantive review.
