---
name: grade-issue-review
description: Review newly created or proposed issues with evidence-backed severity, diagnostic confidence, operational exposure, and duplicate or stale-state checks. Use when Codex must triage an LLM-generated issue batch, filter false positives, duplicates, resolved reports, cosmetic requests, or speculative claims, and retain only actionable or explicitly tracked issues.
---

# Grade Issue Review

Investigate broadly, retain narrowly. Filter an issue unless the current repository state supports a falsifiable, decision-relevant problem. Separate defect severity from confidence that it exists and exposure of its preconditions.

Read [references/rubric.md](references/rubric.md) completely before grading. Apply a repository-provided issue policy when it is stricter or explicitly authoritative; record its version.

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
6. Classify severity, confidence, and exposure independently using the rubric. Never convert intuition into a percentage.
7. Run `python3 <skill-directory>/scripts/classify_issues.py <issues.json>` to derive dispositions mechanically. Do not select a disposition first and reverse-engineer its inputs.
8. Return retained issues first, verification cases second, and filtered issues last. Preserve original issue IDs and state the evidence for every filter action.

## Output contract

For every reviewed issue, emit:

```yaml
id: I-1
severity: blocker | material | cosmetic
confidence: confirmed | supported | speculative
exposure: common | plausible | exceptional | unreachable | unknown
current: true
duplicate_of: null
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

## Ratchets

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
