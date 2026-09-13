---
title: D006 - Agents never run git; archives and decision notes make changes reversible
type: decision
status: accepted
date: 2026-09-13
tags:
  - decision
  - policy
---

# D006 — Agents never run git; archives and decision notes make changes reversible

## Context

Automatic merges need a way back. The obvious one is a git commit before every
change. But the harness lives inside the owner's project, whose git history is
theirs, and a gardener that commits on its own would leave commits nobody
asked for, in whatever state the working tree happened to be in.

## Decision

No agent runs git in a project or in the library. Reversibility comes from
`harness/agents/_archive/` and `library/archive/`, where merged, split and
retired notes are moved with the id of the decision that moved them, and from
`harness.py undo`, which puts them back. Nothing is deleted.

## Consequences

The archive folders grow. That is fine; they are small text files, and a
retired agent's memory is often exactly what a later project needs. The owner
commits when they choose to; the harness never decides that for them.

## Related

- [[D004 - Merges and splits are automatic unless the agent is high and the change is dangerous]]
