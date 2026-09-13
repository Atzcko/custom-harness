# Bootstrapping a new wiki

Read this when setting up an LLM wiki from scratch. The output of bootstrap is
small: a directory layout, an empty index and log, and — the part that matters
— a **schema doc** tuned to the user's domain. Don't over-build; the wiki
earns structure as it grows.

## 1. Scope it

If the user is present, ask (briefly — a few questions, not a form):

- **Domain and purpose** — what is this wiki about, and what questions should
  it eventually answer? (Research topic? A book being read? Personal tracking?
  Competitive analysis? Team knowledge?)
- **Where should it live?** The wiki root gets its own directory — it will
  contain its own `CLAUDE.md` schema, so never root it in a directory that
  already has a `CLAUDE.md` or unrelated content without explicit
  confirmation. Non-interactive default: a new subdirectory of the working
  directory named after the domain (e.g. `./middlemarch-wiki/`).
- **Sources** — what kinds, roughly how many, arriving how? (Clipped articles,
  PDFs, transcripts, journal entries…) Text-only, or with images? If images:
  suggest the user point Obsidian's attachment folder ("Files and links →
  Attachment folder path") at `raw/assets/` and bind the "Download attachments
  for current file" hotkey, so clipped articles keep local images you can
  actually view (remote URLs rot); record the arrangement in the schema.
- **Consumed progressively?** A book being read, a course in progress, a
  situation unfolding — if so, the wiki must trail the user's frontier, and
  the schema records it (see the template's frontier line and SKILL.md hard
  rule 7). Ask this whenever the corpus is a work the user is experiencing in
  order; getting it wrong spoils the work the wiki exists to accompany.
- **Involvement** — ingest one-at-a-time with discussion, or batch with a
  report? Should good query answers be filed back automatically or on request?
- **Environment** — browsing in Obsidian? (If yes: wikilinks, graph view, and
  optionally Dataview frontmatter all pay off. If the directory will be a new
  Obsidian vault, suggest the user open it as one.) Git for history?

If the user is not available, choose sensible defaults from context and record
in the schema that they are defaults to be revisited.

## 2. Lay it out

Default layout — adapt categories to the domain (a book gets
`characters/`, `themes/`, `plot/`; research gets `entities/`, `concepts/`,
`synthesis/`; an ongoing project gets things like `decisions/`, `components/`,
`meetings/`, `threads/`, with sources being the specs, transcripts, and notes
the project generates over time; personal tracking gets whatever the user's
life needs). Whatever
the names, every layout keeps a sources category and a home for synthesis and
filed query answers — the schema must say where filed answers go:

```
<wiki-root>/
├── CLAUDE.md          ← the schema (template below)
├── raw/               ← immutable sources; never edited
│   └── assets/        ← only if sources carry images (clipped-article downloads)
└── wiki/
    ├── index.md       ← catalog of every page; updated on every change
    ├── log.md         ← append-only chronology
    ├── sources/       ← one summary page per raw source
    ├── entities/      ← people, orgs, places, characters, systems…
    ├── concepts/      ← topics, themes, methods, questions
    └── synthesis/     ← overview, evolving thesis, comparisons, filed answers
```

Create `index.md` with the category headings and `log.md` with a
`## [YYYY-MM-DD] bootstrap | <wiki name>` first entry. If using git,
`git init` and make the initial commit.

Flat variants are fine for small wikis (no subdirectories, categories only in
the index) — say so in the schema either way.

## 3. Write the schema

The schema doc is what makes future sessions disciplined. Instantiate this
template, filling in every `<placeholder>` with what the scoping revealed and
deleting lines that don't apply; leave no placeholders behind:

```markdown
# <Wiki name> — LLM wiki

This directory is an **LLM-maintained wiki** (the "llm-wiki" pattern): raw/
holds immutable sources, wiki/ holds pages the LLM writes and maintains, and
this file is the schema. The human curates sources and asks questions; the
LLM does all filing, cross-referencing, and bookkeeping.

**Purpose:** <domain, and the questions this wiki exists to answer>

## Layout

- `raw/` — sources. Read-only. <how sources arrive; image handling if any>
- `wiki/sources/` — one summary page per source
- `wiki/<category>/` — <one line per category: what lives there>
- Filed query answers go in `wiki/<category>/`.
- `wiki/index.md` — catalog, updated on every change
- `wiki/log.md` — append-only; entries start `## [YYYY-MM-DD] <op> | <title>`

## Conventions

- Wikilinks everywhere a page mentions another; link to not-yet-written pages
  freely — they mark wanted work. Bare `[[wikilinks]]` refer to wiki pages
  only; raw files are linked by explicit `raw/` path.
- Frontmatter on every wiki page: `type`, `tags`, `created`, `updated`<, and
  whatever else the domain needs>. Bump `updated` on every touch.
- Every claim cites its source page or raw file. Contradictions are recorded
  with the canonical block (see the skill's operations reference) — never
  silently resolved.
- **Frontier** (progressively-consumed corpus only): the wiki knows only what
  the sources cover so far — currently <chapter/date/episode N>. The LLM must
  not use its own knowledge of this work or fetch anything beyond the
  frontier, even marked as outside context. Advance this line at each ingest.
- <voice/length/format preferences learned from the user>

## Workflows

- **Ingest**: <one-at-a-time with discussion | batch with report>. Read
  source → takeaways → summary page → sweep the <category names> pages →
  index → log.
- **Query**: index first, cite pages. <File synthesis answers back
  automatically | offer first>; filed answers are indexed and logged too.
- **Lint**: <cadence>. Fix mechanical drift immediately; report judgment calls.

## Decisions

Append-only record of workflow decisions, so they stop being re-litigated:

- [YYYY-MM-DD] <decision and why>
```

## 4. First ingest

If the user brought a first source, ingest it immediately (see
[operations.md](operations.md)) — a bootstrap that ends with a populated
sources page, a couple of entity pages, and a real index teaches the user the
pattern better than any explanation. Then walk them through what got created
and where to look in Obsidian — or, in a non-interactive session, make that
walkthrough the closing section of your report.
