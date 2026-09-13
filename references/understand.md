# Phase: understand

Goal: a `harness/brief.md` that is marked ready, written from three sources: a
knowledge graph of the project, a wiki that compiles what the project's own
documents say, and an interview with the user. Nothing gets designed until the
brief is ready, because a roster designed from a guess is a roster you will
tear down next week.

## 0. Preflight

```bash
harness doctor
```

The graph needs the graphify skill, the wiki needs llm-wiki (the bundled copy
under the skill's `bundled/llm-wiki/` is used when none is installed), and the
notes follow the obsidian-markdown skill. If `doctor` reports a hard
dependency missing, stop here and tell the user what to install and where;
a half-built understanding is worse than none.

## 1. Skeleton

```bash
harness init
```

Creates `harness/` from the templates and adds a short pointer to the
instruction file of every tool it detects (`CLAUDE.md`, `AGENTS.md`,
`GEMINI.md`), so future sessions in any of them know the harness exists. It
does nothing to files that already exist. Open `harness/Harness.md`; it is the
entry note.

## 2. The graph

Use the graphify skill on the project root. If `graphify-out/graph.json`
already exists, run it with `--update`. Delegate this to the **librarian**
agent in the background if the compiled roster exists; before the first
compile, run it yourself.

What you want from it is `graphify-out/GRAPH_REPORT.md`: its communities are
the project's natural domains, and its god nodes are the files or concepts
everything depends on. Both go into the brief under "Domains".

## 3. The wiki

The harness keeps an llm-wiki at `harness/wiki/`. `init` wrote its schema
(`harness/wiki/SCHEMA.md`, with a pointer stub named for each tool's
instruction file next to it) from the template; read it, then follow the
llm-wiki skill. If the skill is not installed, read `bundled/llm-wiki/SKILL.md`
in the skill directory and its `references/`; it is the same skill. The
project's own files are the sources and are never copied; external material
the user hands over goes in `harness/wiki/raw/`.

First ingest, in this order: the graph report, the project's `README` and
instruction file if present, and any decision records or design docs the
project keeps. Stop after the first ingest. The librarian keeps the wiki
current later; the point now is to have a page per domain that the architect
can read.

## 4. The interview

This is the part only you can do. Ask in batches of three or four, never the
whole bank at once, and write each answer into `harness/brief.md` as you go
with the date. The question bank is in [interview.md](interview.md); pick the
questions the graph and wiki could not answer. Skip what is already known and
say so, because the user notices when they are asked something the README
states.

Two answers matter more than the others and must not be skipped:

- **What is done?** The definition of done for the project as a whole, and for
  a typical task. Without it every agent invents its own.
- **What must never happen automatically?** Deploys, pushes, payments, deleting
  data, contacting people. These become danger flags on the agents that could
  do them, and the risk policy depends on them.

## 5. Write the brief

Fill `harness/brief.md`: purpose, users, domains (from the graph), constraints,
definition of done, what the user delegates and what they keep, the danger
list, knowledge sources, open questions. Set `status: ready` in its
frontmatter only when the two answers above are in it.

Then tell the user, in a few lines, what you understood and what is still
open, and move to `architect`.

## When the project is brand new

An empty repository has no graph and nothing to ingest. Run the interview
first, write the brief from it, and mark the domains as "intended". The graph
and wiki steps run for real once there is something to read; the librarian
picks them up.
