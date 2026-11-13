# Judge rubric

Version: `0.1.0`

The judge compares the dry run with the delivery implementation. The judge
does not edit either workspace, does not polish the trial, and does not
replace the spec author's review.

## Brief

This brief is the prompt the judge receives. Give the judge one brief
containing:

- The stories the trial used, spec v2, and what changed between them, with
  the friction that motivated each change.
- The friction report, including the spec-author judgment on each item.
- What the trial ran, the observed results, and any friction that appeared
  again during delivery.
- The delivery revision, the checks that ran, and their observed results.
- The models used for the spec author, the implementer, and the judge, or
  `unknown` when the environment does not identify one. Note a separate
  trial implementer and delivery implementer when they differ.
- This rubric's version.

Ask the judge to apply the scores and verdict below, to cite evidence for
every score, and to leave a score unset when the evidence is missing.

Omit the preferred verdict, credentials, and secret values. A summary of
the trial may cite files. The brief must not tell the judge to transplant
the trial.

If the assigned judge cannot be run, do not execute this brief with the
spec author, the implementer, or the model that is currently writing. Leave
the comparison pending.

## Scores

Score each dimension from 0 to 4. Higher is better. A number without a
citation is not a score. Do not average the five scores into a benchmark,
and do not treat them as a property of a model or a model family.

| Score | Anchor |
| --- | --- |
| 0 | The dimension is contradicted or absent. |
| 1 | A major gap remains. |
| 2 | Partial. A material gap remains. |
| 3 | Solid. Only a minor gap remains. |
| 4 | The cited evidence covers the dimension. |

The dimensions are:

- **Spec adherence.** Score the delivery against spec v2. Extra behavior
  does not fill a missing requirement.
- **Deviation control.** A 4 means every material departure from spec v2 is
  an explicit, evidenced decision. A 0 means the delivery substitutes
  different behavior. When spec v2 leaves no other faithful option, record
  a remaining spec gap. That is not an implementer deviation.
- **Test solidity.** Tests fail when the protected behavior breaks, and
  those tests were run. A suite that restates the implementation, or tests
  that were not run, scores no higher than 1. Do not invent a coverage
  percentage.
- **Rework clarity.** Evident rework is described and traces to spec v2 or
  to a demonstrated defect. Hidden churn, or rework that only reprints the
  trial, scores low. A delivery with no rework scores 4 only when it also
  shows the trial was not reused without examination.
- **Real improvement.** The delivery closes frictions from the trial and
  does not copy the trial's mistakes. Copying a sound approach can score
  high when spec v2 requires it. Copying a mistake, a choice spec v2
  rejected, or the trial as a whole caps this score at 1.

## Verdict

Apply these rules in order. The first match is the verdict.

1. `inconclusive`. A material input is missing, or the trial and the
   delivery cannot be compared. Leave missing scores unset.
2. `copied`. Real improvement is 0 or 1 because the delivery repeats the
   trial's mistakes or transplants the trial instead of following spec v2.
3. `regressed`. The delivery is materially weaker against spec v2 than the
   friction report shows the trial was against the stories it used.
4. `improved`. Spec adherence, deviation control, test solidity, and real
   improvement are each at least 3.
5. `mixed`. None of the above. Name the dimension that holds the verdict
   down.

Rediscovery does not by itself select the verdict. Record each friction
from this task's dry run that appeared again during delivery. If spec v2
still omitted that friction, real improvement cannot be 4.

## What the judge returns

Return the rubric version, each score with the citation that supports it,
the rediscovered frictions, the verdict and the rule that selected it, and
what evidence would change the verdict. Do not modify files. Do not supply
a score the brief cannot support.
