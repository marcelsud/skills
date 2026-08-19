---
name: grade-code-review
description: Review code changes and suspected bugs with evidence-backed severity, diagnostic confidence, operational exposure, and quality-gate checks. Use for diffs, pull requests, patches, implementations, release candidates, or generated bug lists. Filter speculation and decide what to fix, verify, track, reject, or omit.
---

# Grade code review

Find broadly, report narrowly. Separate the consequence of a defect from confidence that it exists and likelihood that its preconditions occur.

Read [references/rubric.md](references/rubric.md) completely before grading. Apply a repository-provided rubric when it is stricter or explicitly authoritative; record its version.

## Gather frozen inputs

Collect the diff and merge-base SHA, issue or specification, acceptance criteria, tests and CI evidence, project quality-gate output, and applicable policy. Do not invent missing context. Mark a fact unknown when source, tests, runtime evidence, or telemetry cannot establish it.

Default to diff review. Hold the change responsible only for liabilities it introduces or measurably worsens. Inspect pre-existing code when needed to prove behavior, but do not report unrelated baseline debt. Review the whole repository only when explicitly requested.

## Review workflow

1. Map each behavioral diff segment to an acceptance criterion or stated purpose.
2. Generate candidate defects across correctness, data integrity, reliability, security/privacy, operability/observability, test trust, and maintenance/ownership cost.
3. Falsify each candidate before grading it. Trace callers, data flow, guards, types, lifecycle cleanup, failure paths, configuration defaults, and existing tests. Search for evidence that makes the path unreachable or the consequence impossible.
4. Admit a formal finding only when it has:
   - an exact `file:line` or external evidence location;
   - a falsifiable defect claim;
   - a reachable path and explicit preconditions;
   - a concrete consequence in a canonical category;
   - evidence for confidence and exposure;
   - a binary resolution condition;
   - introduction or worsening evidence for a diff review.
5. Classify severity, confidence, and exposure independently using the rubric. Never convert intuition into a percentage.
6. Run `python3 <skill-directory>/scripts/classify_findings.py <findings.json>` to derive dispositions and the final decision mechanically. Do not select a disposition first and reverse-engineer its inputs.
7. Apply hard project gates after classification. A documented security, data-integrity, resource-bound, or compatibility gate overrides a lower operational priority.
8. Return formal findings ordered by disposition, severity, then evidence strength. Omit cosmetic and speculative observations. Keep rejected candidates out of the main review.

## Output contract

For each reported finding, emit:

```yaml
id: F-1
severity: blocker | material
confidence: confirmed | supported
exposure: common | plausible | exceptional | unknown
disposition: ACT_NOW | VERIFY_NOW | TRACK
location: path/to/file.ts:42
claim: "Falsifiable description of the defect"
preconditions:
  - "Required runtime condition"
consequence_category: reliability
consequence: "Decision-relevant impact"
evidence:
  - "Source, test, trace, metric, or invariant"
introduced_or_worsened_by: "Diff hunk or commit"
resolution: "Binary condition that closes the finding"
```

Derive the final decision from the dispositions. Any `ACT_NOW` produces `REWORK`. Otherwise, any `VERIFY_NOW` produces `NEEDS_EVIDENCE`. With neither, produce `APPROVED`. State the rubric version and whether this was a single review or two-reviewer consensus. Passing CI alone does not prove changed behavior or its material failure path correct.

## Quality rules

Build, type, test-integrity, coverage, complexity, duplication, dependency, and public-contract tools produce evidence. Compare their results with the merge base. A machine signal affects the decision only through a configured threshold or an evidence-backed classification.

Apply these rules to findings:

- Never promote a speculative candidate into a formal finding.
- Never add new scope in a correction round unless a genuine Blocker is discovered.
- Never weaken a test, assertion, type check, or CI gate to obtain approval.
- Never let removal of lower-tier debt cancel a higher-tier liability.
- Record rejected or adjudicated findings for calibration; refine wording only after repeated disagreement.

## Independent consensus

For a ship gate, run two reviewers in separate contexts against identical frozen inputs. Do not reveal either first-pass result to the other. Reconcile only disagreeing facts and rubric clauses. Require agreement on the ship decision and every difference that changes disposition. Adjacent labels that do not change action need not block. If independent execution is unavailable, label the result as a single-review assessment.

## Do not report

- naming, formatting, or equivalent implementation preferences;
- a hypothetical failure without a demonstrated reachable path;
- file length, raw churn, coverage, duplication, or complexity alone;
- pre-existing debt unrelated to the requested review scope;
- a weak test merely because it executes lines or passes CI;
- manually chosen letter grades or numeric likelihood estimates.
