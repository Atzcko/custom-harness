# Phase: operate

This is the normal state. Work arrives, you route it, agents do it, the ledger
records it, memory accumulates. Read `orchestrator.md` for how to delegate;
this file covers what is specific to the running harness.

## Routing

`harness/architecture.md` has the routing table. When a request does not fit a
row, do not stretch an agent to cover it. Do it yourself this once, and note
the gap in `harness/evolution.md` so the architect can decide whether the
roster needs a new role.

## The task lifecycle

1. Delegate with the five-part prompt.
2. The agent reads its instance note, checks its memory, does the work.
3. The agent appends a ledger row and saves memory. If it did not, you do:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/harness.py" ledger add --agent tester --task "run pio test after ui.cpp change" --outcome ok --model haiku
```

4. You read the result, decide what happens next, and only then report to the
   user. The user sees outcomes, not the relay.

## Background agents

Spawn both at session start when the phase is `operate`, in the background,
and forget about them until they report. Bound them so they cannot run away:

**Gardener** (library agent `gardener`, `sonnet`):

> Run the optimize loop once for this project: `overlap`, then `risk` for each
> candidate pair, then apply what the policy marks `auto` and write a
> proposal note for what it marks `ask`. Promote drafts that qualify. Retire
> what qualifies. Report a list of decisions written, nothing else. Stop after
> one pass.

**Librarian** (library agent `librarian`, `sonnet`):

> Bring the knowledge up to date: run graphify with `--update` on the project
> root, then lint the wiki at `harness/wiki/` and ingest anything new in
> `harness/wiki/raw/`. Report what changed in one paragraph.

Both run at most once per session. `status` shows when they last ran; skip
them when it was today, unless the user asks.

When either reports a decision that needs the user, present it in this
conversation with the two or three sentences from the decision note: what
would change, why, and what it would cost to undo.

## Drift

`status` lists agents whose library charter has a newer version than the one
they were compiled from. Recompile at the next quiet moment:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/harness.py" compile
```

Project memory in the instance note survives a recompile; only the charter
part is refreshed.

## When an agent keeps failing

Two failures on the same task is an escalation; the agent stops on its own.
Three escalations from the same agent across tasks is a roster problem: either
its tier is too low, its charter is wrong, or the task type does not belong to
it. Write it in `harness/evolution.md` and, if the pattern is clear, raise the
tier in the instance note and recompile. The gardener reads the ledger and
will flag it as well, but you will notice first.
