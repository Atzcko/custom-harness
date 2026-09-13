---
title: D005 - The main session is the conductor, there is no orchestrator subagent
type: decision
status: accepted
date: 2026-09-13
tags:
  - decision
  - architecture
---

# D005 — The main session is the conductor, there is no orchestrator subagent

## Context

The original sketch had an orchestrator agent at the top of the tree. In
Claude Code a subagent cannot ask the user anything: the question tool is
withheld from every subagent. The interview, approvals and trade-offs are the
orchestrator's whole job.

## Decision

The main conversation, running the skill, is the conductor. Its behaviour is
written in `references/orchestrator.md`, which is read once per session. The
architect, gardener and librarian are subagents; the conductor is not.

## Consequences

Anything that needs the user comes back up to the conversation as an
`ESCALATE:` result. Long autonomous runs are possible by delegating to a lead
agent, which can spawn three levels below the conversation, but a lead cannot
interview the owner; that limit is by design.

## Related

- [[D002 - Agents are compiled into the project, never bundled with the skill]]
