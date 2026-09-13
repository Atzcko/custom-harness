# Memory protocol

Every agent has two memories. Both are markdown, both live in git. The rule
about what goes where is the one rule that must not drift, because it is what
keeps one project's facts out of another project's context.

## The two memories

**Portable memory** is `library/memory/<agent>/MEMORY.md` in the skill
repository. It follows the agent into every project and every tool, because
it is just a file next to the charter. Every compiled prompt names its
absolute path and says: read it first, append at the end.

In Claude Code the compiled definition also declares `memory: user`, and
`compile` links `~/.claude/agent-memory/<agent>` to the library directory, so
Claude Code loads the same `MEMORY.md` into the agent's prompt automatically
and its own memory instructions write to the same file. Other tools get no
automatic loading; the prompt's first step covers it.

**Project memory** is the "Project memory" section of the instance note,
`harness/agents/<name>.md`. It is read by the agent at the start of every task
and appended at the end. It is visible in the vault, wikilinked, and shared by
everyone who works on the project.

## What goes where

| Belongs in portable memory | Belongs in project memory |
|---|---|
| how to do the job better anywhere | where things are in this project |
| a tool's quirks | this project's conventions and constraints |
| a pattern that recurs across projects | a decision this project made |
| a mistake worth never repeating | a person's preference in this project |

The test: **would this line be true and useful in a different project?** If
yes, portable. If it names a file, a person, a device, a customer or a
deadline, project.

Secrets never go in either. If an agent learns a credential, it forgets it.

## The reading order

1. The compiled prompt, which carries the charter and the project context.
2. The instance note, read as the first action.
3. `MEMORY.md` from the portable directory, loaded automatically in Claude
   Code and read explicitly elsewhere.
4. The task prompt from the conductor.

Later items are more specific and win conflicts.

## Writing

- Append; do not rewrite history. A lesson that turned out wrong gets a new
  line saying so, dated.
- Keep `MEMORY.md` under about two hundred lines; when it grows, move detail
  into topic files in the same directory and keep the index short. Claude Code
  tells the agent when it must; elsewhere the agent has to notice.
- Date every line. Absolute dates only.

## Promotion, merges, renames

Promotion copies the charter, not the project memory. When a draft is promoted
under a new name, its memory directory is renamed with it. The gardener
carries project-memory sections over during a merge and never edits them;
they are history and belong to the project. A merged agent starts with an
empty portable memory; its sources' memories stay in place under their old
names for a reader who needs them.
