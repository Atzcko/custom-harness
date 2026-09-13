# Phase: operate

This is the normal state. Work arrives, you route it, agents do it, the ledger
records it, memory accumulates. Read `orchestrator.md` for how to delegate;
this file covers what is specific to the running harness.

## Session start

```bash
harness doctor
harness models check
harness status
```

If `models check` says the registry is stale, refresh it before delegating
anything that matters: send the **researcher** the brief in
[models.md](models.md), apply its findings with `harness models set`, then
`harness models touch` and `harness compile`. A stale registry means every
agent is running on whatever was newest a month ago.

`status` shows drift too: agents whose library charter has a newer version
than the one they were compiled from. Recompile at the next quiet moment.
Project memory in the instance note survives a recompile; only the charter
part is refreshed.

## Routing

`harness/architecture.md` has the routing table. When a request does not fit a
row, do not stretch an agent to cover it. Do it yourself this once, and note
the gap in `harness/evolution.md` so the architect can decide whether the
roster needs a new role.

## The task lifecycle

1. Delegate with the five-part prompt, using your tool's subagent mechanism
   and the agent's compiled name (see [targets.md](targets.md) for how each
   tool calls a subagent).
2. The agent reads its instance note, checks its memory, does the work.
3. The agent appends a ledger row and saves memory. If it did not, you do:

```bash
harness ledger add --agent tester --task "run pio test after ui.cpp change" --outcome ok --model haiku
```

4. You read the result, decide what happens next, and only then report to the
   user. The user sees outcomes, not the relay.

## Background agents

Run both at session start when the phase is `operate`, in the background
where your tool supports it, and forget about them until they report. Bound
them so they cannot run away. Record each run with `harness ran gardener` or
`harness ran librarian`; `status` shows when they last ran, so skip them when
it was today unless the user asks.

**Gardener** (library agent `gardener`, tier 2):

> Run the optimize loop once for this project: `overlap`, then `risk` for each
> candidate pair, then apply what the policy marks `auto` and write a
> proposal note for what it marks `ask`. Promote drafts that qualify. Retire
> what qualifies. Report a list of decisions written, nothing else. Stop after
> one pass.

**Librarian** (library agent `librarian`, tier 2):

> Bring the knowledge up to date: run graphify with `--update` on the project
> root, then lint the wiki at `harness/wiki/` and ingest anything new in
> `harness/wiki/raw/`. Report what changed in one paragraph.

When either reports a decision that needs the user, present it in this
conversation with the two or three sentences from the decision note: what
would change, why, and what it would cost to undo.

## When an agent keeps failing

Two failures on the same task is an escalation; the agent stops on its own.
Three escalations from the same agent across tasks is a roster problem: either
its tier is too low, its charter is wrong, or the task type does not belong to
it. Write it in `harness/evolution.md` and, if the pattern is clear, raise the
tier in the instance note and recompile. The gardener reads the ledger and
will flag it as well, but you will notice first.
