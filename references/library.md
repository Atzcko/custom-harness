# The library

`library/agents/` is the shared pool of agents. It lives inside the skill so it
is versioned with it and available to every project the moment the skill is
installed. `library/INDEX.md` is the catalogue the architect reads;
`library/LESSONS.md` is the skill's own portable memory.

## A library agent

One note per agent, from `templates/agent.md`. The frontmatter is what the
script reads; the body is the charter the compiled agent carries.

| Field | Meaning |
|---|---|
| `name` | the identifier; lowercase, hyphens; also the compiled agent's name |
| `title` | the human name |
| `version` | bumped on every charter change; projects recompile on drift |
| `tier`, `model` | altitude and default model alias |
| `description` | written for matching and for delegation; says what the agent does and when to use it |
| `tags` | the matching vocabulary; five to eight, specific |
| `skills` | skills preloaded into the agent at start |
| `tools` | tool allowlist; empty inherits everything |
| `spawns` | child agents it may create; `*` for any |
| `danger`, `irreversible` | risk flags read by the policy |
| `status` | `seed`, `draft`, `proven`, `retired` |
| `origin`, `created`, `updated` | provenance |
| `used_in`, `tasks`, `successes`, `last_used` | track record, maintained by the ledger |

## Matching

`match` scores a role description against every library agent: overlap of
description words, overlap of tags, and a bonus for a track record. The bands
in `architect.md` turn the score into reuse, adapt or create. The score is
there to shortlist; the architect reads the shortlisted charters and decides.

Write descriptions for matching: the job, the inputs, the outputs, and the
words a future architect would use when looking for this. A description that
only makes sense inside its birth project will never be found.

## Versioning

- A charter change bumps `version` and `updated`.
- Instance notes record `library_version`; `status` reports drift; `compile`
  refreshes the charter and keeps project memory.
- Track-record fields are not versioned changes; the ledger updates them in
  place.

## Promotion

A project draft becomes a library agent when it has done five or more tasks
with four in five successful, or when the user says so. `promote` does the
mechanics; the gardener or conductor then reads the charter and removes what
only made sense in the birth project. Promoted agents start as `proven` if
they met the numbers, `draft` otherwise.

## Archive

`library/archive/` keeps retired and merged agents with their full note and a
pointer to the decision that moved them. Nothing in the library is ever
deleted, so a merge that turned out wrong can be undone and a retired agent
can be brought back when a project needs it again.

## Seeds

The library ships with the harness's own staff (architect, gardener, librarian,
scribe) and six general workers and specialists. They are deliberately
generic; the first real project adapts them with overlays, and what the
overlays keep repeating is what the gardener eventually folds into the
charters.
