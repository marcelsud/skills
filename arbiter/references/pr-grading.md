# Pull request grading and consensus

Source: [Grading Methodology Specification](https://github.com/marcelsud/specs/blob/9b9adf51e1687b950c42f6a6a7e14b5b53b10e7e/grading-methodology.md), draft rubric `1.1.0`.
The sections below are preserved verbatim from that revision. Section numbers
and check IDs belong to the source specification.

## 6. Pull request linkage and exemptions

### 6.1 Required linkage

Every non-trivial PR MUST link exactly one primary graded issue. Additional
issues MAY be linked as secondary scope.

All behavioral changes in the diff MUST trace to the primary issue acceptance
criteria or to documented supporting work required to satisfy them.

If the PR discovers additional independent work, that work MUST be removed or
moved to another issue and PR.

### 6.2 Exempt PR classes

The following MAY be issue-exempt when explicitly labeled:

- clean revert;
- emergency containment;
- automated dependency metadata update with no runtime behavior change;
- administrative repository change;
- release metadata generated from already graded work.

An exemption MUST state why normal issue grading is inapplicable. It does not
skip hard ship gates. Emergency containment MUST receive a follow-up graded
issue before the next release is approved.

An unlinked, non-exempt PR is `UNGRADED` and blocked.

## 7. Hard PR ship gate

Both reviewers answer every check independently. Any `no` result produces
`REWORK`; no execution grade is issued until the failure is resolved.

| ID    | Binary check                                                                        |
| ----- | ----------------------------------------------------------------------------------- |
| SG-1  | Is the primary issue eligible and graded, or is a valid exemption recorded?         |
| SG-2  | Does every behavioral diff segment trace to issue scope?                            |
| SG-3  | Is every acceptance criterion proven by cited evidence?                             |
| SG-4  | Are correctness, security, data-integrity, and resource-bound invariants preserved? |
| SG-5  | Do tests exercise the changed behavior and its material failure path?               |
| SG-6  | Were no tests, assertions, type checks, or CI gates weakened to obtain a pass?      |
| SG-7  | Are all Blocker and Material review findings resolved?                              |
| SG-8  | Do all non-exempt machine ratchets pass?                                            |
| SG-9  | Is the slop ledger complete and evidence-backed?                                    |
| SG-10 | Does the PR contain no S3 slop?                                                     |

Passing CI alone does not prove SG-3, SG-4, or SG-5. Reviewers MUST inspect
whether the evidence covers the stated behavior.

## 8. Execution grading

Execution grading occurs only after all hard ship gates pass.

### 8.1 Execution evidence checks

| ID   | Binary check                                                                                            |
| ---- | ------------------------------------------------------------------------------------------------------- |
| EX-1 | Is the implementation the smallest coherent change that satisfies the issue without unrelated behavior? |
| EX-2 | Does the implementation use existing boundaries and capabilities where appropriate?                     |
| EX-3 | Are public contracts, failure semantics, and lifecycle behavior explicit?                               |
| EX-4 | Do regression tests fail for the pre-change defect or otherwise prove the new capability?               |
| EX-5 | Are tests behavioral rather than assertions of construction, key presence, or line execution only?      |
| EX-6 | Does the implementation avoid new unbounded work, hidden side effects, and silent failure?              |
| EX-7 | Are introduced dependencies and abstractions justified by a current consumer or boundary?               |
| EX-8 | Is observability added or preserved where the changed failure mode requires it?                         |
| EX-9 | Are documentation and examples consistent with the implemented contract?                                |

### 8.2 Mechanical execution grade

After the hard gate passes:

- **A**: EX-1 through EX-9 are `yes`; no S1, S2, or S3 is added; all ratchets
  pass without exception.
- **B**: all hard gates pass; no S2 or S3 is added; one or more S1 entries are
  justified, owned, and linked to follow-up work. Every `no` EX answer MUST
  correspond to one of those S1 entries; an unclassified `no` cannot be used
  to derive a grade.
- **C**: all hard gates pass; no S3 is added; at least one S2 entry or ratchet
  exception is explicitly approved and linked. Every `no` EX answer MUST
  correspond to an approved S1 or S2 entry, and all behavior remains proven.
- **D execution**: the change requires an emergency policy exception that
  cannot satisfy the normal execution floor. It MUST NOT be merged through the
  ordinary workflow and caps project health at D until resolved.

Multiple weak observations MUST NOT be accumulated into a grade penalty unless
each independently qualifies as S1 or higher.

An `EX=no` answer that cannot be classified as S1 or S2 produces `REWORK`.
No execution grade is issued until the implementation makes the answer `yes`
or the reviewer records a qualifying, evidence-backed S1 or S2 entry. An S3
classification fails the hard ship gate.

### 8.3 Overall PR grade

For ordinary PRs:

```text
overall_pr_grade = worse(issue_grade, execution_grade)
```

Examples:

| Issue | Execution | Overall PR |
| ----- | --------- | ---------- |
| A     | A         | A          |
| A     | B         | B          |
| B     | A         | B          |
| C     | A         | C          |
| D     | A         | D          |

A D overall grade may be mergeable when it results from a D-value issue and
the execution grade passes the normal floor. A D execution grade is not
ordinarily mergeable.

## 9. Slop ledger

### 9.1 Slop tiers

| Tier | Definition                                                                         | Policy                                              |
| ---- | ---------------------------------------------------------------------------------- | --------------------------------------------------- |
| S3   | New correctness, security, data-loss, privacy, or unbounded-resource exposure      | Blocks ordinary merge; cannot be waived             |
| S2   | Material reliability, test, coupling, type-safety, dependency, or maintenance debt | Requires approved exception and caps execution at C |
| S1   | Bounded local compromise with a concrete consequence                               | Requires owner and follow-up; caps execution at B   |
| S0   | Cosmetic preference or equivalent formulation                                      | Excluded from reviews and grades                    |

### 9.2 Countable slop categories

A finding counts only when the answer to both questions is `yes`:

1. Is a liability newly introduced or measurably worsened by this PR?
2. Can the reviewer map its concrete consequence to at least one canonical
   category from section 4.6?

Countable categories include:

- dead or unreachable code;
- duplicated business logic that can diverge;
- unchecked type escape such as unjustified `any`, ignored diagnostics, or
  unsafe assertion at a trust boundary;
- swallowed or misclassified error;
- unbounded retry, queue, request, memory, concurrency, or lifecycle behavior;
- implicit or contradictory public contract, failure semantic, or lifecycle
  behavior with a concrete consequence;
- missing or misleading observability for a material failure mode;
- weakened assertion or test that no longer proves the contract;
- dependency duplicating an existing capability with measurable ownership,
  security, size, or runtime cost;
- public abstraction with no current consumer, external contract, test seam,
  or architectural boundary;
- hidden side effect or behavior outside the primary issue scope;
- placeholder, compatibility shim, or temporary branch with no removal path.

### 9.3 Excluded signals

The following do not independently count as slop:

- comment wording;
- naming or formatting preference;
- raw lines changed;
- file length alone;
- a one-caller abstraction with a demonstrated boundary purpose;
- duplication percentage without an identified duplicated business rule;
- complexity score that remains below the configured ceiling;
- preference for extraction over local duplication, or the reverse, without a
  concrete divergence or coupling consequence.

These MAY trigger inspection but MUST NOT affect a grade without qualifying
evidence.

### 9.4 Required slop entry

```yaml
tier: S1
category: bounded_workaround
location: src/example.ts:42
consequence: "A second protocol implementation could classify the error differently."
introduced_by: "PR #123"
justification: "The shared boundary is outside the bounded issue scope."
disposition: follow_up
owner: "@owner"
follow_up_issue: "#124"
target_release: "next"
```

No `file:line`, no consequence, or no introduction evidence means no slop flag.

### 9.5 Slop delta

PRs and releases report counts by tier rather than a single weighted score:

```yaml
slop_delta:
  added: { S3: 0, S2: 0, S1: 1 }
  removed: { S3: 0, S2: 2, S1: 0 }
```

Higher-tier debt MUST NOT be numerically canceled by removing many lower-tier
items.

## 10. Machine ratchets

### 10.1 Baseline

Ratchets compare the PR head with its merge base. Release ratchets compare the
release candidate with the previous release baseline.

Thresholds and exclusions MUST be versioned in the project configuration
artifact defined in section 4.7. Changing the baseline or exclusion list
requires a separately reviewed policy change and MUST NOT be hidden inside a
feature PR.

### 10.2 Required ratchets

| ID   | Machine check              | Pass condition                                                                                       |
| ---- | -------------------------- | ---------------------------------------------------------------------------------------------------- |
| RT-1 | Build and type safety      | No new build, lint, or type error relative to baseline                                               |
| RT-2 | Test integrity             | No new skipped, focused-only, quarantined, or ignored failing test                                   |
| RT-4 | Coverage floor             | Changed scope meets its configured floor and project/package coverage does not cross below its floor |
| RT-5 | Complexity ceiling         | No touched function newly crosses the ceiling; existing hotspot does not worsen                      |
| RT-6 | Duplicate-rule signal      | No new duplicated block is accepted without reviewer classification and evidence                     |
| RT-7 | Dependency policy          | Every new runtime dependency has capability, ownership, and security justification                   |
| RT-8 | Public contract validation | Public configuration/API changes have schema, compatibility, docs, and behavioral tests              |

`RT-3` is intentionally unused in rubric 1.1.0. Behavioral proof is evaluated
by reviewers under SG-5 because a tool cannot determine whether assertions
prove the intended contract. Tools MAY emit test-execution evidence for SG-5,
but that evidence is not itself a machine ratchet.

Coverage percentage and duplication percentage are signals, not proof of test
quality or design quality.

### 10.3 Ratchet exceptions

An exception MUST record:

- failed ratchet ID;
- measured before/after values;
- why satisfying the ratchet would create greater material risk;
- owner;
- follow-up issue;
- target release;
- approving reviewers.

An approved ratchet exception caps execution at C. An expired exception blocks
the next release. RT-1, RT-2, and S3 protections cannot be waived through the
ordinary exception process.

## 11. Two-reviewer consensus protocol

### 11.1 Independent first pass

Both reviewers receive the same frozen inputs:

- issue body and authoritative issue-grade record;
- PR diff and merge-base SHA;
- CI and ratchet output;
- acceptance criteria and test evidence;
- rubric version.

Each reviewer completes the full structured review independently before seeing
the other review.

### 11.2 Required reviewer output

```yaml
rubric_version: 1.1.0
reviewer: reviewer-id
issue_grade: A
ship_gate:
  SG-1: { answer: yes, evidence: "Issue #29" }
  SG-2: { answer: yes, evidence: "All diff paths map to AC-1 or AC-2" }
  SG-3: { answer: yes, evidence: "redis-streams-input.test.ts" }
  SG-4: { answer: yes, evidence: "ACK remains pending on send failure" }
  SG-5: { answer: yes, evidence: "Failure-path integration test" }
  SG-6: { answer: yes, evidence: "No weakened tests or checks" }
  SG-7: { answer: yes, evidence: "No open Blocker/Material findings" }
  SG-8: { answer: yes, evidence: "Ratchet check URL" }
  SG-9: { answer: yes, evidence: "Slop ledger reviewed" }
  SG-10: { answer: yes, evidence: "S3 added = 0" }
execution_checks:
  EX-1: yes
  EX-2: yes
  EX-3: yes
  EX-4: yes
  EX-5: yes
  EX-6: yes
  EX-7: yes
  EX-8: yes
  EX-9: yes
slop_delta:
  added: { S3: 0, S2: 0, S1: 0 }
  removed: { S3: 1, S2: 0, S1: 0 }
findings: []
execution_grade: A
overall_pr_grade: A
decision: APPROVED
```

Every Blocker or Material finding MUST include:

- severity;
- violated rubric or acceptance-criterion ID;
- `file:line` or external evidence;
- concrete consequence;
- binary resolution condition.

### 11.3 Consensus requirements

Consensus requires all of the following:

- same `APPROVED` or `REWORK` decision;
- same answer for every SG check;
- no unresolved Blocker or Material finding from either reviewer;
- same issue grade;
- same execution grade;
- compatible slop entries and tiers.

Matching letters alone do not constitute consensus.

### 11.4 Disagreement resolution

1. Compare only the disagreeing binary checks and evidence.
2. Each reviewer cites the exact rubric clause supporting the answer.
3. Verify disputed factual claims against source, tests, or runtime evidence.
4. Discard Cosmetic disagreements.
5. Update the artifact or finding once for Blocker/Material corrections.
6. The second review round verifies that the correction landed.

If a hard-gate disagreement remains, the PR stays blocked for bounded human
adjudication. The lower grade does not win automatically. The adjudicator MUST
record the decisive fact and clause.

There is no third review round unless a genuine Blocker is discovered.

Final ship-gate question:

> Any Blocker or Material issue? If no → APPROVED.
