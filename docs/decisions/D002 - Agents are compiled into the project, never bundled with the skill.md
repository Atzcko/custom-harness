---
title: D002 - Agents are compiled into the project, never bundled with the skill
type: decision
status: accepted
date: 2026-09-13
tags:
  - decision
  - architecture
---

# D002 — Agents are compiled into the project, never bundled with the skill

## Context

Claude Code loads custom agents from `.claude/agents/` in the project or
`~/.claude/agents/` for the user. A skill cannot ship agents of its own; the
documentation says so directly. Putting every library agent in
`~/.claude/agents/` would also expose all of them in every project, matched or
not.

## Decision

The canonical agent definition is a markdown note: the charter in the library,
the project overlay in `harness/agents/<name>.md`. `harness.py compile`
generates `.claude/agents/<name>.md` from the two, with the memory scope, the
tool allowlist, the spawn allowlist and the harness rules filled in. Generated
files carry a marker and are never edited by hand.

## Consequences

A project only sees the agents its architect chose. Changing a charter in the
library requires a recompile in every project that reuses it, which `status`
reports as drift. The compiled prompt is long because it carries the charter
and the working rules; that is the price of an agent that behaves the same
in every project.

## Related

- [[D001 - The skill and the agent library share one repository]]
- [[D003 - Every agent has two memories, portable and per project]]
