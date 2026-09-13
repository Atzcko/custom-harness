---
name: {{name}}
title: {{title}}
type: agent
version: 1
tier: {{tier}}
model: {{model}}
description: {{description}}
tags: [{{tags}}]
skills: []
tools: []
spawns: []
background: false
memory: user
danger: []
irreversible: false
status: draft
origin: {{project}}
created: {{date}}
updated: {{date}}
used_in: []
tasks: 0
successes: 0
last_used:
---

# {{title}}

## Charter

You are the {{title}}. Write here, in the second person, what this agent does,
how it approaches the work, and what a good result looks like. Keep it to what
would be true in any project; project facts belong in the instance note.

## Inputs and outputs

What the agent expects to be given, and the shape of what it returns.

## How you judge done

The checks the agent runs before it reports success.

## Boundaries

What it does not do, and when it stops and returns `ESCALATE:` instead.
