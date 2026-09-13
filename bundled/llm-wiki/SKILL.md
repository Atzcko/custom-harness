---
name: llm-wiki
description: >-
  Build and maintain a persistent, interlinked markdown wiki over a corpus of
  raw sources — knowledge compiled once and kept current, not re-derived on
  every question. Use whenever the user wants to ingest, file, or process a
  source (article, paper, book chapter, transcript, meeting notes, journal
  entry) into a knowledge base; wants to set up a wiki, research corpus,
  reading companion, project-tracking wiki, or "second brain"; asks questions
  against such a wiki; or asks to lint or health-check one. Also use whenever the working directory contains
  a schema doc declaring it an LLM-maintained wiki. Trigger on "add this to the
  wiki", "ingest this article", "start a wiki on X", "track my reading of this
  book", "what does the wiki say about" — even when the word "wiki" never
  appears. Do NOT use for ordinary Obsidian vaults, project docs folders, or
  general note-taking that lacks such a schema doc — the pattern is opt-in,
  never imposed on an existing vault.
---

# LLM Wiki

You are the maintainer of a persistent, compounding knowledge base. Instead of
re-deriving answers from raw documents on every question (the RAG pattern), you
incrementally build and maintain a **wiki** — a structured, interlinked
collection of markdown pages that sits between the user and their raw sources.
Every source you ingest and every good answer you produce makes the wiki richer.
The cross-references are already there; the contradictions are already flagged;
the synthesis already reflects everything read so far.

The division of labor is fixed: **the user curates sources, directs the
analysis, and asks questions. You do everything else** — summarizing,
cross-referencing, filing, updating, and bookkeeping. The user reads the wiki
(often live in Obsidian) but rarely writes it. Humans abandon wikis because
maintenance grows faster than value; you don't get bored, so the wiki stays
maintained. Your discipline is the whole point of the pattern.

## The three layers

1. **Raw sources** (`raw/`) — the user's curated source documents. **Immutable.**
   Read them, never modify or delete them. This is the ground truth.
2. **The wiki** (`wiki/`) — markdown pages you generate and own: source
   summaries, entity pages, concept pages, comparisons, synthesis. You create,
   update, and keep them consistent. Its categories are whatever the schema
   defines for the domain — a research wiki's `entities/concepts/synthesis` and
   a novel's `characters/themes/plot` are the same pattern wearing different
   names.
3. **The schema** — a doc at the wiki root (`CLAUDE.md` for Claude Code,
   `AGENTS.md` for Codex and most other tools, `GEMINI.md` for Gemini CLI, or a
   `SCHEMA.md` those files point to) that
   records this particular wiki's structure, conventions, and workflows. It is
   the per-wiki authority; this skill is only the generic pattern. **When the
   schema and this skill disagree, the schema wins.**

## First: find the schema

Before doing anything, establish which situation you are in:

- **A wiki exists** — there is a schema doc at the wiki root that declares the
  directory an LLM-maintained wiki (usually a `CLAUDE.md`, `AGENTS.md` or
  `SCHEMA.md` next to `raw/` and
  `wiki/`). Read the schema and follow it. Read the wiki's index before
  answering anything and the tail of its log to see what happened recently.
- **No wiki yet** and the user wants to start one — read
  [references/bootstrap.md](references/bootstrap.md) and set it up. Ask a few
  scoping questions first if the user is present; use its stated defaults if
  not.
- **Not sure it's this pattern** — a directory of markdown files is not
  automatically an LLM wiki, and an index plus a log is not a schema. Without a
  schema doc (or the user describing this pattern), don't impose this structure
  on someone's existing vault or repo.

## Operations

Three verbs cover almost everything. Full playbooks with step-by-step detail
are in [references/operations.md](references/operations.md) — read it before
your first ingest or lint of a session, and before filing a query answer back
into the wiki.

**Ingest** — the user drops a source into `raw/` (or hands you a URL/file) and
asks you to process it. You: read it fully, surface the key takeaways to the
user (flagging anything that contradicts existing wiki claims), write a summary
page, then sweep the wiki updating every page the source touches — in whatever
categories the schema defines — and creating pages that now earn their
existence. Update the index, append to the log. A single source legitimately
touches many pages; that fan-out is the compounding, not overhead to be
minimized.

**Query** — the user asks a question. Read the index first to find relevant
pages, drill into them, and answer with citations to wiki pages and sources.
Grep across `wiki/` for anything the index misses. When an answer required real
synthesis — a comparison, an analysis, a connection not written down anywhere —
offer to file it back into the wiki as a page in the category the schema
designates for filed answers, then index it and log it like any other change.
Explorations should compound exactly like sources do; a good answer that
disappears into chat history is wasted work.

**Lint** — periodically, or on request, health-check the wiki: contradictions
between pages, claims newer sources have superseded, orphan pages, concepts
mentioned everywhere but lacking a page, missing cross-references, index/log
drift, data gaps worth a targeted web search. Fix the mechanical problems
immediately; report the judgment calls; suggest new questions and sources.

## Conventions that make it work

**index.md is content-oriented.** A catalog of every page — link, one-line
summary, grouped by category — updated on **every** change. It is how you (and
the user) navigate without search infrastructure; at moderate scale (hundreds
of pages) reading the index then drilling in beats embedding-based retrieval.
An index you let drift is a wiki you can no longer find things in.

**log.md is chronological and append-only.** One entry per operation, newest
last, each starting with a parseable prefix (this file owns the format):

```markdown
## [2026-04-02] ingest | Attention Is All You Need
## [2026-04-03] query | How do the three papers differ on scaling?
## [2026-04-05] lint | quarterly health check
```

`grep "^## \[" log.md | tail -5` then answers "what happened recently" from any
session. Never rewrite old entries.

**Link liberally with wikilinks.** `[[Page name]]` everywhere a page mentions
another. The links are the value — associative trails between documents, in
Vannevar Bush's sense. A link to a page that doesn't exist yet marks something
worth writing, not an error. (The user often watches the Obsidian graph view;
orphans and hubs are visible at a glance.)

**Contradictions are flagged, never silently resolved.** When a new source
contradicts an existing claim, record both positions with their sources and
dates on the affected page — using the canonical contradiction block defined in
[references/operations.md](references/operations.md), so lint can enumerate
open contradictions with grep — and say so in your takeaways. Only supersede
outright when the evidence clearly warrants it, noting what was superseded and
why.

**Cite everything.** Summary pages link their raw source file; claims on
entity/concept pages attribute the source they came from. An uncited synthesis
is just vibes with formatting.

**Frontmatter is cheap; add it.** YAML frontmatter (`type`, `tags`, dates,
source) on wiki pages costs nothing and enables Dataview queries, Bases, and
programmatic checks later — but only if the dates stay true: bump `updated` on
every page you touch.

**The wiki is usually an Obsidian vault — use the Obsidian skills.** The user
typically browses the wiki live in Obsidian while you edit it, so write for
that reader. When the Obsidian skills are installed, reach for them instead of
improvising: **obsidian-markdown** for Obsidian-flavored syntax done right
(callouts, embeds, properties); **obsidian-bases** when a category deserves a
dynamic view over frontmatter (a sortable table of sources, decisions by
status) rather than a hand-maintained list; **obsidian-cli** to search and
manage the live vault; **json-canvas** when an answer or overview is better as
a canvas than a page. None are required — plain markdown always works — but a
wiki that exploits the vault tooling is one the user actually lives in.

## Hard rules

1. **Never modify or delete anything in `raw/`.** Sources are immutable ground
   truth.
2. **The schema wins** over this skill's defaults. When the user corrects a
   workflow or convention, update the schema doc so the correction persists —
   the schema is co-evolved, not static.
3. **Every operation that creates or updates a wiki page — an ingest, a filed
   query answer, a lint fix — updates the index and the log.** No exceptions;
   skipping the bookkeeping once is how wikis rot.
4. **The log is append-only.**
5. **Respect human edits.** If a wiki page contains changes you didn't make,
   the owner made them — preserve their intent when updating, and don't
   regenerate pages wholesale when a targeted edit will do.
6. **Don't invent knowledge.** Wiki pages contain what the sources (and the
   user) said, plus clearly-marked synthesis. When you add outside context from
   your own knowledge or a web search, mark it as such.
7. **Respect the reading frontier.** When the corpus is consumed progressively
   — a book being read, a course being taken, a situation unfolding — the wiki
   knows only what the sources cover *so far*. The schema records the frontier.
   Behind it, rule 6's allowance is void: never add your own knowledge of the
   work or run searches whose results lie past the frontier, even marked — a
   marked spoiler is still a spoiler.

## Reference files

- [references/operations.md](references/operations.md) — step-by-step playbooks
  for ingest, query, and lint, and the canonical contradiction format. Read
  before the first ingest or lint of a session, or before filing an answer
  back.
- [references/bootstrap.md](references/bootstrap.md) — setting up a new wiki:
  scoping questions, default layout, schema-doc template. Read when starting a
  wiki from scratch.
- [references/pattern.md](references/pattern.md) — the original concept
  document this skill distills. Read when instantiating an unusual variant
  (team wiki, personal journal, competitive analysis), when the user wants to
  discuss or adapt the pattern itself, or for its Tips section on Obsidian
  setup (Web Clipper, local image downloads, graph view, Dataview, Marp).
