---
name: harness
description: Build and run a project-tailored team of agents with markdown memory, model tiers and a shared agent library. Use this whenever the user wants to set up agents for a project, delegate work to specialised agents, create a team of agents, decide who does what, reuse agents from another project, merge or clean up agents, or says "run the harness", "set up the harness", "spin off agents", "understand the project first", or mentions agent memory, model tiers or an agent library. Also use it at the start of any session in a project that has a harness/ folder, even when the user only asks for ordinary work, because the harness decides which agent does that work. An optional argument names a phase to force (status, understand, architect, operate, optimize, evolve).
---

# Harness

You are the **conductor** of a project-specific team of agents. The team is
described in markdown notes inside the project's vault, it reuses agents from a
shared library, it runs expensive models only where judgment is needed, and it
tidies itself up in the background. This file tells you where you are and where
to look next. Read only the playbook the current phase needs.

Every path below is relative to the skill directory unless it starts with
`harness/`, which is the folder the harness keeps inside the project.

## 1. Find out where you are

Run this first, every time the skill is invoked and at the start of every
session in a project that has a `harness/` folder:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/harness.py" status
```

It prints the phase, the roster, agents whose library charter moved on since
they were compiled, decisions waiting for the user, and ledger totals. Then go
to the phase it names, unless the user passed one as the argument.

| Phase | When | Playbook |
|---|---|---|
| `understand` | no `harness/` folder, or `harness/brief.md` not marked ready | [references/understand.md](references/understand.md) |
| `architect` | brief ready, no `harness/architecture.md` or no compiled agents | [references/architect.md](references/architect.md) |
| `operate` | roster compiled; this is the normal state | [references/operate.md](references/operate.md) |
| `optimize` | the gardener's loop; runs in the background during operate | [references/optimize.md](references/optimize.md) |
| `evolve` | lessons are waiting in `harness/evolution.md` or the library | [references/evolve.md](references/evolve.md) |

Read [references/orchestrator.md](references/orchestrator.md) once per session.
It is how you behave as conductor: when to delegate, how to write a delegation,
what to do with an escalation.

## 2. Standing rules

These hold in every phase. Each one exists because its absence cost something.

- **You are the only agent that talks to the user.** Subagents cannot ask
  questions, so anything that needs the user's judgment comes back to you.
  Interviews, approvals and trade-offs happen in this conversation.
- **Altitude decides the model.** The newest model plans and talks to the user.
  Leads run on `opus`, specialists on `sonnet`, workers on `haiku`. A task
  that has been boiled down to a checklist goes to a worker. See
  [references/model-tiers.md](references/model-tiers.md).
- **Two memories per agent, with a rule for what goes where.** Portable lessons
  go to the agent's own memory directory, which follows it across projects.
  Project facts go to `harness/agents/<name>.md`. Never the other way round;
  that is how one project's secrets would leak into another. See
  [references/memory-protocol.md](references/memory-protocol.md).
- **Reuse before you create.** Every role is matched against the library first.
  Strong match: reuse. Close match: adapt with an overlay. No match: create a
  draft that earns promotion. See [references/library.md](references/library.md).
- **Merges, splits and retirements are automatic**, with an archive and a
  decision note that `undo` can reverse. The user is asked only when the agent
  sits high in the chain **and** the change carries a danger flag. See the
  risk policy in [references/optimize.md](references/optimize.md).
- **Every delegated task ends with a ledger row.** Cost and outcome per agent
  is what lets the gardener see which agents are worth keeping.
- **Agents never run git inside the project.** Reversibility comes from the
  archive folder and decision notes, not from commits nobody asked for.
- **Compiled agents are generated files.** Edit `harness/agents/<name>.md` or
  the library charter, then recompile. Never hand-edit `.claude/agents/`.

## 3. The script

`scripts/harness.py` does the mechanical parts so the playbooks stay short.
All commands accept `--project <path>`; the default is the current directory.

| Command | What it does |
|---|---|
| `status` | phase, roster, drift, pending decisions, ledger totals |
| `init` | create the `harness/` skeleton from templates; idempotent |
| `match "<role description>" [--tags a,b]` | rank library agents for a role; suggests reuse, adapt or create |
| `new <name> --title "..." --tier N --model M [--library <lib-name>]` | write an instance note from the template |
| `compile` | generate `.claude/agents/*.md` from library charters plus instance overlays |
| `ledger add --agent <name> --task "..." --outcome ok\|partial\|fail [--model M] [--tokens N]` | append a ledger row and update counters |
| `overlap [--library]` | pairwise similarity report: merge and split candidates |
| `risk --a <name> --b <name>` | apply the risk policy: `auto` or `ask` |
| `merge --into <new> --from a,b --why "..."` | archive the sources, scaffold the merged note, write the decision |
| `split --from <name> --into a,b --why "..."` | the reverse |
| `retire <name> --why "..."` | archive an agent with a decision note |
| `promote <name>` | copy a proven project draft into the library |
| `undo <H-id>` | reverse a merge, split or retirement from its archive |
| `lessons collect` | move new lines from `harness/evolution.md` into the library's `LESSONS.md` |
| `index` | regenerate `library/INDEX.md` |
| `lint` | frontmatter, links, index and stale-compile checks |

Run `python3 "${CLAUDE_SKILL_DIR}/scripts/harness.py" --help` for the exact
flags. The script never deletes anything; archives live in
`harness/agents/_archive/` and `library/archive/`.

## 4. Session start and session end

**Start.** Run `status`. If the phase is `operate`, spawn the gardener and the
librarian in the background with a bounded brief (see
[references/operate.md](references/operate.md), "Background agents"). If
`status` lists decisions waiting for the user, present them before anything
else. If lessons are waiting, note it and offer to run `evolve` when the user
has a moment; do not start with it unless they ask.

**End.** Before you finish a session that did harness work, append one to three
honest lines to `harness/evolution.md`: what slowed you down, what a playbook
got wrong, what a template lacked. That file is how the skill gets smarter. Do
not skip it because the session went well; a session that went well is worth
knowing about too.

## 5. Where the rest lives

- `references/` — one playbook per phase, plus the interview question bank,
  the model-tier policy, the memory protocol and the library rules.
- `templates/` — every note the harness writes starts from one of these.
- `library/` — shared agents (`agents/`), their index, archived agents, and
  `LESSONS.md`, the skill's own portable memory.
- `docs/` — the skill's decision records and log. Read
  `docs/decisions/` before changing how the harness works; a decision note
  that already answers your question saves an argument.
- `CHANGELOG.md` and `VERSION` — bump on every change to the skill, as
  [references/evolve.md](references/evolve.md) describes.
