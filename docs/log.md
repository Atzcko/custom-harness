---
title: Log
type: log
---

# Log

Append-only, newest at the bottom. What happened; the decisions say why.

## 2026-09-13 — v0.1.0, the first build

- Repository created on GitHub as `Atzcko/Custom-Harness-Design` and cloned
  into the iCloud Projects vault.
- Design agreed with the owner: five phases (understand, architect, operate,
  optimize, evolve), four model tiers, two memories per agent, a shared agent
  library with reuse-adapt-create matching, automatic merges under a risk
  policy, and a skill that evolves from its own lessons.
- Verified against the Claude Code docs before building: the `memory` field
  on agents (`user` / `project` / `local`), model aliases including `fable`,
  the `skills` preload, `Agent(a, b)` spawn allowlists, three levels of
  nesting, and that skills cannot bundle agents.
- Written: `SKILL.md`, ten playbooks and references, nine templates, ten seed
  library agents, `scripts/harness.py` with seventeen commands, evals,
  installer, and decisions D001 to D006.
- Tested on a fixture project in a scratch directory: init, status, match,
  new, compile, ledger, overlap, risk, an automatic merge and its undo, a
  merge that the policy sent to the user, an approved merge, split, retire,
  promote, lessons collect and lint all behaved. Fixture data that leaked into
  the library's track-record fields was reset afterwards.
- Pilot project: Desktop gadget, to be started with `/harness` in a session
  rooted there.
