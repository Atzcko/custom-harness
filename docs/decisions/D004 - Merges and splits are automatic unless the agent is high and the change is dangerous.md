---
title: D004 - Merges and splits are automatic unless the agent is high and the change is dangerous
type: decision
status: accepted
date: 2026-09-13
tags:
  - decision
  - policy
---

# D004 — Merges and splits are automatic unless the agent is high and the change is dangerous

## Context

The first design proposed that the gardener only proposes and the owner
approves every merge. The owner rejected that: merges and splits must happen
on their own, and the owner is involved only when the agent is high up the
chain and there is real potential for harm.

## Decision

`harness.py risk` decides mechanically. The user is asked only when both hold:
the agent's tier is 0 or 1, and at least one danger signal is present (a
`danger:` flag, `irreversible: true`, use by two or more projects, or a track
record of twenty tasks or more). Tier 0 is never merged. Everything else is
applied automatically with an archive, a decision note and an `undo` path.

## Consequences

The gardener can change the roster without the owner noticing until they read
`status`. The decision notes and the index table in `harness/Harness.md` are
therefore not optional; they are the audit trail. Danger flags must be set
honestly during the architect phase, from the brief's "must never happen
automatically" list, or the policy has nothing to protect.

## Related

- [[D006 - Agents never run git; archives and decision notes make changes reversible]]
