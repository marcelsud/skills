---
name: workflow-hardening
description: Harden GitHub Actions workflows that build and deploy. Use when adding, reviewing, or revising a workflow, especially one that deploys or uses secrets, including Cloudflare Pages deploys.
---

# Workflow hardening

Keep build work free of secrets, grant each job only the permissions it
needs, and make workflow files safe to review and reuse. Apply this
checklist when writing or reviewing a GitHub Actions workflow.

## Separate build from deploy

Put the secret-free build in its own job. The deploy job should be a
later job that consumes build artifacts and is the only job that needs
deployment credentials.

Store those credentials in a protected environment, and run the deploy
job in that environment. Do not place secrets on the secret-free build
job, and do not give the build job access to the protected environment
unless the build truly requires it.

## Declare minimal permissions

Set default permissions to the narrowest safe baseline, typically
`contents: read` or no permissions, and grant additional permissions
per job only when that job needs them. A deploy job may need
`contents: read` plus the specific permission required by its deployment
target; a job that only builds or tests should not inherit deploy
permissions.

## Pin actions by commit

Reference third-party and first-party actions by a full commit SHA, not
a mutable tag or branch. A tag can be moved; a SHA cannot. Record the
human-readable version beside the SHA in a comment when that helps later
review.

## Pass expressions through environment variables

Do not interpolate `${{ }}` expressions directly inside a `run:` script.
Assign them to an `env:` value and read the environment variable in the
script. Interpolation inside the script can break quoting and can turn
untrusted workflow data into shell syntax.

## Limit concurrency cancellation

If the workflow cancels in-progress runs, do so only for non-default
branches. Do not cancel an in-progress run on the default branch
(commonly `main`); a deploy or protected-branch job should be allowed
to finish.

## Include the workflow in path filters

When the workflow uses a `paths` filter, include the workflow file
itself in that filter. Otherwise a change to the workflow will not run
the workflow, and the revised behavior will not be exercised until some
other matching path changes.

## Scope deployment tokens

For a Cloudflare Pages deploy, use an API token whose account or
resource scope is limited to Pages Edit, and nothing broader. Store it
in the protected environment used by the deploy job. For other deploy
targets, use the narrowest token the platform offers for that operation
alone.

## Report remaining gaps

When reviewing an existing workflow, list each unmet item with the file
and job or step involved, the risk, and the concrete change that would
close it. Do not approve a workflow that interpolates untrusted
expressions into `run:`, that pins actions by a mutable tag, or that
exposes secrets to a job that does not need them.
