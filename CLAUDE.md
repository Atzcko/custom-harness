# Custom Harness Design — the `harness` skill

This repository is a Claude Code skill and an Obsidian vault. `SKILL.md` at the
root is the skill; it is installed by symlinking this folder to
`~/.claude/skills/harness` (`./install.sh`). Start at [[index]].

## Working agreements

1. **Read `docs/decisions/` before changing how the harness works.** Six
   decisions exist so the same ground is not re-litigated. Disagree by writing
   a new decision that supersedes the old one, never by editing it.
2. **Every change to the skill bumps `VERSION` and gets a `CHANGELOG.md` entry
   that says why.** PATCH for wording and fixes, MINOR for a new command,
   playbook or seed agent, MAJOR for a change to what the harness writes into
   a project or to the risk policy.
3. **Append to `docs/log.md` at the end of any session that changes the
   repository.** Newest at the bottom.
4. **Test on a fixture, never on the library.** `scripts/harness.py` updates
   the library's track-record fields (`used_in`, `tasks`, `successes`,
   `last_used`) whenever a ledger row is added or a draft is promoted. A test
   run against a fixture project leaks fixture names into the real library.
   After any test: reset those fields on touched seed agents, remove promoted
   fixture agents from `library/agents/`, drop fixture lines from
   `library/LESSONS.md`, and run `python3 scripts/harness.py index`.
5. **Before a commit:** `python3 scripts/harness.py lint` (in this directory it
   lints the library) and the skill-creator validator:

   ```bash
   uv run --with pyyaml python "$HOME/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py" .
   ```

   (The validator needs PyYAML, which the system Python does not have; `uv`
   supplies it without installing anything globally.)

6. **Generated files are generated.** `library/INDEX.md` comes from
   `harness.py index`; compiled agents come from `harness.py compile`. Edit the
   source note, then regenerate.

## Conventions

- Notes under `docs/` use wikilinks and follow the obsidian-markdown skill:
  a `type:` property on every note, decision titles that state the
  conclusion, absolute dates.
- `references/` and `templates/` are read by the model at run time. Write
  them for a reader with no context: explain why, avoid shouting, keep each
  file to what one phase needs.
- Library charters are written in the second person and must make sense in a
  project other than the one that produced them.
- The script is standard library only, so it runs on any Python 3 without a
  virtual environment.

## Layout

| Path | What |
|---|---|
| `SKILL.md` | entry point and phase router |
| `references/` | playbooks: orchestrator, understand, architect, operate, optimize, evolve, interview, model-tiers, memory-protocol, library |
| `templates/` | agent, instance, brief, architecture, decision, ledger, evolution, harness-index, wiki-schema |
| `library/` | `agents/`, `archive/`, `decisions/` (L-numbered), `INDEX.md`, `LESSONS.md` |
| `scripts/harness.py` | the CLI |
| `evals/evals.json` | test prompts for skill-creator |
| `docs/` | `decisions/` (D-numbered) and `log.md` |
