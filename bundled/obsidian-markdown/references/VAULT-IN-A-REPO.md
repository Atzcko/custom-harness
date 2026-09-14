# A vault that is also a source repository

When the vault root *is* the project root — the notes sit beside `src/`, and
both are in the same git repo — four things go wrong that never go wrong in a
notes-only vault. All four are cheap to prevent and expensive to discover.

## 1. Exclude the build tree, or it becomes most of your vault

Obsidian indexes every `.md` under the vault root. Dependency and build
directories are full of them: vendored library READMEs, `CHANGELOG.md`,
`node_modules`. They show up in search, in the graph, and — worst — in wikilink
autocomplete, where a stray `[[README]]` can silently resolve into a dependency.

Check before anything else:

```bash
find . -name "*.md" -not -path "./.pio/*" | wc -l    # your notes
find .pio -name "*.md" | wc -l                        # the noise
```

If the second number is comparable to the first, fix it. Obsidian's *Excluded
files* setting lives in `.obsidian/app.json` under `userIgnoreFilters`, and the
file may not exist yet — Obsidian only writes it once you change a setting:

```json
{
  "userIgnoreFilters": [".pio/", "node_modules/", ".git/"],
  "alwaysUpdateLinks": true,
  "newLinkFormat": "shortest",
  "useMarkdownLinks": false
}
```

Paths are relative to the vault root and need the trailing slash. Commit
`app.json`; gitignore `.obsidian/workspace.json` and `workspace-mobile.json`,
which are per-machine window layout and churn on every open.

## 2. Wikilinks only work in one of the two places the file is read

`[[D026 - Apps are a platform]]` renders as a link in Obsidian and as the
literal characters `[[D026 - Apps are a platform]]` on GitHub, in a code host's
file preview, and in any other Markdown renderer.

Decide per file, by who reads it where:

| File | Use |
|---|---|
| Notes under `docs/`, read in Obsidian | `[[wikilinks]]` |
| `README.md`, read on the forge | `[relative](docs/decisions/D026%20-%20Apps.md)` |
| `CLAUDE.md`, `AGENTS.md` — read by an agent, in the repo | either; wikilinks are fine and shorter |

Relative Markdown links need `%20` for spaces. Wikilinks do not, which is one
reason vaults tolerate spaces in filenames that a repo otherwise would not.

## 3. A wikilink inside source code will rot silently

Obsidian's rename-updates-links only rewrites files it manages: Markdown.
Rename a note and every `[[Old Title]]` in a `.cpp`, `.py` or `.ts` comment is
left pointing at nothing, with no warning and no broken-link report — the file
is invisible to the vault.

**In non-Markdown files, reference the stable ID only:**

```cpp
/* The host owns the app screen lifetime. See D026. */   // survives a rename
/* ... See [[D026 - Apps are a platform]]. */            // rots silently
```

This is the main reason to give notes a short immutable ID in the filename.

## 4. Editing notes with scripts needs assertions

Bulk edits to notes — inserting a release entry, updating an index table — are
naturally done with `sed` or a small Python script. A pattern that does not
match fails **silently**: `str.replace` returns the string unchanged, `sed`
exits 0, and you learn about it much later from the rendered output.

Assert the match count, and abort:

```python
def patch(path, old, new, n=1):
    s = open(path, encoding="utf-8").read()
    assert s.count(old) == n, "%s: %d matches, want %d" % (path, s.count(old), n)
    open(path, "w", encoding="utf-8").write(s.replace(old, new, n))
```

Two extra hazards specific to notes:

- **Frontmatter is YAML.** A regex that rewrites a title can break the document
  by introducing an unquoted `:` or `#`. Prefer matching the whole block.
- **Newest-first vs append-only.** Decide once per file and write it down. An
  index or a release log usually reads newest-first, so new entries are
  *inserted above an anchor*; a chronological log is append-only. Mixing them
  in one repo produces entries in the wrong place, which nobody notices.

## 5. Vault hygiene that pays for itself

- **Absolute dates.** "last Tuesday" in a note is unreadable in six months, and
  the file mtime is not the event date once the file is copied or synced.
- **Frontmatter `type:`** (`decision`, `stage`, `index`, `reference`) is what
  makes the vault filterable later without touching a single note.
- **One hand-maintained `index.md`** beats a Dataview or Bases query when the
  vault is small and read by people and agents who may not have the plugin.
  The manual table is also a link-integrity check: broken entries are visible.
