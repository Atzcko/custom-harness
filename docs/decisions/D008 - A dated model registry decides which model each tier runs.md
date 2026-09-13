---
title: D008 - A dated model registry decides which model each tier runs
type: decision
status: accepted
date: 2026-09-13
tags:
  - decision
  - policy
---

# D008 — A dated model registry decides which model each tier runs

## Context

Agents used to name their model directly (`model: sonnet`). That ties every
charter to one vendor's aliases, and it goes stale the day a new model ships.
The owner wants the harness to know the latest models and keep moving agents
onto them.

## Decision

Agents declare a **tier** (0 to 3). `library/models.json` maps each tier to a
concrete model per provider, with the date it was checked and the source
page. `compile` resolves the model through the registry for the target tool;
an explicit `model:` on an instance or library note is a pin and wins.

`harness models check` reports when the registry is older than its maximum
age (fourteen days by default). At session start the conductor sends the
researcher to the providers' model pages, records what changed with
`harness models set`, and recompiles. Where a provider offers aliases that
always point at the newest of a class, the registry uses those, so an upgrade
can happen without a refresh.

## Consequences

Every agent in every project moves to a new model with one registry change
and a recompile, which is what the owner asked for. It also means a bad
registry entry moves every agent at once; `models set` records the source so
the change can be argued with, and the ledger's model column shows what
actually ran.

## Related

- [[D007 - The core is tool-neutral; each coding agent gets an adapter]]
