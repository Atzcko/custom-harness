---
title: D009 - Portable memory lives in the library, not in a tool's directory
type: decision
status: accepted
date: 2026-09-13
supersedes: "[[D003 - Every agent has two memories, portable and per project]]"
tags:
  - decision
  - memory
---

# D009 — Portable memory lives in the library, not in a tool's directory

## Context

D003 put each agent's portable memory in Claude Code's own per-agent memory
directory under `~/.claude/agent-memory/`. That is invisible to Codex, to
Gemini CLI, and to git. This reverses the location while keeping the two-memory
rule, which stands.

## Decision

Portable memory is `library/memory/<agent>/MEMORY.md` in the skill
repository, so it is versioned with the library and readable by any tool.
Every compiled prompt names that path and says to read it first and append at
the end. For Claude Code, `compile` links `~/.claude/agent-memory/<agent>`
to that directory, so Claude Code's automatic loading and its memory
instructions keep working against the same file. Other tools get the
instruction in the prompt and nothing else.

## Consequences

Memory changes show up as diffs in this repository, alongside the charters
they belong to. A tool without automatic memory loading depends on the agent
following the prompt, which is why the prompt says it twice. The link into
`~/.claude/agent-memory/` is per machine and is recreated by `compile`; an
existing real directory there is left alone and reported.

## Related

- [[D003 - Every agent has two memories, portable and per project]]
- [[D007 - The core is tool-neutral; each coding agent gets an adapter]]
