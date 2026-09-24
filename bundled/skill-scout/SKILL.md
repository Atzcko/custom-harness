---
name: skill-scout
description: Plan which skills a piece of work should use before starting it. Breaks the task into parts, scans every installed skill (all agent tools, the project, plugins, and the skills the agent already sees), picks the ones that fit and the order to use them in, and flags gaps — suggesting a skill to look for online, a new skill to write, or an existing skill to upgrade — then waits for approval before installing, creating or changing anything. Use when the user says "which skills should I use", "scout skills", "pick the skills for this", "plan the skills", "do I have a skill for", "what skills fit this task", invokes /skill-scout, or starts a large or multi-part task and asks how to approach it with their skills. Not for running a single skill the user already named.
---

# Skill scout

Match the work to the skills, before the work starts. The output is a short
plan the user approves; nothing is installed, created or edited without that
approval.

## 1. Understand the work

State the task back in one or two sentences, then split it into the parts a
skill could own: e.g. *research → design → build UI → write docs → review*.
Keep it to the parts that actually differ in method; three to six is typical.
If the task is ambiguous enough that the split would change, ask one question
first. If it is tiny (one step, obvious method), say so and skip the scout —
a plan is overhead there.

## 2. Take the inventory

Two sources, and both count:

1. **What is on disk**, from every tool's folder, the project and plugins:

   ```bash
   python3 scripts/inventory.py                  # every skill, one line each
   python3 scripts/inventory.py --query "<part>" # ranked candidates for one part
   python3 scripts/inventory.py --show <name>    # read a candidate in full
   ```

   (Run from this skill's folder; in Claude Code the folder is
   `${CLAUDE_SKILL_DIR}`.) The `--query` ranking is only word overlap — a
   pre-filter, not a verdict. Judge the fit yourself from the descriptions.

2. **What the agent already sees**: the skill list in your own context
   (built-in, account and plugin skills that may not exist as folders, such as
   document or PDF skills). Include them; tag them `built-in`.

Each on-disk skill carries an owner tag, which decides what an upgrade may do:

| tag | meaning | may be edited? |
|---|---|---|
| `own` | written by the user, in a git repository | yes, in its repository |
| `adapted` | the user's copy of an upstream skill (has `UPSTREAM.md`) | yes; record the change in `UPSTREAM.md` |
| `vendor` | third-party copy under `vendor/` | no — propose adapting it into the user's own skills instead |
| `plugin` / `built-in` | shipped by someone else | no — propose a companion skill instead |
| `local` | loose folder, no repository | yes, but suggest moving it into the skills repository |

## 3. Match

For each part, read the top candidates' full `SKILL.md` (`--show`) before
choosing — a description can promise more or less than the body delivers.
Decide one verdict per part:

- **USE** `<skill>` — fits as is. Note anything the user must supply.
- **USE + UPGRADE** `<skill>` — fits, but misses something this task needs
  and future tasks will too (a missing format, an outdated step, a trigger
  that should have fired). Name the concrete change.
- **BROWSE** — no installed skill fits and the need is common enough that
  someone has probably published one. Give the search terms.
- **CREATE** — no skill fits and the method is specific to this user, or it
  will recur. Sketch name, trigger and the steps it would hold.
- **NONE NEEDED** — ordinary work; a skill would add nothing.

Rules of judgment:

- Prefer fewer skills. Two skills that overlap on one part (e.g. two frontend
  design skills) → pick one and say why; loading both gives conflicting advice.
- A one-off gap is **NONE NEEDED**, not **CREATE**. Suggest a new or upgraded
  skill only when the same need is likely to come back.
- Prefer upgrading a close fit over creating a near-duplicate.
- Never propose editing `vendor`, `plugin` or `built-in` skills in place.

## 4. Present the plan

One table, then the proposals, then a question. Keep it scannable:

```
Task: <one sentence>

| # | Part            | Verdict        | Skill / action                      | Why |
|---|-----------------|----------------|-------------------------------------|-----|
| 1 | Page design     | USE            | design-taste-frontend               | landing page, anti-template |
| 2 | Loading state   | USE            | animations                          | offline picker, has orbs |
| 3 | Copy review     | BROWSE         | "ux writing", "microcopy"           | nothing installed covers copy |
| 4 | Deploy          | NONE NEEDED    | —                                   | one command |

Order: 1 → 2 → 3.  Skipped on purpose: frontend-design (overlaps with #1).

Proposed changes (need your OK):
- UPGRADE animations: add a "respect prefers-reduced-motion" step to snippets
- BROWSE for a copy-review skill
```

Ask which proposals to act on. Stop there until the user answers.

## 5. Act on what was approved

- **USE** — invoke the skills in the planned order as the work proceeds (or,
  if the user only wanted the plan, stop).
- **BROWSE** — search the places skills are published: the agent's own skill
  or plugin search tools when it has them, the Anthropic skills repository
  (github.com/anthropics/skills), agentskills.io, and GitHub for
  `SKILL.md <topic>`. Return at most three candidates with source, licence,
  last update and what each would cover. Read a candidate's `SKILL.md` and any
  scripts before recommending it; say plainly if it runs code or fetches from
  the network. Installing is a separate, explicit yes — and it follows the
  skills repository's own rules for third-party skills (see below).
- **CREATE** — use a skill-authoring skill if one is installed
  (e.g. `skill-creator`); otherwise write `SKILL.md` directly: frontmatter
  with only `name` and `description`, a description that says what it does
  *and* when to trigger, steps in the body, scripts on the standard library,
  paths relative to the skill folder.
- **UPGRADE** — edit the skill in its repository (the inventory's `repo`
  field), keep the change minimal and scoped to what the task showed was
  missing, and show the diff. For an `adapted` skill, note the change in its
  `UPSTREAM.md`. For a `vendor` skill, copy it into the user's own skills as an
  adapted skill first, with the approval that implies.

### Where new and changed skills go

If the inventory lists a repository that holds the user's skills (a folder
with `skills/`, often `vendor/`, an `install.sh` and a README), that
repository is the source of truth: create and edit there, follow its README
(checks, changelog, vendoring rules, install step), and never edit the
installed copies in the tools' home folders — those are links. Commit only
when the user asks. With no such repository, create the skill in the folder
the user's main tool reads (`~/.claude/skills/<name>/`, or
`~/.agents/skills/<name>/` for the other tools) and say where it went.

## After the work

If a chosen skill turned out wrong or thin during the task, say so in one
line at the end and offer the upgrade then — that evidence is better than any
guess made up front.
