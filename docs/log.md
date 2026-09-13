---
title: Log
type: log
---

# Log

Append-only, newest at the bottom. What happened; the decisions say why.

## 2026-09-13 — v0.1.0, the first build

- Repository created on GitHub as `Atzcko/custom-harness` and cloned
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

## 2026-09-13 — v0.2.0, tool-neutral, model registry, preflight

- The owner added three requirements after the first build: the skill must
  work in Codex, Gemini or any other coding agent, not only Claude Code; it
  must know the latest models and keep moving agents onto them; and it must
  check for its dependencies before use, with llm-wiki (the owner's own
  skill) bundled in.
- A researcher agent verified the current facts from the tools' own docs:
  Codex custom agents are TOML under `.codex/agents/`, Gemini CLI subagents
  are markdown under `.gemini/agents/` and cannot nest, Cursor and OpenCode
  have their own markdown forms, and all five tools read skills from
  `~/.agents/skills`. Model pages gave the lineups; the local Codex model
  cache confirmed the OpenAI ids. Recorded in `references/targets.md` and
  `library/models.json`.
- Rewrote `scripts/harness.py` around targets and the registry: `compile`
  renders per tool plus a generic prompt, `doctor` and `models` are new,
  portable memory moved to `library/memory/` with a link for Claude Code.
  `HARNESS_LIBRARY` and `HARNESS_HOME` let tests use scratch copies after a
  fixture run leaked memory folders and links into the real library.
- Decisions D007 to D010; D003 superseded by D009 for the memory location.
- Doctor found that the two installed llm-wiki copies (`~/.agents/skills`
  and `~/.claude/skills`) differ; the bundled copy follows the newer one.

## 2026-09-13 — v0.3.0, the registry checks itself

- The owner asked for the model check to run periodically and update the
  files, and for the work to arrive as a pull request.
- Probed the official model pages: the Anthropic and OpenAI docs serve a
  markdown twin at `.md`, Google's page carries the ids in its HTML. All
  three are readable by a plain script, so `harness models watch` needs no
  dependencies.
- Added `models watch`, the snapshot `library/models-seen.json`, and the
  weekly workflow; decision D011 separates the fact (pages unchanged) from
  the judgment (tier mapping), which is why unchanged pages commit and new
  ids open a pull request.
- Pushed `main` at v0.1.0 as the base and opened a pull request carrying
  v0.2.0 and v0.3.0.
