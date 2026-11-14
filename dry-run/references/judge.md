# Judge rubric

Compare the delivery with the accepted specification: the stories plus the
spec changes the spec writer accepted. Additional context the spec writer
did not promote is not a requirement. Environment preparation is part of
the comparison only as evidence of whether the next iteration was made
runnable.

The judge compares the dry run with the delivery implementation. The judge
does not edit either workspace, does not polish the trial, and does not
replace the spec author's review.

## Brief

This brief is the prompt the judge receives. Give the judge one brief
containing:

- The stories the trial used, the suggestions, and the spec writer's
  decision on each one. Include the accepted specification and the
  additional context that was attached.
- The friction report, including the spec-author judgment on each item.
- Which environment preparation was completed, and which remains pending.
- What the trial ran, the observed results, and any friction that appeared
  again during delivery.
- The delivery revision, the checks that ran, and their observed results.

Ask the judge to apply the scores and verdict below, to cite evidence for
every score, and to leave a score unset when the evidence is missing.

Omit the preferred verdict, credentials, and secret values. A summary of
the trial may cite files. The brief must not tell the judge to transplant
the trial.

Use this brief only when the user supplied an independent reviewer. When
that reviewer is the spec author or the implementer, skip the comparison.
Do not relabel their review as a judge verdict.

## Scores

Score each dimension from 0 to 4. Higher is better. A number without a
citation is not a score. Do not average the five scores into a benchmark,
and do not treat them as a property of who did the work.

| Score | Anchor |
| --- | --- |
| 0 | The dimension is contradicted or absent. |
| 1 | A major gap remains. |
| 2 | Partial. A material gap remains. |
| 3 | Solid. Only a minor gap remains. |
| 4 | The cited evidence covers the dimension. |

The dimensions are:

- **Spec adherence.** Score the delivery against the accepted
  specification. Extra behavior does not fill a missing requirement.
  Additional context is not a requirement.
- **Deviation control.** A 4 means every material departure from the
  accepted specification is an explicit, evidenced decision. A 0 means the
  delivery substitutes different behavior. When the accepted specification
  leaves no other faithful option, record a remaining spec gap. That is
  not an implementer deviation.
- **Test solidity.** Tests fail when the protected behavior breaks, and
  those tests were run. A suite that restates the implementation, or tests
  that were not run, scores no higher than 1. Do not invent a coverage
  percentage.
- **Rework clarity.** Evident rework is described and traces to the
  accepted specification, to completed environment preparation, or to a
  demonstrated defect. Hidden churn, or rework that only reprints the
  trial, scores low. A delivery with no rework scores 4 only when it also
  shows the trial was not reused without examination.
- **Real improvement.** The delivery closes the accepted changes and does
  not copy the trial's mistakes. Copying a sound approach can score high
  when the accepted specification requires it. Copying a mistake, a choice
  the spec writer rejected, or the trial as a whole caps this score at 1.
  Moving inferable detail into the specification is not an improvement.

## Verdict

Apply these rules in order. The first match is the verdict.

1. `inconclusive`. A material input is missing, or the trial and the
   delivery cannot be compared. Leave missing scores unset.
2. `copied`. Real improvement is 0 or 1 because the delivery repeats the
   trial's mistakes or transplants the trial instead of following the
   accepted specification.
3. `regressed`. The delivery is materially weaker against the accepted
   specification than the friction report shows the trial was against the
   stories it used.
4. `improved`. Spec adherence, deviation control, test solidity, and real
   improvement are each at least 3.
5. `mixed`. None of the above. Name the dimension that holds the verdict
   down.

Rediscovery does not by itself select the verdict. Record each friction
from this task's dry run that appeared again during delivery. If the
accepted specification still omitted a fact that was hard to infer and
depends on the environment, real improvement cannot be 4. An environment
friction whose preparation is still pending is a limit of the next
iteration, not a missed product requirement.

## What the judge returns

Return each score with the citation that supports it, the rediscovered
frictions, the verdict and the rule that selected it, and what evidence
would change the verdict. Do not modify files. Do not supply a score the
brief cannot support.
