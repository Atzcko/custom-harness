# Targets

The harness core is tool-neutral. This file records what each tool actually
reads, verified against its documentation on the date shown, and what the
adapter in `harness compile` writes for it. When a tool changes, this file and
the renderer change together; the librarian's refresh brief includes it.

Verified 2026-09-13. Sources are the tools' own docs, quoted in the log of the
research that produced this table.

## What every tool shares

- **Skills.** Claude Code, Codex, Gemini CLI, Cursor and OpenCode all read
  the Agent Skills standard: a directory with `SKILL.md` carrying `name` and
  `description`. The one location all of them read is `~/.agents/skills/`
  for the user and `.agents/skills/` in a project. The installer links the
  harness there, plus each tool's own folder.
- **Instruction files.** `AGENTS.md` is read by Codex, Cursor and OpenCode
  natively, by Gemini CLI only when `context.fileName` lists it, and not by
  Claude Code, which reads `CLAUDE.md`. `init` writes the harness pointer to
  the file each detected tool reads; `compile` keeps a generated roster table
  in `AGENTS.md` and `GEMINI.md` so those tools see the agents even without
  native definitions.
- **Subagents have no portable format.** Each tool gets its own rendering of
  the same prompt. The generic prompt in `harness/compiled/<name>.md` is the
  fallback for a tool that has none.

## Per tool

| | Claude Code | Codex | Gemini CLI | Cursor | OpenCode |
|---|---|---|---|---|---|
| detected by | `.claude/`, `CLAUDE.md`, or `~/.claude` | `.codex/`, `AGENTS.md`, or `~/.codex` | `.gemini/`, `GEMINI.md`, or `~/.gemini` | `.cursor/` or `~/.cursor` | `.opencode/`, `opencode.json`, or `~/.config/opencode` |
| instruction file | `CLAUDE.md` | `AGENTS.md` (global `~/.codex/AGENTS.md`) | `GEMINI.md` (global `~/.gemini/GEMINI.md`) | `AGENTS.md` and `.cursor/rules/*.mdc` | `AGENTS.md` (global `~/.config/opencode/AGENTS.md`) |
| skills folder | `~/.claude/skills`, `.claude/skills` | `~/.agents/skills`, `.agents/skills` | `~/.gemini/skills` or `~/.agents/skills`; `.gemini/skills` or `.agents/skills` | `~/.cursor/skills`, `~/.agents/skills`, also reads `.claude/skills` and `.codex/skills` | `~/.config/opencode/skills`, `~/.claude/skills`, `~/.agents/skills` |
| agent definition | `.claude/agents/<name>.md`, YAML frontmatter | `.codex/agents/<name>.toml`: `name`, `description`, `developer_instructions`, optional `model`, `model_reasoning_effort` | `.gemini/agents/<name>.md`: frontmatter `name`, `description`, `model`, `tools`; body is the system prompt | `.cursor/agents/<name>.md`: `name`, `description`, `model`, `is_background`; body is the prompt; also reads `.claude/agents` and `.codex/agents` | `.opencode/agents/<name>.md`: `description`, `mode`, `model`; body is the prompt |
| model field | `sonnet`, `opus`, `haiku`, `fable`, full id, `inherit` | id such as `gpt-5.6-terra`; `gpt-5.6` aliases Sol | id such as `gemini-3.7-flash`; default `inherit` | bare slug such as `claude-sonnet-5` or `gpt-5.6-sol` | `provider/model`, e.g. `anthropic/claude-sonnet-5` |
| nesting | up to three levels below the conversation | not documented | **no**; a subagent cannot call another | two levels; a child cannot spawn | not documented |
| memory | `memory: user` loads `MEMORY.md` automatically | none built in | none built in | none built in | none built in |
| how to delegate | Agent tool with the agent's name | ask in natural language; `/agent` switches threads | exposed as a tool named after the agent; `@name` forces it | Task tool or `/name` | Task tool or `@name` |

## What the adapters do with the differences

- **Spawn lists.** Claude Code gets an `Agent(a, b)` allowlist that the
  runtime enforces. Cursor gets a sentence naming allowed children and the
  two-level limit. Gemini CLI gets a sentence saying to return subtasks to
  the conductor, because it cannot nest. Codex and OpenCode get a sentence
  naming the children; enforcement is by prompt.
- **Memory.** Every prompt names the portable memory file. Claude Code also
  gets `memory: user` and a link so its automatic loading hits the same file.
- **Models.** Each target resolves its tier through its provider in
  `library/models.json`; OpenCode ids get the `anthropic/` prefix. Codex
  also gets a reasoning effort by tier (`xhigh`, `high`, `medium`, `low`).
- **Background agents.** Claude Code gets `background: true`; Cursor gets
  `is_background: true`; the others run when the conductor asks.
- **Tools.** Claude Code and Gemini CLI take a tool list; Cursor and
  OpenCode do not, so the list is omitted and the prompt's boundaries do the
  work.

## Not verified, and treated as absent

- Whether Codex or OpenCode subagents can nest.
- A dedicated skills-directory environment variable in Codex, Gemini CLI,
  Cursor or OpenCode. The launcher on the PATH exists so none is needed.
- Gemini CLI's `pro` and `flash` aliases for the 3.x generation; the registry
  pins ids instead.
