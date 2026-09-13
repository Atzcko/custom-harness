---
title: Custom Harness Design
type: index
updated: 2026-09-13
---

# Custom Harness Design

The `harness` skill: a project-tailored team of agents with markdown memory,
model tiers, a shared library and a gardener. This vault is the skill's home.
`README.md` is the same story for GitHub; `SKILL.md` is what the model reads.

## Decisions

| Decision | Claim |
|---|---|
| [[D001 - The skill and the agent library share one repository]] | reuse anywhere the skill is installed, every charter change is a diff |
| [[D002 - Agents are compiled into the project, never bundled with the skill]] | skills cannot ship agents, and a project should only see the agents it chose |
| [[D003 - Every agent has two memories, portable and per project]] | portable lessons travel, project facts stay, secrets go nowhere |
| [[D004 - Merges and splits are automatic unless the agent is high and the change is dangerous]] | automation by default; the owner only for altitude plus danger |
| [[D005 - The main session is the conductor, there is no orchestrator subagent]] | subagents cannot ask the user, so the conversation conducts |
| [[D006 - Agents never run git; archives and decision notes make changes reversible]] | undo comes from archives, not from commits nobody asked for |

## Log

[[log]] — what happened, newest at the bottom.

## Library

`library/INDEX.md` — generated catalogue of the shared agents.
`library/LESSONS.md` — the skill's own portable memory.
