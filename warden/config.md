# `.warden.yaml`

Optional repo file at the project root. Missing file → profile `pr-ship`.
Unknown keys are ignored. Invocation `profile=` overrides `profile:` here.

```yaml
profile: pr-ship          # pr-ship | local-validate | repo
integrate: rebase         # rebase | merge | none
default_branch: auto      # auto | main | master | <name>
review:
  when: [pre-publish]     # pre-publish | post-publish
  on: committed           # committed | worktree
  seats: auto             # auto | path to a seating document
deliver:
  kind: pr                # pr | none | patch
  host: auto              # auto | gh | glab | az | none
  merge: never            # never | ask | auto
  document: auto          # auto | path to the delivery document
commands:
  test: ...
  lint: ...
  format: ...
document:
  instructions: ...       # path to doc-ownership instructions
ci:
  empty: fail             # fail | pass
```

## Defaults by profile

| Key | `pr-ship` | `local-validate` | `repo` |
|---|---|---|---|
| phases | intent → rebase → review → test → document → lint → push → pr → ci | intent → review → test → document → lint | the delivery document |
| `integrate` | `rebase` | `none` | from the document |
| `review.when` | `[pre-publish]` | `[pre-publish]` | from the document |
| `review.on` | `committed` | `worktree` if dirty, else `committed` | from the document |
| `deliver.kind` | `pr` | `none` | from the document |
| `deliver.document` | n/a | n/a | the path named here, else `AGENTS.md` |
| `deliver.merge` | `never` | n/a | from the document |
| `ci.empty` | `fail` | n/a | from the document |

`profile: repo` with no seating or delivery document → stop. Do not invent
a pipeline.

`review.seats: auto` → one `reviewer` agent, unless the repo already
documents seating.

`deliver.host: none` or a missing CLI with `deliver.kind: pr` → stop after
push.

`default_branch: auto` → remote `HEAD`, else `origin/main`, else
`origin/master`.
