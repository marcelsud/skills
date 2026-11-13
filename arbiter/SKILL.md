---
name: arbiter
description: Grade issues, pull requests, reviewer consensus, and release quality using evidence-backed binary checks from marcelsud's grading methodology. Use for eligibility and value grading, execution grading, slop and ratchet assessment, or project-health and delivery-portfolio grades. Ordinary code review without a grading request belongs to the project's review workflow.
metadata:
  author: marcelsud
  rubric-version: "1.1.1"
  source: https://github.com/marcelsud/specs/blob/0a3a07de87651622098e0183c9fcf4a15ea64ed8/grading-methodology.md
---

# Arbiter

Derive grades from independently answered binary checks and cited facts. Keep
issue value, implementation quality, and project health separate. Choose the
letter only after evaluating the evidence.

This skill implements the [Grading Methodology Specification](https://github.com/marcelsud/specs/blob/0a3a07de87651622098e0183c9fcf4a15ea64ed8/grading-methodology.md),
draft rubric `1.1.1`. Its linked references preserve the applicable source
sections verbatim. Read the reference for the requested mode before grading.

This revision was prepared from the correction proposed in [specs PR #6](https://github.com/marcelsud/specs/pull/6).
Verify that PR's integration status and the target project's adopted version.
Integrate the normative correction before this skill update. A proposed source
revision does not establish adoption or replace a project's frozen rubric.

## Establish the grading context

Identify the artifact and revision being assessed, the requested mode, and
the project's adopted rubric version. Read its versioned configuration for
the objective registry, ratchet commands, thresholds, exclusions, and approved
exceptions. Each objective must have a stable ID and a stated guarantee; an
identifier absent from the registry does not satisfy IE-7. Do not invent an
objective, threshold, exemption, or approval to fill a gap.

Record `rubric_version` in every grading record. Freeze the rubric when
substantive PR review starts. If a project adopts another version, obtain
that version before issuing its grades; do not silently apply this snapshot.
When no adoption or configuration exists, offer an explicitly provisional
assessment under `1.1.1` and identify what prevents an authoritative grade.

Missing required evidence means `UNGRADED`, not a lower letter or an assumed
pass. Preserve known failures and name the evidence needed to resolve unknowns.
Use `REWORK` for failed PR gates. Keep an assessment of ship readiness separate
from permission to merge or release. Assessing an artifact does not authorize
editing it, posting findings, changing labels, or publishing it.

## Classify consequences

Use the source definitions: Blocker means factually wrong behavior, security
exposure, data-loss risk, or another condition that makes merge or release
unsafe. Material means information that changes a reasonable merge, design,
or operational decision. Cosmetic means a preference that does not change
such a decision. Exclude cosmetic findings from grading and consensus.

Every consequential finding must map to correctness or data integrity,
reliability, security or privacy, operability or observability, testing or test
trust, or maintenance or ownership cost. Include severity, the violated check
or acceptance criterion, `file:line` or external evidence, the concrete
consequence, and a binary resolution condition.

For PR slop, prove that the liability is introduced or measurably worsened
relative to the baseline. Existing debt is not automatically a PR finding;
touched hotspots must not worsen without an approved exception. Comment
wording, naming, file length, line count, and equivalent implementations do
not independently count. A one-caller abstraction may protect a real boundary.
Do not apply the PR introduction test to the value of an issue about old debt.

## Grade the requested artifact

- **Issue:** Read [issue-grading.md](references/issue-grading.md). Answer IE-1
  through IE-9 with evidence before applying the value decision tree in its
  stated order: D, C, A, B. Record severity independently. A cosmetic request
  can follow the documented D path with `consequence: none`; never fabricate
  impact to make it eligible. Include the required two-to-three-sentence
  rationale and evidence-backed eligibility record.
- **Pull request:** Read [pr-grading.md](references/pr-grading.md), and use
  [issue-grading.md](references/issue-grading.md) to verify the primary issue's
  authoritative record. Check linkage or a valid labeled exemption, then
  SG-1 through SG-10. A failed gate means `REWORK` with no execution grade.
  Only after the gates pass, evaluate EX-1 through EX-9 and derive the execution
  grade. Every EX `no` needs a qualifying S1 or S2 entry; an unclassified `no`
  means `REWORK`. S3 blocks ordinary merge and cannot be waived. Never trade
  removed low-tier debt against added high-tier debt. For ordinary PRs,
  compute `overall_pr_grade = worse(issue_grade, execution_grade)`.
- **Reviewer consensus:** Read the PR reference's section 11. Obtain two
  genuinely independent first-pass reviews of the same frozen issue, diff,
  merge base, check output, acceptance evidence, and rubric. Do not expose
  either review to the other before both are complete. Compare every SG
  answer, decision, issue grade, execution grade, and slop entry, not letters
  alone. Verify factual disagreements and discard cosmetic ones. Use the
  second round to verify corrections; unresolved hard-gate disagreement needs
  bounded human adjudication. A third round requires a genuine Blocker.
  Without a second reviewer, report only the available assessment and pending
  consensus. Re-reading one's own work is not independent review.
- **Project or release:** Read [release-grading.md](references/release-grading.md).
  Identify the previous release or recorded baseline and the complete included
  PR set. Derive project health from execution grades, ratchets, material debt,
  test trust, and slop changes. Report the worst non-exempt overall PR grade
  separately as the delivery portfolio. `current_project_grade` equals project
  health. A D-value issue with sound execution does not itself lower health.
  Apply the explicit health-regression exception and recovery requirements.

## Preserve the evidence

Use the structured records in the relevant reference. Include artifact and
baseline revisions, all required answers with citations, the slop ledger,
exceptions with their owners and approvals, derived grades, and unresolved
requirements. The order is `A > B > C > D`; `worse()` with no grades is A.
`UNGRADED` must stop a calculation, never enter it as a grade. Do not invent
an issue-value grade for an exempt PR or include it in the release portfolio.

Inspect what tests prove, including material failure paths. Green CI,
coverage percentages, and labels alone do not prove the contract. Use actual
machine output for configured ratchets; disclose unavailable checks. Never
weaken a test, threshold, exclusion, or baseline to manufacture a pass.

Retain enough evidence to reconstruct each decision. Author-proposed grades
are provisional; authoritative PR grading requires the source's reviewer
consensus and automated calculation. If that capability is unavailable,
report the derived proposal and the missing requirement without claiming
final approval. Keep policy changes separate from the artifact being graded.
If source clauses conflict, cite the clauses, show their effect on the result,
and request recorded clarification before presenting an authoritative affected
grade. Do not silently reorder a decision tree or revise a frozen rubric.
For methodology adoption or integration requests, consult source sections
13, 15, and 16; grading a project does not itself authorize installing gates.
