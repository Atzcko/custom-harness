# Operation playbooks

Step-by-step playbooks for the three core operations. The wiki's own schema
doc overrides anything here — these are the defaults for a wiki whose schema
doesn't say otherwise. Where this file says "entity/concept/synthesis", read
the category names the schema actually defines; that triad is just the default
research layout.

## Ingest

The goal is not to summarize a document; it is to **integrate** it, so the
wiki afterwards reads as if it had always known this source.

1. **Place the source.** If handed a URL or a loose file, put a markdown copy
   into `raw/` (Obsidian Web Clipper output, a converted PDF, pasted notes).
   Name it descriptively. Never edit a source that's already there.
2. **Read it fully** — the whole text, not a skim. If the markdown references
   local images, read the text first, then view the images that carry real
   information (figures, charts, screenshots) as a second pass.
3. **Surface takeaways before filing.** Tell the user the 3–7 things that
   matter: what's new, what's surprising, and — most importantly — **what
   contradicts or complicates something the wiki already claims**. If the user
   is present, this is the moment they steer emphasis ("focus on the methods,
   ignore the politics"). If the session is non-interactive, state the
   takeaways in your report and proceed with judgment.
4. **Write the source summary page** in the schema's sources category:
   frontmatter (type, dates, link to the raw file), a summary in your own
   words sized to the source's importance, key claims/data worth citing later,
   and wikilinks to every entity and concept it touches. Link the raw file by
   explicit path (`[[raw/<name>]]` or a relative markdown link) — bare
   wikilinks are reserved for wiki pages, because in an Obsidian vault a
   summary page often shares its raw file's basename and a bare `[[name]]`
   could resolve to either.
5. **Sweep the wiki.** This is the step that makes the pattern work — never
   skip it. First build the candidate list, don't trust memory: take the
   entities and concepts you just linked from the summary page, re-scan the
   index for pages matching them, and grep across `wiki/` for the same terms
   to catch pages whose index lines don't mention them. The union is your
   sweep list. Then, for each page the source touches, in whatever categories
   the schema defines:
   - add the new facts, cited to this source;
   - revise summaries the new information changes;
   - flag contradictions with the canonical block below, never by overwriting;
   - strengthen or challenge the evolving synthesis/overview page;
   - bump `updated` in the frontmatter of every page you touch.
   Create new pages for things that now earn one — a person, place, theme, or
   claim that is load-bearing in this source or has now appeared in two. In a
   mature wiki a source often touches 10–15 pages; in a young one, far fewer.
   The test is coverage, not count: every page this source is load-bearing for
   got updated or created. Touching only the summary page is almost always
   under-integration; padding the count with thin stubs is not integration
   either.
6. **Update the index** — add the new pages with one-line summaries in the
   right categories; adjust lines whose summaries the ingest invalidated.
7. **Append to the log** (format owned by SKILL.md):
   `## [YYYY-MM-DD] ingest | <Source title>` plus 2–4 lines: what it was, what
   changed in the wiki (pages created/updated), and any contradiction flagged.
8. **Report.** List pages created and updated (they render as clickable links),
   the takeaways, and anything the user should look at in Obsidian.

**Batch ingest**: same steps per source, but surface takeaways as one combined
report at the end, and consider a mini-lint afterwards — batches are where
cross-references get missed. Prefer one-at-a-time when the user wants to stay
involved; record their preference in the schema.

### The canonical contradiction block

One shape, everywhere, so open contradictions are machine-findable:

```markdown
> [!warning] Contradiction
> [[meridian-report]] (2026-03-02): the facility opened in 1958.
> [[harlow-memoir]] (2026-04-11): construction was not finished until 1961.
```

Each position cites its source page and the date it was ingested. Place the
block on the page that carries the claim. When later evidence resolves it,
replace the block with the settled claim plus a one-line note of what was
superseded and why. `grep -rn '\[!warning\] Contradiction' wiki/` lists every
open contradiction — lint depends on this.

## Query

1. **Read the index first**, then open the pages that plausibly bear on the
   question. Grep across `wiki/` for terms the index might not surface. Check
   the tail of the log if recency matters. Only go back to `raw/` sources
   when the wiki's compiled knowledge is insufficient or the user wants exact
   quotes/details — and if you find yourself doing that often, the wiki is
   missing a page; consider that a lint finding.
2. **Answer with citations** — name the wiki pages (and through them the
   sources) each claim rests on. Where the wiki records a contradiction,
   present both positions; don't quietly pick a side the wiki hasn't picked.
3. **Match the output form to the question** — prose, a comparison table, a
   Marp deck, a chart, a canvas — whatever the schema says the user likes.
4. **File good answers back.** If the answer involved real synthesis (a
   comparison, an evaluation, a connection no page had made), offer to save it
   as a wiki page — or just do it, if the schema says so. File it in the
   category the schema designates for filed answers (`synthesis/` in the
   default research layout), add wikilinks in both directions, update the
   index, and log it: `## [YYYY-MM-DD] query | <Question>`. Trivial lookups
   don't get filed; the bar is "would this answer be worth re-deriving next
   month?"

## Lint

Run when asked, after a large batch ingest, or when you notice drift. Two
kinds of findings: **mechanical** (fix immediately) and **judgment** (report,
let the user decide).

**Scope it first.** On a small wiki, lint everything. On a mature one, a full
editorial read of every page degrades into skimming — bound the pass instead:
default to the pages changed since the last `lint |` log entry (git history or
file mtimes) plus every page they link to; rotate through one category per
lint for the editorial checks; reserve the full-corpus read for an explicit
"full lint". Record the scope in the log entry so the rotation is visible.

Mechanical checks — scriptable, so script them (`grep`/`ls` are enough):

- **Index drift**: pages on disk missing from the index; index entries whose
  file no longer exists; summaries that no longer match the page.
- **Broken wikilinks**: `[[Links]]` with no matching page. Decide per link:
  create a stub, or remove/reword. A red link that marks genuinely-wanted
  future work may stay — note it.
- **Orphan pages**: no inbound links **from content pages** — exclude the
  index and log when counting, since the index links everything by design and
  would make this check vacuous. Either link orphans from where they're
  relevant or ask whether they still belong.
- **Open contradictions**: grep for the canonical block and list them — age
  and count are worth reporting even when none can be resolved yet.
- **Stale frontmatter**: `updated` dates that predate the file's real
  modification history.
- **Log gaps**: wiki changes with no log entry (compare recent file mtimes or
  git history against the log tail).

Judgment checks — read the scoped slice like an editor:

- **Contradictions between pages** that no page acknowledges.
- **Stale claims** superseded by newer sources but still stated as current.
- **Missing pages**: a concept mentioned on 3+ pages with no page of its own
  — provided the wiki actually holds enough about it to fill one. Mention
  count measures demand; information content measures supply. If every
  mention traces back to one sentence in one source, a red link under the
  index's wanted list beats a thin stub.
- **Missing cross-references**: two pages that obviously bear on each other
  with no link either way.
- **Data gaps**: questions the wiki raises but can't answer — suggest specific
  sources to find or web searches to run, and offer to run them. On a
  frontier-limited wiki (see the schema and SKILL.md hard rule 7), gap-filling
  stops at the frontier: never suggest or run a search whose results would
  reveal what the user hasn't reached yet.

Finish with a short report (fixed / flagged / suggested), and log it:
`## [YYYY-MM-DD] lint | <scope>` — even a clean pass gets an entry; "nothing
found" is information the next lint's incremental scope depends on. If the lint revealed a recurring workflow
problem, propose a schema amendment — that's how the wiki stops the same rot
from recurring.

## Scale

The index-first navigation pattern works to roughly ~100 sources / hundreds of
pages. Beyond that, or when index-first repeatedly misses relevant pages,
suggest adding search tooling (e.g. `qmd`, a local hybrid-search engine for
markdown with CLI and MCP interfaces — or a simple grep-based script) and
record the choice in the schema. Don't build tooling before the pain exists.
