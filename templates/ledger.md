---
title: Ledger
type: log
project: {{project}}
---

# Ledger — {{project}}

Append-only. One row per delegated task. `outcome` is `ok`, `partial` (the
agent escalated) or `fail`. `tokens` when known. Rows are added with
`harness.py ledger add`, which also updates the agent's track record.

| date | agent | model | task | outcome | tokens | note |
|---|---|---|---|---|---|---|
