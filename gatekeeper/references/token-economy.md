# Token use

The six-run v2 test measured output costs 1.6 to 3.9 times the baseline.
Long single-context runs also consumed large cached inputs. These rules keep
gate enforcement small and isolate leaf context.

## Keep enforcement small

- **Use command checks.** A CHECK command replaces repeated model review with
  a repeatable subprocess.
- **Keep the stop hook local.** It scans gate files without a model call.
- **Limit evidence.** Record only the lines that decide the gate. Keep each
  gates file short enough to review directly.

## Limit leaf context

- **Send narrow briefs.** Give a leaf the contract and its gates file. Do not
  send the driver's transcript, sibling output, or all of PLAN.md.
- **Append status.** Keep the PLAN.md status log append-only. Avoid rewriting
  stable content that the runtime may cache.
- **Load details when needed.** Keep the main skill short and read reference
  files only for the active mode.

## Control orchestration cost

- **Match models to work.** Use a cheaper model for mechanical leaves. Use
  the strongest available model for design, integration, the driver, and
  parent verification.
- **Keep small tasks solo.** Subagent setup costs more than it saves for work
  under about half an hour.
- **Choose depth from deliverables.** Do not use depth as a request for more
  effort. Choose leaves by the rule in method.md, then let their gates define
  completion.
- **Keep verification.** Reduce narration, recap, and copied logs before
  removing a check.
