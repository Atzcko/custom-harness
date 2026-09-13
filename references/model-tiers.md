# Model tiers

The rule: the model matches the altitude of the judgment, not the importance
of the task. Running tests is important; it needs no judgment.

| Tier | Who | Model alias | Judgment involved |
|---|---|---|---|
| 0 | the conductor | the session's model, ideally the newest | talking to the user, deciding what matters |
| 1 | leads, architect, high-stakes reviewer | `opus` | trade-offs, design, anything that shapes other work |
| 2 | specialists, gardener, librarian, researcher | `sonnet` | reading the project and deciding how, within a defined scope |
| 3 | workers | `haiku` | executing a checklist and reporting |

Aliases resolve to the current model of that class, so the harness does not
need updating when a model is replaced. A full model id in an instance note
pins a specific version and is the exception.

## Picking a tier for a task

Ask, in order:

1. Could this be done from a checklist with no reading beyond the files named
   in the prompt? Tier 3.
2. Does it need to understand part of the project and choose an approach, but
   the approach is not contested? Tier 2.
3. Does it change how other work will be done, or weigh options the user
   might disagree about? Tier 1.
4. Does it need the user? Tier 0, meaning you.

When in doubt between two tiers, take the cheaper one and let escalation
correct you. A failed haiku run costs less than an unnecessary opus run, and
the escalation is recorded, so the pattern becomes visible.

## Escalation

- An agent that fails the same task twice stops and returns `ESCALATE:` with
  what it learned. The conductor raises the tier or adds context.
- A lead may run a subtask at its own tier when the subtask turns out to need
  judgment; it notes why in its ledger row.
- The conductor may pin a model for one delegation with the Agent call's
  `model` parameter. Pinning in the instance note is for a standing need.

## Cost hygiene

- Background agents run on tier 2 with a bounded brief. Never tier 1.
- The ledger's `model` column is the cost signal. Once a week, or when the
  numbers in `status` look off, check which agents are running above their
  work.
- Every tier boundary is also a review boundary: what a worker produces is
  checked by the specialist that asked for it, which is why workers can be
  cheap.
