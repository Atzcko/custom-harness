---
title: D011 - A scheduled job watches the model pages; new ids open a pull request
type: decision
status: accepted
date: 2026-09-13
tags:
  - decision
  - policy
---

# D011 — A scheduled job watches the model pages; new ids open a pull request

## Context

D008 made the registry the single place where tiers meet models, and asked
the conductor to refresh it when `models check` says it is stale. That still
depends on someone opening a session. The owner asked for the check to happen
periodically and for the files to be updated without waiting for a session.

Two kinds of change hide in "update the files". Whether the pages still list
the same models is a fact a script can verify. Which tier a newly released
model belongs to is a judgment: the newest Gemini is a Flash, Anthropic says
to start on Opus and escalate to Fable, OpenAI's mini tier is called Terra.

## Decision

`harness models watch` fetches the three official model pages, extracts the
model ids, and compares them with `library/models-seen.json`. A GitHub
Actions workflow runs it every Monday:

- **Unchanged pages**: the snapshot and the registry's `checked` date are
  committed to `main`, so `models check` stays green in every project.
- **New ids that could change a tier**: a pull request with the report,
  listing the ids and the current mapping. The owner, or the researcher
  agent given the brief in `references/models.md`, decides the mapping and
  records it with `models set`, which keeps the source URL.
- **A page unreachable**: the job fails and nothing is assumed.

Ids that are modality variants (image, audio, live, embeddings, and so on)
are recorded but never open a pull request on their own.

## Consequences

The registry can be verified without a person for as long as the pages keep
their shape; when a page changes layout and the extractor finds nothing, the
job fails loudly rather than silently reporting "unchanged". A new model
still needs a human or an agent to place it, which is the part that should
not be automatic. Locally, `harness models watch` gives the conductor the same
answer at session start before it spends a researcher on a refresh.

## Related

- [[D008 - A dated model registry decides which model each tier runs]]
