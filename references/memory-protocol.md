# Memory protocol

Every agent has two memories. Both are markdown. The rule about what goes
where is the one rule that must not drift, because it is what keeps one
project's facts out of another project's context.

## The two memories

**Portable memory** is the agent's own directory, provided by Claude Code's
`memory:` field in the compiled definition. Library-linked agents use the
`user` scope, so the directory lives under `~/.claude/agent-memory/<name>/`
and follows the agent into every project. Its `MEMORY.md` is loaded into the
agent's prompt automatically. Local drafts use the `project` scope until they
are promoted, so their memory stays in the project.

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
2. `MEMORY.md` from the portable directory, loaded automatically.
3. The instance note, read with the Read tool as the first action.
4. The task prompt from the conductor.

Later items are more specific and win conflicts.

## Writing

- Append; do not rewrite history. A lesson that turned out wrong gets a new
  line saying so, dated.
- Keep `MEMORY.md` under the size the runtime loads (about two hundred lines);
  when it grows, move detail into topic files in the same directory and keep
  the index short. The runtime tells the agent when it must.
- Date every project-memory line. Absolute dates only.

## Promotion and merges

Promotion copies the charter, not the project memory. The gardener carries
project-memory sections over during a merge and never edits them; they are
history and belong to the project.
