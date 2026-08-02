---
name: sonarqube-code-analysis
description: Run local SonarQube analysis. Import coverage and turn scanner signals into evidence-backed findings. Use when the user asks to scan a repository or inspect SonarQube results. Use the skill to explain a quality gate or triage code with SonarQube. Default to local analysis. Do not add CI unless the user asks.
---

# SonarQube Code Analysis

Use SonarQube Community Build for evidence. Do not use a SonarQube label for a final code-review decision.

Default to local analysis. Do not add CI, repository secrets, or hosted integration unless the user asks.

## Safety contract

- Read the server URL from `SONAR_HOST_URL`.
- Read the analysis token from `SONAR_TOKEN`.
- Never print or log a token. Never delegate or commit a token.
- Prefer a project analysis token when you create a token.
- Keep a stored token outside the repository with mode `0600`.
- Do not put credentials in `sonar-project.properties`.
- Do not commit `.scannerwork/` or generated coverage output.

A scan updates the analysis for its project key. Use a separate project key if an existing local baseline must remain unchanged.

## Check the local tools

Use `sonar-scanner` for a full repository scan. Do not substitute the separate `sonar` command.

Resolve the scanner before you change the repository.

```bash
if command -v sonar-scanner >/dev/null 2>&1; then
  SCANNER=sonar-scanner
elif [ -x "$HOME/sonar-experiment/sonar-scanner" ]; then
  SCANNER="$HOME/sonar-experiment/sonar-scanner"
else
  echo "SonarScanner CLI is not installed" >&2
  exit 1
fi
```

Check the environment without displaying the token.

```bash
test -n "${SONAR_HOST_URL:-}"
test -n "${SONAR_TOKEN:-}"
curl -fsS "$SONAR_HOST_URL/api/system/status"
"$SCANNER" -v
```

If a known local server is stopped, start the server. Do not install or reconfigure a server unless the user asks.

Use the scanner made for the build system when one exists. Use the Maven, Gradle, or .NET scanner for those projects.

## Configure the project

Read the build files and test configuration. Identify source roots, test roots, and ignored files. Reuse an existing `sonar-project.properties` file.

If the file does not exist, create the smallest correct file at the repository root.

```properties
sonar.projectKey=<stable-local-key>
sonar.projectName=<project-name>
sonar.sources=<source-roots>
sonar.tests=<test-roots>
sonar.sourceEncoding=UTF-8
```

Add exclusions only for generated files or established project policy. Keep source and test scopes separate.

For JavaScript or TypeScript, generate LCOV before the scan. Set the LCOV path in the project file.

```properties
sonar.javascript.lcov.reportPaths=coverage/lcov.info
```

Match SonarQube coverage exclusions to the test runner. A scope mismatch makes coverage values misleading.

## Generate analysis inputs

Use existing project commands. Do not add a second test runner or replace an established coverage tool.

- Run the existing build or type check when the analysis needs compiled metadata.
- Run the existing coverage command.
- Check the configured report. The report must exist and contain data.
- Record the commit SHA. Record whether the worktree is dirty.

SonarQube does not run tests or calculate test coverage. SonarQube imports the report from the coverage tool.

For JavaScript or TypeScript, check LCOV with the following command.

```bash
test -s coverage/lcov.info
```

## Run the scan

Run the scanner from the repository root.

```bash
"$SCANNER"
```

Do not pass the token through a command-line property. Environment variables keep the token out of shell history and command arguments.

Read `.scannerwork/report-task.txt` after upload. Record `ceTaskId` and `ceTaskUrl`. Record `dashboardUrl` and `serverUrl`.

Scanner exit code zero means the report upload succeeded. The analysis is complete only when the Compute Engine task has status `SUCCESS`.

Use a user token for Web API reads when the server requires authentication. Do not assume an analysis-only token can browse issues or metrics.

If no browse credential is available, open `dashboardUrl` and report upload success separately from analysis completion.

## Collect results

After the Compute Engine task succeeds, collect these result groups.

- quality gate status and evaluated conditions.
- coverage measures.
- duplication and complexity measures.
- code size.
- open issues by issue type.
- security hotspots.
- issue rule, location, and message.
- issue impact, status, and creation context.

Use the Web API when access is available. Paginate issue searches until all pages are read.

Use these Web API endpoints.

```text
/api/ce/task?id=<task-id>
/api/qualitygates/project_status?projectKey=<project-key>
/api/measures/component?component=<project-key>&metricKeys=<keys>
/api/issues/search?componentKeys=<project-key>&statuses=OPEN,CONFIRMED,REOPENED
/api/hotspots/search?projectKey=<project-key>
/api/rules/show?key=<rule-key>
```

An `OK` gate can have no evaluated conditions. An empty condition set does not prove clean code. Report the empty condition set.

## Turn signals into findings

A SonarQube issue is a candidate. Verify the candidate before you report or fix the issue.

- Read the complete function or module around the issue.
- Trace callers and guards.
- Trace types, data flow, and failure paths.
- Read applicable tests and project policy.
- Reproduce the behavior when the claim is uncertain.
- Classify whether the issue is new or existing.
- Determine whether the code path is reachable or intentional.
- State the concrete consequence and trigger.

Use `$grade-code-review` when the user needs a review decision. Apply its evidence and severity rules.

Apply these interpretation rules:

- A bug or vulnerability label is a lead, not proof.
- A security hotspot requires review. A security hotspot is not automatically a vulnerability.
- Coverage and code size are prioritization signals. Complexity and duplication are also signals. These signals are not defects by themselves.
- A rule can be correct generally and wrong for the local context.
- A clean scan means no actionable SonarQube finding was confirmed. A clean scan does not prove defect-free code.

Do not change code during analysis. Change code only when the user asks for remediation. Fix confirmed findings and run the same scan again.

## Output contract

Return the scan facts before the findings.

```text
Scan: SUCCESS | UPLOAD_ONLY | FAILED
Project key: <key>
Revision: <sha> [clean | dirty]
Server: <version and URL>
Scanner: <version>
Coverage report: <path or none>
Quality gate: <status and evaluated conditions>
Measures: <selected values>
Dashboard: <URL>
```

For each actionable finding, return the following data.

```text
<file>:<line> | <rule> | <impact>
Claim: <falsifiable defect claim>
Trigger: <reachable precondition>
Consequence: <decision-relevant result>
Evidence: <source, test, trace, or runtime evidence>
Action: <binary fix or verification condition>
```

List dismissed signals separately with a short reason. Do not include cosmetic findings. Do not use raw issue counts for recommendations.

## Troubleshooting

- `401` or `403`: check the token type and expiration. Check project permissions. Do not display the token.
- Zero coverage: check report generation and the configured path. Check LCOV source paths and coverage exclusions.
- Upload succeeded but results are stale: wait for the Compute Engine task.
- Missing blame data: scan a committed checkout with sufficient Git history.
- Scanner failure: rerun with `-X`. Diagnose the first root error.
- Wrong scanner: use the scanner made for Maven, Gradle, or .NET.

Remove `.scannerwork/` after you collect the analysis evidence. Keep server data or coverage output only when the user needs them.
