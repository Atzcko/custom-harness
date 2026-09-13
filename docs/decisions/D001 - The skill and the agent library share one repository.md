---
title: D001 - The skill and the agent library share one repository
type: decision
status: accepted
date: 2026-09-13
tags:
  - decision
  - architecture
---

# D001 — The skill and the agent library share one repository

## Context

Agents must be reusable across sessions and across projects. That needs a
home outside any single project. Two candidates: a separate directory under
`~/.claude/` that only exists on this machine, or a folder inside the skill's
own repository.

## Decision

The library lives at `library/` inside this repository, next to the skill. The
repository is installed by symlinking it to `~/.claude/skills/harness`, so
the library is available wherever the skill is, and every change to a charter
is a commit with a diff.

## Consequences

Track-record fields (`used_in`, `tasks`, `successes`, `last_used`) change
when projects use agents, which makes the library churn in git. That is
accepted: the history of which agent did how much work is worth having. Test
runs against fixture projects must not touch the real library; the working
agreements in `CLAUDE.md` say how.

## Related

- [[D002 - Agents are compiled into the project, never bundled with the skill]]
