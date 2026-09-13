# Models

Agents declare a tier. The registry decides the model. That is the whole
policy, and it exists so that a new model reaches every agent in every project
with one change.

## The registry

`library/models.json`:

```json
{
  "checked": "2026-09-13",
  "max_age_days": 14,
  "targets": {"claude": "anthropic", "codex": "openai", "gemini": "google", "generic": "anthropic"},
  "providers": {
    "anthropic": {
      "source": "https://docs.claude.com/en/docs/about-claude/models",
      "tiers": {"0": "fable", "1": "opus", "2": "sonnet", "3": "haiku"},
      "notes": "Claude Code aliases resolve to the newest model of each class."
    }
  }
}
```

- `tiers` maps 0 to 3 to the model id the target tool accepts. Prefer an alias
  that tracks the newest of a class when the provider has one; otherwise the
  exact id, and expect to update it.
- `checked` is the date a person or the researcher last verified the mapping
  against the provider's model page. `harness models check` compares it with
  `max_age_days`.

## Resolution order at compile time

1. `model:` on the instance note, a pin for this project.
2. `model:` on the library charter, a pin for this agent everywhere.
3. The registry entry for the target's provider and the agent's tier.

Pins are exceptions and should say why in the note. A pin on a library
charter is the only way a charter names a vendor; use it for an agent that
genuinely needs one model, not for a preference.

## Refresh

At session start the conductor runs:

```bash
harness models check
```

If it reports the registry as stale, delegate to the **researcher** with this
brief and nothing more:

> Read the official model pages for Anthropic, OpenAI and Google (the URLs
> are in `library/models.json`). For each provider, list the current model
> ids with release dates and which is the most capable, the strong mid-range,
> the cost-effective one, and the cheapest. Propose the tier mapping. Report
> only what the pages say; mark anything not on the page as not verified.

Apply the result with `harness models set --provider openai --tier 1 --model
<id> --source <url>`, one line per change, then `harness models touch` and
`harness compile`. Note the change in `harness/evolution.md` so the ledger's
model column can be read against it later.

Local evidence beats the web when a tool ships a model list: Codex keeps
`~/.codex/models_cache.json`, and Claude Code's `/model` picker shows what the
session can use. `harness models show --local` prints what it can find.

## Tiers, restated

| Tier | Meaning | What to pick |
|---|---|---|
| 0 | the conductor and anything that talks to the owner | the newest, most capable model the tool offers |
| 1 | leads, architect, high-stakes review | the strongest reasoning model below the frontier, or the frontier if cost allows |
| 2 | specialists, gardener, librarian, researcher | the cost-effective model that still reads a project well |
| 3 | workers | the cheapest model that follows a checklist reliably |

When a provider's lineup has fewer classes than tiers, two tiers share a model.
When it has more, pick by the meaning above, not by name.
