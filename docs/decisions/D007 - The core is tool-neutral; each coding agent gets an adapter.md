---
title: D007 - The core is tool-neutral; each coding agent gets an adapter
type: decision
status: accepted
date: 2026-09-13
tags:
  - decision
  - architecture
---

# D007 — The core is tool-neutral; each coding agent gets an adapter

## Context

The first build assumed Claude Code: `.claude/agents/`, the `memory:` field,
`${CLAUDE_SKILL_DIR}`, model aliases like `opus`. The owner runs Codex as
well, and wants the harness to work in Codex, Gemini CLI, or whatever comes
next. Everything that matters to the harness is already markdown and a Python
script; only the last mile is tool-specific.

## Decision

The core stays neutral: notes in the project vault, the library, the ledger,
the decision records, the script. Everything a specific tool needs is an
**adapter**, selected with `harness compile --target` and auto-detected from
the project and the home directory:

- `claude` writes `.claude/agents/<name>.md` with Claude Code frontmatter.
- `codex` writes what Codex reads, described in `references/targets.md`.
- `gemini` writes what Gemini CLI reads, likewise.
- `generic` always runs and writes `harness/compiled/<name>.md` plus a JSON
  sidecar, a prompt any tool can be pointed at.

The skill is installed into every skills location that exists
(`~/.agents/skills`, the cross-tool standard, plus `~/.claude/skills`,
`~/.codex/skills`, `~/.gemini/skills`), and a `harness` launcher goes on the
PATH so no playbook needs a tool-specific environment variable.

## Consequences

Adapters must be kept honest against each tool's documentation, which changes.
`references/targets.md` records what was verified and when; the librarian's
refresh brief includes it. Features one tool lacks, such as nested spawning or
auto-loaded memory, degrade to instructions in the prompt rather than
breaking the harness.

## Related

- [[D008 - A dated model registry decides which model each tier runs]]
- [[D009 - Portable memory lives in the library, not in a tool's directory]]
