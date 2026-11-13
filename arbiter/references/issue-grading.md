# Issue grading

Source: [Grading Methodology Specification](https://github.com/marcelsud/specs/blob/9b9adf51e1687b950c42f6a6a7e14b5b53b10e7e/grading-methodology.md), draft rubric `1.1.0`.
The sections below are preserved verbatim from that revision. Section numbers
and check IDs belong to the source specification.

## 5. Issue grading

Issue grading occurs during triage, before implementation review.

### 5.1 Issue eligibility gate

Every check requires `yes` and cited evidence. Any `no` result makes the issue
`UNGRADED` and prevents it from authorizing a non-exempt PR.

| ID   | Binary check                                                                                          | Required evidence                                                            |
| ---- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| IE-1 | Is the problem or opportunity stated without prescribing an unverified implementation?                | Issue summary                                                                |
| IE-2 | Is there direct evidence?                                                                             | Reproduction, incident, metric, user request, source invariant, or benchmark |
| IE-3 | Is the consequence stated, including an explicit `none` for a non-consequential request?              | Consequence evidence, or a cited request with `consequence: none`            |
| IE-4 | Is the scope bounded?                                                                                 | Explicit in-scope and out-of-scope boundaries                                |
| IE-5 | Are completion criteria binary and observable?                                                        | Acceptance criteria                                                          |
| IE-6 | Is the required regression proof identified?                                                          | Test, check, benchmark, or runtime observation                               |
| IE-7 | Is the work tied to a current objective, or is it a recorded administrative request using the D path? | Objective identifier from the registry (section 4.8), or request link        |
| IE-8 | Is a 2–3 sentence grade rationale present?                                                            | `Grade rationale` section                                                    |
| IE-9 | Has duplicate or intentional-overlap status been checked?                                             | Search result or linked related issue                                        |

The rationale MUST answer:

1. Why does this matter now?
2. What material decision or outcome changes if it is resolved, or why does
   none change for a D candidate?
3. Why does the selected value grade follow from the rules below?

IE-3 MUST NOT be satisfied by a fabricated impact. A request with no material
consequence MAY record `consequence: none` and cite the underlying request.
That request MAY also satisfy IE-7 without a broader objective. These
alternatives are available only through the D path and force issue grade D
when the remaining eligibility checks pass.

### 5.2 Issue severity

Severity is recorded independently from value grade:

```yaml
severity: blocker | material | cosmetic
```

A feature or debt item may be Material when its evidence would change a
reasonable product, design, or operational decision, even if it is not a bug.

### 5.3 Issue value-grade decision tree

Apply the first matching rule:

1. **D**: The outcome is cosmetic, preference-driven, administrative, or has
   no measurable capability, safety, reliability, or maintenance consequence.
2. **C**: The outcome removes measurable and bounded maintenance or test debt,
   but does not change a user-visible, operational, security, correctness, or
   release decision.
3. **A**: The issue is eligible and any of the following is true:
   - it addresses a Blocker;
   - it protects or restores a core documented guarantee;
   - it affects two or more independent components or user flows;
   - it repairs a project-wide release, security, reliability, or test-trust gate;
   - it is explicitly designated as a release-critical objective with an
     observable outcome.
4. **B**: The issue is eligible and Material, but its demonstrated effect is
   localized and no A rule applies.

An issue MUST NOT receive A solely because it is clearly written, large, or
difficult.

### 5.4 Required issue record

```yaml
rubric_version: 1.1.0
eligibility:
  IE-1: { answer: yes, evidence: "Problem section" }
  IE-2: { answer: yes, evidence: "Reproduction output" }
  IE-3: { answer: yes, evidence: "Impact section" }
  IE-4: { answer: yes, evidence: "Scope section" }
  IE-5: { answer: yes, evidence: "Acceptance criteria" }
  IE-6: { answer: yes, evidence: "Regression test plan" }
  IE-7: { answer: yes, evidence: "Reliability objective R-2" }
  IE-8: { answer: yes, evidence: "Grade rationale" }
  IE-9: { answer: yes, evidence: "No duplicate found" }
severity: material
issue_grade: A
grade_rationale: >-
  This restores an at-least-once delivery guarantee and prevents acknowledged
  messages from being lost after downstream failure. The behavior is a core
  reliability invariant and has a deterministic reproduction.
```

The grade label SHOULD be computed from this record. A manually applied label
without the record is not authoritative.
