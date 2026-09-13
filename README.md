# Harness

A Claude Code skill that turns any project into a staffed team of agents.

Invoked inside a project, it learns the project first: a knowledge graph
(graphify), a compiled wiki (llm-wiki), and an interview with you. Then it
designs the agents the project needs and writes each one as a markdown note in
the project's Obsidian vault, where the note is both the agent's charter and
its memory. Work flows down a hierarchy with the newest model only at the
top and cheaper models doing the boiled-down tasks. A gardener runs alongside,
merging overlapping agents into stronger specialists. Agents that prove
themselves are promoted to a shared library and reused in the next project.
And the skill studies its own performance so it gets better with every
session.

This repository is the skill's home: the skill, its playbooks, the agent
library, and the skill's own decision records.

## Install

```bash
./install.sh
```

It symlinks this folder to `~/.claude/skills/harness` and lints the library.
Then start a new Claude Code session in any project and type `/harness`.

Requirements: Claude Code with custom agents and skills, Python 3, and the
`graphify`, `llm-wiki` and `obsidian-markdown` skills for the understand
phase.

## Use

1. Open a session in a project. Type `/harness`.
2. It runs `status`, sees there is no harness yet, and starts the
   **understand** phase: builds the graph, seeds the wiki, and interviews you
   in small batches. The answers become `harness/brief.md`.
3. **Architect**: it derives the roster from the brief and the graph, matches
   every role against the library, writes one note per agent, compiles them
   into `.claude/agents/`, and shows you the roster.
4. **Operate**: from then on, work you bring is routed to agents. Every task
   ends with a ledger row. Agents append what they learned to their notes.
5. In the background, the **gardener** merges, splits, retires and promotes
   agents automatically, asking you only when an agent is high in the chain
   and the change carries a danger flag. The **librarian** keeps the graph and
   wiki current.
6. At the end of a session the skill writes one to three lessons to
   `harness/evolution.md`. The **evolve** phase turns them into playbook
   improvements and a version bump.

Read [SKILL.md](SKILL.md) for the full picture and the command table.

## How it decides

| Question | Answer |
|---|---|
| Which model runs an agent? | By altitude: the conductor on the newest model, leads on `opus`, specialists on `sonnet`, workers on `haiku`. See [references/model-tiers.md](references/model-tiers.md). |
| Where does an agent's memory live? | Portable lessons in Claude Code's per-agent memory directory, which follows the agent across projects; project facts in the instance note in the vault. See [references/memory-protocol.md](references/memory-protocol.md). |
| Reuse or create? | Every role is matched against the library: strong match reuse, close match adapt with an overlay, no match create a draft. See [references/library.md](references/library.md). |
| Who approves a merge? | Nobody, unless the agent is tier 0 or 1 **and** carries a danger signal. Then you. Every automatic change is archived, recorded as a decision, and reversible with `undo`. See [references/optimize.md](references/optimize.md). |

## Layout

```
SKILL.md              the skill: phase router and standing rules
references/           one playbook per phase, plus interview, tiers, memory, library
templates/            every note the harness writes starts here
library/agents/       shared agents; INDEX.md is generated; LESSONS.md is the skill's memory
scripts/harness.py    the mechanical half: status, init, match, compile, ledger, overlap,
                      risk, merge, split, retire, undo, promote, lessons, index, lint
evals/                test prompts for the skill-creator benchmark
docs/decisions/       why the harness is shaped this way (D001...)
docs/log.md           what happened, newest at the bottom
```

Inside a project the harness keeps a `harness/` folder: `Harness.md` (entry),
`brief.md`, `architecture.md`, `agents/`, `decisions/`, `ledger.md`,
`evolution.md` and `wiki/`. Compiled agents go to `.claude/agents/`.

## Versioning

`VERSION` and [CHANGELOG.md](CHANGELOG.md). The evolve phase bumps them; see
[references/evolve.md](references/evolve.md) for which changes are automatic
and which are proposed to you first.
