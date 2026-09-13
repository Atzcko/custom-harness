---
title: Custom Harness Design
type: index
updated: 2026-09-13
---

# Custom Harness Design

The `harness` skill: a project-tailored team of agents with markdown memory,
model tiers, a shared library and a gardener, for Claude Code, Codex, Gemini
CLI, Cursor and OpenCode. This vault is the skill's home. `README.md` is the
same story for GitHub; `SKILL.md` is what the model reads.

## Decisions

| Decision | Claim |
|---|---|
| [[D001 - The skill and the agent library share one repository]] | reuse anywhere the skill is installed, every charter change is a diff |
| [[D002 - Agents are compiled into the project, never bundled with the skill]] | skills cannot ship agents, and a project should only see the agents it chose |
| [[D003 - Every agent has two memories, portable and per project]] | superseded by D009 for the location; the two-memory rule stands |
| [[D004 - Merges and splits are automatic unless the agent is high and the change is dangerous]] | automation by default; the owner only for altitude plus danger |
| [[D005 - The main session is the conductor, there is no orchestrator subagent]] | subagents cannot ask the user, so the conversation conducts |
| [[D006 - Agents never run git; archives and decision notes make changes reversible]] | undo comes from archives, not from commits nobody asked for |
| [[D007 - The core is tool-neutral; each coding agent gets an adapter]] | notes and script are shared; only the last mile is per tool |
| [[D008 - A dated model registry decides which model each tier runs]] | one registry change moves every agent to a newer model |
| [[D009 - Portable memory lives in the library, not in a tool's directory]] | memory travels with the charter and is visible to every tool |
| [[D010 - llm-wiki ships inside the harness; graphify and obsidian-markdown are checked for]] | doctor before anything; the owner's own skill travels with the harness |

## Log

[[log]] — what happened, newest at the bottom.

## Library

- `library/INDEX.md` — generated catalogue of the shared agents and the
  tier-to-model table.
- `library/models.json` — the model registry, dated and sourced.
- `library/memory/` — one folder per agent, the portable memories.
- `library/LESSONS.md` — the skill's own portable memory.
