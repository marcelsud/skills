---
name: make-no-mistakes
description: Validate or ship code changes through an agent-orchestrated gate. Kernel is intent, independent review, targeted tests, docs, and lint. Default profile also rebases, pushes, opens a PR, and watches CI. Use when the user asks to run make-no-mistakes, gate or ship or validate their changes, push safely, asks you to do a task and then validate it, or invokes /make-no-mistakes.
user-invocable: true
argument-hint: "[task | profile=<name> | skip=<steps>]"
---

# make-no-mistakes

Agent-owned gate. You run every phase yourself. There is no `no-mistakes` CLI,
daemon, AXI loop, disposable worktree, or skill script. Do not install, call,
or wait on that binary.

Resolve the **profile**, then run only its phases. Config schema:
[config.md](config.md).

```
profile=  →  .make-no-mistakes.yaml  →  pr-ship
```

`profile=` on the invocation wins. Unknown yaml keys are ignored. Missing file
is `pr-ship`.

Per-run skips are allowed (`skip lint`, `--skip=test,lint`). Do not add
undeclared phases. Do not skip a phase the profile includes unless the user
skipped it. Do not skip **intent**. Do not skip **review** unless the user
explicitly skipped review.

## Kernel

Always on, every profile:

- Capture **intent** before any later phase. Later phases grade against it.
- Never self-review. Never silently substitute a required review seat.
- Review uses the rubric in [Review](#review). Do not replace it with a
  different severity scale or an open-ended "what do you think?" pass.
- Tests hit a public interface, not source strings. See [Test](#test).
- Cap automatic fix attempts at 3 per mutating phase (rebase, test, lint, CI,
  integrate conflicts). Then ask.
- Do not claim CI is green unless you saw the checks on the SHA you pushed.
- You are in the user's working tree. There is no isolated gate worktree.
  Do not stash, reset, or clean files you did not create for this run.
  Leave unrelated dirty files unstaged.

## Two ways to invoke

Flags are `profile=<name>` and `skip=…` / `skip <phase>` / `--skip=a,b`.
Remaining text is the task. Bare `/make-no-mistakes` is validate-only.

- **Validate-only** — changes are already the work to gate. Then run the
  profile.
- **Task-first** — do the task, then gate it:
  1. Inspect `git status` before you touch anything. Leave unrelated dirty
     files alone. Commit only the task's files when the profile requires
     commits.
  2. Branch creation is profile-owned (see [Profiles](#profiles)).
  3. Do the work.
  4. Run the profile. The user's task text **is** the intent — keep their
     requirements, constraints, exclusions, and later decisions verbatim.
     Add only the decisions and tradeoffs you made while implementing.

## Profiles

### `pr-ship` (default)

```
intent → rebase → review → test → document → lint → push → pr → ci
```

- `integrate: rebase`, `review.when: pre-publish`, `review.on: committed`
- `deliver.kind: pr`, `deliver.merge: never`
- Work to validate is **committed** on a **feature branch**, not the default
  branch. Uncommitted task work gets committed first.
- If `HEAD` is the default branch, create a feature branch first.

### `local-validate`

```
intent → review → test → document → lint
```

- `integrate: none`, `deliver.kind: none`
- `review.when: pre-publish`
- `review.on: worktree` if the task work is dirty; `committed` if it is
  already committed
- No feature-branch requirement. Do not push, open a PR, or watch CI.
- Done when the local phases pass. Report that nothing was published.

### `repo`

The repo's delivery document is the profile (`AGENTS.md`, a seating doc, or
`.make-no-mistakes.yaml` pointing at one). This skill supplies the kernel and
the phase specs below. It does not invent a pipeline.

If that document is missing, stop and say so. If it names seats or a host
the session cannot run, stop — never substitute.

## Phases

### Intent

Write the intent down and keep it in every later prompt.

Intent is **what the user set out to accomplish**, in their terms — not a
diff summary. Err long: goal, decisions, tradeoffs, constraints, ruled-in
and ruled-out approaches, anything that would look surprising in the diff.

A thin one-liner makes review invent objections the user already chose.

### Rebase

Only when the profile has `integrate: rebase`. For `merge`, merge
`<remote>/<default>` instead of rebasing; keep the safety rules. For `none`,
skip this phase.

1. Default branch is `default_branch` when set, else the remote `HEAD`
   symbolic ref, else `origin/main`, else `origin/master`.
2. `git fetch` the default branch and, if it exists, the remote feature branch.
3. If the feature branch is behind the remote feature branch, rebase onto
   that first, then onto `<remote>/<default>`. Skip a target that does not
   exist or is already an ancestor. Fast-forward with reset only when the
   target is a strict ancestor of `HEAD`.
4. If `HEAD` contains commits from the **local** default branch that are
   not on `<remote>/<default>`, stop and ask. Do not silently bundle them.
5. On conflict: stop, show the conflicted files, and either resolve (smallest
   correct merge of both sides, then `git rebase --continue` or
   `git merge --continue`) or ask. Abort rather than leave a half-integrate.
6. If the diff against `<remote>/<default>` is empty after integrate, stop.
   The rest of the pipeline has nothing to gate.

### Review

The rubric below is the only review contract. A `repo` profile may run this
phase more than once (`pre-publish` and `post-publish`). It may not replace
the rubric.

#### Independence

Never self-review. Dispatch a **read-only** independent reviewer
(`reviewer` agent, or the seating doc if one is named). The reviewer sees
the intent, the snapshot, and the worktree path. It does not see your
private rationale beyond what is in the intent. It must not edit, commit,
push, or run repo-wide suites.

Snapshot is the committed diff against the merge base when
`review.on: committed`, or the worktree diff when `review.on: worktree`.
`committed` with uncommitted task work: commit first (`pr-ship`) or stop.

If the repo or config defines review seating (models, pair review,
publication), follow that document. If a required seat is unavailable, stop
and report it — never silently substitute. Otherwise one independent
reviewer is enough.

#### Severity gate

Classify every proposed change before sending it:

- **Blocker** — factually wrong, or misleads the reader. **Must fix.**
- **Material** — a reader would act differently knowing it. **Fix.**
- **Cosmetic** — more precise or better-worded, but same reader outcome.
  **Drop. Do not send.**

Line-number tweaks, synonym swaps, and "slightly more precise phrasing"
are Cosmetic by default. If you cannot name the wrong decision a nit
would cause, it is Cosmetic.

Do not report Cosmetic findings. Do not convert taste, naming, or
optional cleanup into Material.

#### Stop conditions (any one ends the exchange)

1. **All-cosmetic round** — only Cosmetic items → stop and ship. A
   reviewer reduced to line-number nits is the convergence signal.
2. **Hard cap: 2 rounds per artifact.** Round 1 = substance. Round 2 =
   verify the Round 1 fixes landed. No Round 3 unless a genuine
   **Blocker** is found.
3. **Diminishing returns** — when the remaining changes are all Cosmetic,
   stop. Edit size never gates severity: a one-line Blocker or Material
   still ships as a fix.

#### Ship-gate phrasing

The review prompt ends with this binary, not an open question:

> **Any Blocker or Material issue? If no → APPROVED.**

The reviewer answers the binary. `APPROVED` ends the phase.

#### Verify before you doubt

If you question a factual claim, check the code or source first. Do not
assert doubt from memory. If the check proves you wrong, say so and move
on; a corrected claim is a resolved issue, not a new round.

Ask **"good enough to ship?"** — not **"can it be better?"**

#### What the reviewer checks

Against the intent and the snapshot:

- acceptance criteria, including constraints the user ruled in or out
- reachable correctness, data-integrity, reliability, and security defects
- error paths, lifecycle / resource cleanup, and sibling callers of a
  claimed bug fix
- whether a new test fails on the original bug (when the change claims a
  durable fix)

Do not treat code shape or duplication alone as a defect. Do not demand
speculative redesign. Do not expand scope. Do not flag the absence of a
push, PR, or CI result this run has not reached yet.

A finding needs a falsifiable claim, a reachable path, a concrete
consequence, and an exact `path:line`. No path → drop it.

#### Finding loop

1. Reviewer returns `APPROVED` or Blocker/Material findings only.
2. You fix every Blocker and Material. Re-run only the focused check that
   proves that fix. `review.on: committed` → commit the fix on the same
   branch. `review.on: worktree` → leave the fix in the tree unless this
   run already committed the work, in which case commit it.
3. The **same** reviewer runs Round 2: verify those fixes landed. It may
   not add new scope unless it finds a genuine Blocker.
4. Product or intent challenges (the finding argues the user chose wrong)
   are not yours to dismiss. Stop and ask the user. Quote the finding.

You may dispute **severity** with a stated reason. You may not wave
through a finding you agree is Blocker or Material.

### Test

Targeted local validation of the change and the intent. Not a substitute
for remote CI when the profile delivers.

1. If the repo documents a **targeted** test command (Makefile, package
   script, `AGENTS.md`, `.make-no-mistakes.yaml` `commands.test`), run that
   first. Non-zero is a failure.
2. Then run the **smallest** additional checks that can prove the intent.
   Do not run the full suite here. Remote CI owns broad regression when
   this profile watches it.
3. UI / visual changes need reviewer-visible evidence (screenshot, rendered
   artifact) or an explicit note that it could not be captured.
4. If no targeted check can establish the intent, write or tighten one
   focused test, do a manual check with evidence, or stop and say evidence
   is not possible.

**Test-quality rule.** Never add a test whose only evidence is that it
opens, greps, or snapshots implementation source and finds a string,
token, symbol, or prompt phrase. Execute a public interface and assert
observable behavior, state, output, or failure. A prompt is not proven
because its source contains a sentence.

For a claimed regression fix: reproduce first when feasible — fail before,
pass after.

Repair the root cause, re-run only the focused check, then continue.
Product-behavior surprises: ask.

Record what you ran (commands, result, evidence paths) for closeout, and
for the PR body when this profile opens one.

### Document

Update existing docs or doc comments for gaps the diff creates. One fact,
one owner. Prefer deleting a stale duplicate or replacing it with a
pointer over synchronizing two copies. Do not create a new documentation
surface to close a perceived gap. Do not dump incident notes into
`AGENTS.md`.

If `.make-no-mistakes.yaml` `document.instructions` or a repo ownership map
exists, follow it.

Unresolved doc gaps that need a human call: ask. Otherwise apply the doc
fix (`committed` profiles: commit it) and continue.

### Lint

1. If `.make-no-mistakes.yaml` `commands.lint` / `commands.format` or the
   repo documents a lint/format command, run it.
2. Otherwise detect the project's linter/formatter from its config and
   run the scoped form (changed paths) when the tool supports it.
3. Apply safe mechanical fixes. Re-run the same command. Commit them when
   the profile commits other work.
4. Remaining Blocker/Material lint (a rule that would fail CI, or a real
   correctness/security hit): fix or ask. Style nits that would not
   change CI or a reader's decision: drop.

### Push

Only when `deliver.kind` is `pr`. Only after review, test, document, and
lint have passed.

1. Run the repo formatter (`commands.format` or detected) if one exists
   and the tree is still dirty.
2. Commit leftover agent fixes (`chore: apply gate fixes`) if anything
   remains uncommitted that belongs to this run.
3. `git ls-remote` the push target. Refuse to force-push if the remote
   has commits this branch does not contain.
4. Push the current branch. Use `--force-with-lease` only after a rebase
   you just did onto a remote you already fetched. New branches: regular
   push.
5. Push the exact SHA you validated, not an unexamined later `HEAD`.

`deliver.kind: patch`: write `git format-patch` against the merge base, do
not push, and stop.

`deliver.kind: none`: skip this phase.

### PR

Only when `deliver.kind` is `pr`.

Create or update a pull request on the host CLI (`deliver.host`, or
`gh` / `glab` / `az` when `auto`). If the host or CLI is missing, stop
after push and say so.

Title: conventional commit from the final diff and the intent
(`feat` / `fix` when user-facing). Fallback: `chore: update pull request`.

Body:

```markdown
## Intent
<verbatim intent>

## What Changed
<final branch delta after local mutating phases>

## Risk Assessment
<what could break, and why the review called it good enough>

## Testing
<commands run, results, evidence>

## Pipeline
- profile: <name>
- intent: …
- rebase: …          <!-- omit when the profile skipped it -->
- review: APPROVED | findings fixed (round N)
- test / document / lint / push: …
```

Only **What Changed** describes full branch scope. Do not wait for merge
unless `deliver.merge` says to.

### CI

Only when `deliver.kind` is `pr`.

Watch the PR checks on the latest SHA.

- Empty check list is **not** green unless `ci.empty: pass` or the repo
  explicitly declares it has no CI.
- On failure: fetch the failed logs, fix the root cause, commit, push
  with the same lease guard, re-watch.
- Merge conflict against the default branch: integrate with the profile's
  strategy, smallest correct resolution, force-with-lease, re-watch.
- Cancelled checks: rerun the same SHA once if the host can; do not
  invent a code fix for a run that never tested anything.
- If the published head is not the SHA you pushed, stop and ask.

When checks are green (or a declared no-CI repo has none):

- `deliver.merge: never` — **you are done.** Give the user the PR link and
  ask them to review and merge.
- `deliver.merge: ask` — ask.
- `deliver.merge: auto` — merge via the host CLI, then report.

List every fix the gate applied after the original commits.

## Escalate to the user

Stop and ask, quoting the finding, when:

- a review finding challenges deliberate intent or product behavior
- rebase would bundle unpublished local-default commits
- evidence for the intent cannot be produced
- push would discard remote commits you do not have
- a required review seat is unavailable
- `profile: repo` and no delivery document exists
- CI is still failing after the fix cap

Mechanical, low-risk fixes (lint, integrate conflict that does not change
behavior, test assertion that encodes existing intent) you resolve
yourself. If the user said to drive unattended, resolve those and still
stop for intent/product conflicts unless they waived those too.

## Close the loop

On success, report briefly: profile, branch, PR URL if one exists, what
was validated, what the reviewer approved, commands you ran, and each
gate-applied fix. For `local-validate`, say that nothing was published.
Do not claim CI is green unless you saw the checks on the SHA you pushed.
