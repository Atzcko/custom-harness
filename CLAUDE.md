# Custom Harness Design — the `harness` skill

This repository is an agent skill and an Obsidian vault. `SKILL.md` at the
root is the skill; it is installed by linking this folder into the skills
folders every tool reads (`./install.sh`). It works in Claude Code, Codex,
Gemini CLI, Cursor and OpenCode; see `references/targets.md`. Start at
[[index]].

## Working agreements

1. **Read `docs/decisions/` before changing how the harness works.** Ten
   decisions exist so the same ground is not re-litigated. Disagree by writing
   a new decision that supersedes the old one, never by editing it.
2. **Every change to the skill bumps `VERSION` and gets a `CHANGELOG.md` entry
   that says why.** PATCH for wording and fixes, MINOR for a new command,
   playbook, target or seed agent, MAJOR for a change to what the harness
   writes into a project or to the risk policy.
3. **Append to `docs/log.md` at the end of any session that changes the
   repository.** Newest at the bottom.
4. **Test on a fixture with a scratch library, never on the real one.** The
   script updates the library (track-record fields, `memory/`, promoted
   agents, `LESSONS.md`) and links `~/.claude/agent-memory/` into it. Point
   tests elsewhere:

   ```bash
   cp -R library /tmp/harness-lib && HARNESS_LIBRARY=/tmp/harness-lib HARNESS_HOME=/tmp/harness-home python3 scripts/harness.py --project /tmp/fixture doctor
   ```

   If a test did touch the real library: reset `used_in`, `tasks`,
   `successes`, `last_used` on the seed agents, remove promoted fixture agents
   and fixture folders under `library/memory/`, drop fixture lines from
   `library/LESSONS.md`, remove fixture links from `~/.claude/agent-memory/`,
   and run `python3 scripts/harness.py index`.
5. **Before a commit:** `python3 scripts/harness.py lint` (in this directory it
   lints the library and the registry) and the skill-creator validator:

   ```bash
   uv run --with pyyaml python "$HOME/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py" .
   ```

   (The validator needs PyYAML, which the system Python does not have; `uv`
   supplies it without installing anything globally.)
6. **Generated files are generated.** `library/INDEX.md` comes from
   `harness index`; compiled agents come from `harness compile`. Edit the
   source note, then regenerate.
7. **Keep `library/models.json` honest.** Change a tier's model only with
   `harness models set --source <url>` so the history records where the id
   came from; the researcher's refresh brief is in `references/models.md`.
8. **Keep `bundled/llm-wiki/` and `bundled/obsidian-markdown/` in step with
   the owner's copies in the skills repository.** `harness doctor` reports
   when they differ and which is newer; sync in the direction the owner
   wants, never silently. graphify is never bundled (D012).

## Conventions

- Notes under `docs/` use wikilinks and follow the obsidian-markdown skill:
  a `type:` property on every note, decision titles that state the
  conclusion, absolute dates.
- `references/` and `templates/` are read by the model at run time, in any
  of the supported tools. Write them for a reader with no context and no
  Claude-specific vocabulary: explain why, avoid shouting, keep each file to
  what one phase needs. Invoke the script as `harness`.
- Library charters are written in the second person, never pin a model
  unless the agent needs one, and must make sense in a project other than
  the one that produced them.
- The script is standard library only, so it runs on any Python 3 without a
  virtual environment.

## Layout

| Path | What |
|---|---|
| `SKILL.md` | entry point and phase router |
| `references/` | playbooks: orchestrator, understand, architect, operate, optimize, evolve, interview, model-tiers, models, memory-protocol, library, targets |
| `templates/` | agent, instance, brief, architecture, decision, ledger, evolution, harness-index, wiki-schema |
| `library/` | `agents/`, `memory/`, `archive/`, `decisions/` (L-numbered), `models.json`, `models-seen.json` (snapshot kept by `models watch`), `INDEX.md`, `LESSONS.md` |
| `.github/workflows/models-watch.yml` | the weekly model-page check; unchanged pages commit a date bump, new ids open a pull request |
| `bundled/` | llm-wiki and obsidian-markdown, fallbacks when not installed, each with `UPSTREAM.md` |
| `scripts/harness.py` | the CLI, reachable as `harness` after install |
| `evals/evals.json` | test prompts for skill-creator |
| `docs/` | `decisions/` (D-numbered) and `log.md` |
