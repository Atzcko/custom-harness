---
title: D003 - Every agent has two memories, portable and per project
type: decision
status: superseded
superseded_by: "[[D009 - Portable memory lives in the library, not in a tool's directory]]"
date: 2026-09-13
tags:
  - decision
  - memory
---

> [!note] Superseded on 2026-09-13 by [[D009 - Portable memory lives in the library, not in a tool's directory]].
> The two-memory rule below still holds; only the location of the portable
> memory changed, because a directory under `~/.claude/` is invisible to other
> tools and to git.

# D003 — Every agent has two memories, portable and per project

## Context

The owner wants agents that remember, and agents that move between projects.
One memory cannot serve both: a memory that follows the agent everywhere will
carry one project's paths, people and secrets into the next.

## Decision

Two memories, both markdown. Portable lessons go to Claude Code's per-agent
memory directory (`memory: user` in the compiled definition, so it follows the
agent across projects; `memory: project` for local drafts until they are
promoted). Project facts go to the "Project memory" section of the instance
note in the project's vault. The compiled prompt states the rule and the test
for it: would this line be true and useful in a different project?

## Consequences

Agents must be told the rule every time; the compiled prompt does that.
Promotion copies the charter and never the project memory. The vault shows
project memory to the owner in Obsidian, which is the point; the portable
memory is only visible under `~/.claude/agent-memory/`.

## Related

- [[D002 - Agents are compiled into the project, never bundled with the skill]]
