---
title: Harness
type: index
project: {{project}}
skill_version: {{skill_version}}
created: {{date}}
updated: {{date}}
gardener_last_run:
librarian_last_run:
---

# Harness — {{project}}

This folder is the project's agent harness, managed by the `harness` skill
(v{{skill_version}}). Start a session with `/harness`; it reads this folder and
knows where it left off.

| Note | What it is |
|---|---|
| [[brief]] | what the project is: graph, wiki and interview |
| [[architecture]] | the roster, routing, escalation, background agents |
| `agents/` | one note per agent: charter link, project context, project memory |
| `decisions/` | H-numbered decision records, including automated merges |
| [[ledger]] | every delegated task, its outcome and cost |
| [[evolution]] | lessons for the skill itself |
| `wiki/` | the project's llm-wiki; schema in `wiki/CLAUDE.md` |

Compiled agents live in `.claude/agents/` at the project root. They are
generated; edit the notes here and run `harness.py compile`.

## Decisions

| Decision | Claim |
|---|---|
