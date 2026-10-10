# Evidence and risk rubric

Version: `0.2.0`

Adapted from the [Cascade grading methodology](https://raw.githubusercontent.com/marcelsud/specs/refs/heads/main/grading-methodology.md). This reference defines the classifications shared by code review and issue triage. A repository's explicit policy remains authoritative.

The selected mode defines eligibility, dispositions, output records, and consensus requirements. Do not apply code review's introduced-or-worsened requirement to issue triage, or issue triage's tracker-state dispositions to a code-review decision.

## Consequence categories

- correctness or data integrity;
- reliability;
- security or privacy;
- operability or observability;
- testing or test trust;
- maintenance or ownership cost.

## Severity

- `blocker`: demonstrated consequence makes ordinary merge or release unsafe in code review, or demands immediate ownership in issue triage. Examples include material security/privacy exposure, data-loss risk, a broken core guarantee, or unbounded-resource risk.
- `material`: would change a reasonable merge, product, design, testing, or operational decision, but does not independently make release unsafe or demand emergency action.
- `cosmetic`: preference or refinement that would not change a reasonable decision. Omit it from code findings and filter it from retained issues.

Incorrect behavior is not automatically a Blocker. Classify the demonstrated consequence, not the defect category or reviewer alarm.

## Diagnostic confidence

- `confirmed`: reproduced by a failing test, runtime observation, incident, benchmark, or direct invariant violation with no unresolved factual assumption.
- `supported`: source, type, control-flow, or data-flow evidence establishes the defect; no material assumption remains, but it has not been reproduced at runtime.
- `speculative`: at least one material claim about reachability, state, API behavior, configuration, or consequence remains unverified. Exclude it from formal code findings and retained issues.

Confidence answers whether the diagnosis is true. It does not describe how often the defect occurs.

## Operational exposure

- `common`: occurs on a default, documented, or routine path without an unusual external failure.
- `plausible`: occurs in a supported configuration, ordinary edge case, or expected operational failure mode.
- `exceptional`: requires a rare but realistic condition or combination of conditions.
- `unreachable`: a guard, type, invariant, platform guarantee, or proven configuration excludes the path. Use the selected mode's reject or filter disposition.
- `unknown`: available code and evidence cannot establish how often the preconditions occur. Do not silently treat unknown as rare.

Exposure answers how likely the preconditions are in the relevant environment. Use telemetry when available. Otherwise cite defaults, supported configurations, call paths, and the number and independence of required conditions. Never assign an unsupported percentage.
