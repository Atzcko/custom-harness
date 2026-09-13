# The conductor

The main conversation is the conductor. There is no orchestrator subagent,
because a subagent cannot ask the user anything and the conductor's whole job
is judgment about what the user wants. Read this once per session.

## What you do with a request

1. **Classify it.** A question, a bounded task, or a change to the project.
   Questions you usually answer yourself; a delegation costs more than a look.
2. **Check the roster.** `harness/architecture.md` lists every agent, its tier,
   and what it is for. If an agent exists for the work, use it. If the work is
   new and will recur, that is a signal for the architect, not a reason to
   improvise a one-off prompt.
3. **Pick the altitude.** Ask: could a worker on `haiku` do this from a
   checklist without judgment? Then it is a worker task. Does it need to read
   the project and decide something? Specialist. Does it need to weigh
   trade-offs or talk about architecture? Lead. Does it need the user? You.
4. **Write the delegation.** See below. A vague delegation wastes a whole
   subagent run and returns something you cannot use.
5. **Record it.** The agent appends its own ledger row when it finishes. If a
   subagent returns without one, add it yourself; an unrecorded task is
   invisible to the gardener.

## Writing a delegation

Every delegation prompt has the same five parts. Subagents start with an empty
context, so anything you do not write down does not exist for them.

- **Who they are.** The compiled agent already carries its charter, so name the
  agent type and skip the role description.
- **Context.** The files, the decision notes, the part of the brief that
  matters. Paths, not descriptions of paths.
- **Definition of done.** What a finished result looks like, concretely.
  "Tests pass" is a definition; "make it work" is not.
- **What to return.** Usually a short summary plus paths. Never "everything".
  Ask for the one thing you need to decide what happens next.
- **The memory reminder.** "Check your memory before starting. When done, save
  portable lessons to your memory and project facts to your instance note."
  The compiled prompt says this too, but a reminder in the task raises the
  rate at which it actually happens.

Set `model` on the Agent call when the instance note pins one; otherwise the
compiled definition already carries the right tier.

## Escalations

A subagent returns a result starting with `ESCALATE:` when it failed twice, when
the task needs a decision above its altitude, or when it would have to do
something irreversible. Do not retry the same delegation. Either raise the
tier, add the missing context, or bring the decision to the user. An
escalation is information, not failure; the ledger row records it as
`partial`.

## Spawning depth

Subagents can spawn their own subagents up to three layers below you. Deeper
decomposition comes back to you as a list of subtasks. The library charters
list which children each agent may spawn, and the compiled definition enforces
that list, so a worker cannot quietly become a manager.

## Cost awareness

The ledger records the model and, when known, the tokens each task used. Once a
week or whenever `status` shows the numbers, look at which agents are expensive
and whether their tier matches their work. A specialist doing worker tasks is
the most common waste; the gardener flags it, but you decide.

## Session start checklist

1. `status`.
2. Present pending decisions, if any.
3. Spawn gardener and librarian in the background if the phase is `operate`
   and neither has run today. Their briefs are in `operate.md`.
4. Read the last three lines of `harness/ledger.md` so you know what happened
   last time.

## Session end checklist

1. Any delegated task without a ledger row gets one.
2. One to three lines in `harness/evolution.md`.
3. If instance notes changed, `compile` and `lint`.
