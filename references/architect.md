# Phase: architect

Goal: `harness/architecture.md`, one instance note per agent in
`harness/agents/`, and a compiled `.claude/agents/` folder. The roster is
derived from the brief and the graph, not invented; every role must point at
the domain or task type that justifies it.

Delegate the design to the **architect** library agent on `opus` when the
project is large; it returns a proposed roster and you review it with the user.
For a small project, design it yourself in this conversation. Either way the
steps are the same.

## 1. Derive the roles

Read `harness/brief.md` and `graphify-out/GRAPH_REPORT.md`.

- **Always present:** architect, gardener, librarian, scribe. They are the
  harness's own staff.
- **One lead per domain** that is large enough to have its own vocabulary and
  its own definition of done. Small domains share a lead.
- **Specialists** for task types that recur and need project knowledge:
  implementing in a particular subsystem, reviewing, researching.
- **Workers** for the boiled-down set: tests, lint, formatting, renames,
  summaries. These are usually straight reuses from the library.

Fewer agents is better. Every agent is a note someone has to keep honest. If
two roles would have the same charter with different nouns, that is one agent
with an overlay.

## 2. Match each role against the library

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/harness.py" match "reviews firmware changes for memory safety and LVGL misuse" --tags review,firmware
```

The score is a heuristic; you make the call. The bands:

| Score | Outcome | What to write |
|---|---|---|
| high (≥ 0.60) | **reuse** | instance note linked to the library agent, project context only |
| middle (0.35 – 0.60) | **adapt** | linked instance note with an overlay: extra context, tools, a pinned model |
| low (< 0.35) | **create** | a local draft with its own charter; it earns promotion later |

A proven library agent beats a draft with a slightly better score. Reuse is
the point: the agent already has memory.

Create instance notes with the script so the frontmatter is right:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/harness.py" new firmware-reviewer --title "Firmware reviewer" --tier 1 --model opus --library reviewer --tags review,firmware
```

Then fill the "Project context" section by hand. For a create, also write the
charter under "Charter" in the same note.

## 3. Danger flags and spawn lists

From the brief's "must never happen automatically" list, set `danger:` on
every agent that could do one of those things, and set `irreversible: true`
where the action cannot be undone. The risk policy in `optimize.md` reads
these flags; an agent without them will be merged without asking.

Set `spawns:` to the children each agent may create. Leads spawn specialists,
specialists spawn workers, workers spawn nothing. The compile step turns this
into an allowlist the runtime enforces.

## 4. Write architecture.md

From the template. It holds the roster table, the routing rules (which kind of
request goes to which agent), escalation, budgets from the brief, and the
background agents' cadence. Keep it to one screen; detail lives in the
instance notes.

## 5. Compile, lint, record

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/harness.py" compile
python3 "${CLAUDE_SKILL_DIR}/scripts/harness.py" lint
```

Write the first decision note, `H001 - Initial roster`, with the template.
State why each lead exists and which roles were deliberately left out. Then
show the user the roster in a short table and move to `operate`.

## Changing the roster later

Adding an agent is steps 2 to 5 for that one agent. Removing or merging is the
gardener's job; see `optimize.md`. Changing a library charter is a library
change: bump its `version`, and every project that reuses it recompiles on its
next `status`.
