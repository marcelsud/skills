# Project and release grading

Source: [Grading Methodology Specification](https://github.com/marcelsud/specs/blob/0a3a07de87651622098e0183c9fcf4a15ea64ed8/grading-methodology.md), draft rubric `1.1.1`.
Prepared from the correction proposed in [specs PR #6](https://github.com/marcelsud/specs/pull/6);
check integration and project adoption before treating this revision as policy.
The sections below are preserved verbatim from that revision. Section numbers
and check IDs belong to the source specification.

## 12. Project and release grading

Project health measures code quality. It uses execution grades, ratchets, open
material debt, test trust, and slop delta. It does not use issue value as a
proxy for code health.

Issue and overall PR grades are reported separately as the delivery-value
portfolio.

### 12.1 Project health grade

For this assessment, compare outstanding S2 debt at the release candidate
with the recorded release baseline (section 4.5). Neutral means the same
number of S2 entries; reduced means fewer; net added means more. Compare
each tier separately, without canceling higher-tier debt with lower-tier
removals.

The common conditions for A and B are:

- no D or C condition below holds;
- all required ratchets pass;
- no Blocker or S3 debt exists;
- S2 debt is neutral or reduced relative to the release baseline;
- included execution grades are A or B.

Apply the first matching rule:

1. **D** when any condition holds:
   - an open release-relevant Blocker exists;
   - S3 debt exists;
   - a required release gate is known to produce false positives or cannot run;
   - an emergency D-execution PR remains unresolved.
2. **C** when no D condition holds and any condition holds:
   - the release adds net S2 debt;
   - a ratchet exception is active;
   - an S1 or S2 follow-up has expired;
   - a C execution PR is included.
3. **A** when all common conditions hold and:
   - the release reduces S2 debt, or the baseline contains no S2 debt;
   - no S1 introduced by the release remains present at the release candidate;
   - no required check depends on a known weak or false-positive assertion;
   - all included execution grades are A.
4. **B** when all common conditions hold but at least one additional A
   condition does not hold.

One high-grade PR cannot numerically hide a Blocker or S3 condition.
If the evidence does not establish a rule's conditions, do not infer a
passing health grade. Missing required evidence remains `UNGRADED`;
known failed gates remain failures and block release under their applicable
rules, rather than becoming an automatic B.

### 12.2 Delivery-value portfolio grade

The delivery-value portfolio grade is the worst overall PR grade among
non-exempt PRs included in the release:

```text
release_portfolio_grade = worse(included_overall_pr_grades...)
```

Equivalently:

- **A**: every included overall PR grade is A;
- **B**: at least one B is included and no C or D is included;
- **C**: at least one C is included and no D is included;
- **D**: at least one D is included.

This grade measures the value/quality portfolio selected for the release. It
does not replace the project health grade.

### 12.3 Release reporting and current project grade

```text
current_project_grade = project_health_grade
```

The delivery-value portfolio grade MUST be reported alongside project health,
but MUST NOT be combined with it or used as a proxy for code quality. This
keeps B/C/D-value work visible without treating a well-executed lower-value PR
as a project-health regression.

Every release reports its distribution and derived grades:

```yaml
release: 0.7.0
overall_pr_grades: { A: 7, B: 2, C: 1, D: 0 }
execution_grades: { A: 9, B: 1, C: 0, D: 0 }
slop_delta:
  added: { S3: 0, S2: 0, S1: 1 }
  removed: { S3: 0, S2: 3, S1: 2 }
exceptions: { active: 0, expired: 0 }
project_health_grade: A
release_portfolio_grade: C
current_project_grade: A
```

GPA MAY be displayed as a secondary summary, but MUST NOT determine the project
health or portfolio grade or override their ceilings.

### 12.4 Release ratchet

A release MUST NOT reduce the project health grade without an explicit release
exception. The exception MUST name the material reason, affected grade rule,
owner, and recovery issue. The delivery-value portfolio grade is reported but
is not ratcheted.

An exception records regression; it does not redefine the lower grade as a
higher one.
