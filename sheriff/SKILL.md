---
name: sheriff
description: Review code changes or triage issue reports using evidence-backed severity, diagnostic confidence, operational exposure, and project gates. Use for diffs, pull requests, patches, release candidates, or issue and bug-report batches. Check duplicates and current state during triage; return review decisions or issue-retention dispositions.
---

# Sheriff

Find broadly, report narrowly. Separate the consequence of a defect from confidence that it exists and likelihood that its preconditions occur.

## Select the mode

| Request | Mode and instructions |
| --- | --- |
| Review a diff, pull request, patch, implementation, or release candidate | [Code review](references/code-review.md) |
| Review existing or proposed issues, triage reports, or check duplicates and stale reports | [Issue triage](references/issue-triage.md) |

A list of suspected bugs about a specific change follows code review. A list of existing or proposed issue reports follows issue triage. A ticket supplied as context for a diff does not change the mode.

If the target is ambiguous, ask whether the user wants a change reviewed or reports triaged. If both are requested, run both modes against their respective scopes and keep their outputs separate.

Read [references/rubric.md](references/rubric.md) completely, then read only the selected mode's instructions. Apply a repository-provided policy when it is stricter or explicitly authoritative; record its version.

## Shared rules

- Freeze the selected mode's inputs and repository revision. Do not invent missing context; mark unsupported facts unknown.
- Falsify candidates by tracing reachable paths, preconditions, guards, and consequences before classifying them.
- Grade severity, diagnostic confidence, and operational exposure independently. Never invent numeric likelihoods.
- Treat tool signals as evidence. A signal affects a decision only through a documented threshold or an evidence-backed classification.
- Record documented project gates as `hard_gate`. Run the selected mode's classifier to derive dispositions; do not choose the outcome first.
- Never weaken tests, assertions, types, or CI gates to obtain approval or make an issue disappear.
- Report the shared rubric version and whether the result is a single-review assessment or independent consensus.

## Results

- **Code review:** `classify_findings.py` returns `REWORK`, `NEEDS_EVIDENCE`, or `APPROVED`.
- **Issue triage:** `classify_issues.py` returns issue-retention dispositions and keep, verify, and filter counts. Tracker changes require explicit user authorization.
