# Changelog

Semantic versioning. MAJOR for a change to what the harness writes into a
project or the risk policy; MINOR for a new command, playbook or seed agent;
PATCH for wording and fixes. Every entry says why, not only what.

## 0.1.0 — 2026-09-13

First build. The skill, five phase playbooks, the interview bank, the
model-tier policy, the memory protocol, the library rules, nine templates,
ten seed agents, and `scripts/harness.py`.

Why it is shaped this way:

- Agents are markdown notes with two memories so they can be read in Obsidian
  and still travel between projects (D003).
- The library lives in this repository so reuse works anywhere the skill is
  installed and every charter change has a diff (D001).
- Merges, splits and retirements are automatic under a risk policy because the
  owner asked for automation with the user involved only for high-altitude,
  dangerous changes (D004).
- Nothing is deleted and no agent runs git; archives and decision notes make
  every automated change reversible with `undo` (D006).
