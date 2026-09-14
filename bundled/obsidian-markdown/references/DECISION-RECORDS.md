# Decision records in a vault

A decision record is one note per decision, written when the decision is made,
never edited to reverse it. In a vault it is better than the usual ADR folder
because the links are bidirectional: a decision shows you everything that cites
it, which is exactly what you want before changing it.

## The note

```markdown
---
title: D026 - Apps are a platform, not a special case
type: decision
status: accepted        # accepted | superseded | rejected
date: 2026-08-17
tags:
  - decision
  - architecture
---

# D026 — Apps are a platform, not a special case

## Context
What made this non-obvious. The constraint, the failed attempt, the thing that
was tried first. **If the reasoning is recoverable from the code, the note is
not worth writing.**

## Decision
The conclusion, in the present tense, as an instruction.

## Consequences
What this costs, including the parts you are not happy about.

## Related
- [[D014 - Touch hit-testing]]
```

## Naming: a stable ID plus a claim

`D026 - Apps are a platform, not a special case.md`

- **The ID is immutable.** It is what source-code comments cite (see
  [VAULT-IN-A-REPO.md](VAULT-IN-A-REPO.md) §3 — a wikilink in a `.cpp` file
  rots on rename, a bare `D026` does not).
- **The title states the conclusion, not the topic.** `D002 - Pin LVGL to
  8.4.0` beats `D002 - LVGL version`, because the wikilink then reads as an
  argument wherever it appears: "…upgrading breaks the link, not just the API
  ([[D002 - Pin LVGL to 8.4.0]])."

Titles this specific make the *sentence containing the link* the summary, which
is why a vault of decisions stays readable as it grows.

## Superseding, never editing

When a decision reverses, write a new note and mark the old one:

```yaml
status: superseded
superseded_by: "[[D031 - Hush at the end of every turn]]"
```

Do not delete or rewrite it. Every inbound link — from other notes, from a
changelog, from a commit message — still points at the old ID, and a reader who
follows one needs to land on the reasoning that was true at the time plus a
pointer forward. Rewriting history here is how the same ground gets
re-litigated a month later.

State the reversal explicitly in the new note: *"This reverses D023. That rule
existed because X; Y removed the reason."* The strongest thing a decision log
does is record why a rule that now looks wrong was once right.

## Where the numbers come from

Sequential and never reused, allocated when the note is written. Gaps are fine.
Do not group by area (`UI-01`, `NET-01`) — decisions cross areas, and you will
spend more time deciding the prefix than writing the note.

## Keeping the index honest

A hand-written table in `index.md`, one row per decision, ID and a one-line
claim. It costs one line per note and it is the only place a broken or missing
decision is visible at a glance:

```markdown
| [[D027 - The gesture budget]] | One finger, four gestures — displacement disqualifies a press |
```

Add the row in the same edit as the note. A decision that is not in the index
is one nobody will find.

## What belongs, and what does not

| Write a decision for | Do not |
|---|---|
| A constraint that will look arbitrary later | Anything git history already explains |
| Something tried, failed, and rejected | A restatement of the code |
| A rule that reverses an earlier rule | A bug and its fix — that is the log |
| A trade-off with a named cost | A preference with no alternative considered |

The test: **would someone reasonably do the opposite?** If not, there is no
decision to record.

## The companion log

Decisions answer *why is it like this*. They do not answer *what happened*.
Keep a separate append-only `log.md`, newest at the bottom, for the narrative:
what was attempted, what broke, what it measured. The two link to each other
and neither absorbs the other's job.
