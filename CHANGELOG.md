# Changelog

Semantic versioning. MAJOR for a change to what the harness writes into a
project or the risk policy; MINOR for a new command, playbook, target or seed
agent; PATCH for wording and fixes. Every entry says why, not only what.

## 0.3.2 — 2026-09-13

- `doctor` now says where to get a missing dependency, not only that it is
  missing: the graphify skill and CLI (Graphify-Labs/graphify, `graphifyy`
  on PyPI), obsidian-markdown (kepano/obsidian-skills), `uv`, and Obsidian,
  with the `npx skills add` one-liners where they apply. Origins verified on
  2026-09-13. Why: a person without these skills was told to install them
  into a folder but not from where.

## 0.3.1 — 2026-09-13

- `install.sh` no longer treats a linked llm-wiki as missing. It used to
  require a real folder, so when the owner's skills repository linked llm-wiki
  into the tool folders, the harness installer replaced those links with its
  bundled copy. Now only its own bundled link counts as "not installed".

## 0.3.0 — 2026-09-13

The model registry checks itself.

- **`harness models watch`** fetches the official Anthropic, OpenAI and Google
  model pages, extracts the model ids, and compares them with
  `library/models-seen.json`. With `--write`, unchanged pages advance the
  registry's `checked` date; new ids that could change a tier are reported and
  leave the date alone; modality variants (image, audio, live, embeddings) are
  recorded without fuss. Exit codes: 0 unchanged, 3 new ids or a registry id
  missing from its page, 2 a page unreachable.
- **A weekly GitHub Actions workflow** (`.github/workflows/models-watch.yml`)
  runs it every Monday: unchanged pages become a small commit on `main`, new
  ids become a pull request carrying the report, an unreachable page fails
  the job (D011). Why: the owner asked for the check to happen periodically
  and the files to be updated without waiting for a session; the part that
  is a fact is automated, the part that is a judgment gets a pull request.
- Session start now runs `models watch` before spending a researcher on a
  refresh.

## 0.2.0 — 2026-09-13

Tool-neutral core, a model registry, preflight, and llm-wiki bundled.

- **Targets.** `compile` renders every agent for each tool it detects: Claude
  Code (`.claude/agents/*.md`), Codex (`.codex/agents/*.toml`), Gemini CLI
  (`.gemini/agents/*.md`), Cursor (`.cursor/agents/*.md`), OpenCode
  (`.opencode/agents/*.md`), plus a generic prompt and JSON sidecar under
  `harness/compiled/`. `init` writes the pointer into `CLAUDE.md`,
  `AGENTS.md` or `GEMINI.md` as appropriate, and `compile` keeps a roster
  table in the shared instruction files. Verified formats in
  `references/targets.md` (D007). Why: the owner runs Codex as well as Claude
  Code and wants the harness to survive the next tool.
- **Model registry.** Agents declare a tier; `library/models.json` maps tiers
  to the current model per provider and per tool, dated and sourced.
  `harness models show|check|set|touch`; `doctor`, `lint` and `status` report
  staleness; the refresh brief for the researcher is in
  `references/models.md` (D008). Why: a new model should reach every agent in
  every project with one change, not an edit per charter.
- **Portable memory moved into the library** at `library/memory/<agent>/`,
  linked into `~/.claude/agent-memory/` for Claude Code's automatic loading
  (D009, superseding the location in D003). Why: a directory under
  `~/.claude/` is invisible to other tools and to git.
- **Preflight.** `harness doctor` checks Python, `uv`, the graphify binary,
  Obsidian, the three skills, the launcher, targets and the registry.
  `bundled/llm-wiki/` ships with the harness and is used when no llm-wiki is
  installed (D010).
- **Launcher.** `install.sh` links the skill into `~/.agents/skills` (read by
  every tool) plus each tool's own folder, and writes `~/.local/bin/harness`,
  so playbooks and compiled prompts no longer depend on a Claude-only
  environment variable.
- Seed agents no longer pin a model; their tier resolves through the
  registry. `new` no longer requires `--model`.

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
