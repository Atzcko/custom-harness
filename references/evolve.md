# Phase: evolve

The skill improves itself from what its own use teaches it. Two inputs, one
loop, a version bump at the end.

## Inputs

- `harness/evolution.md` in each project: lines written by the conductor and
  by agents when the harness got in their way or could have helped more.
- `library/LESSONS.md` in the skill: the same lines, collected across projects,
  each with its origin and date, and a `processed` mark once acted on.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/harness.py" lessons collect
```

moves new lines from the project into the library without duplicates.

## The loop

1. Read the unprocessed lessons. Group them: playbook gaps, template gaps,
   script bugs, policy problems, things that are not the skill's fault.
2. For each group, decide the smallest change that would have prevented the
   lesson. Explain why in one sentence; that sentence goes in the changelog.
3. Apply by risk level:

   | Change | Policy |
   |---|---|
   | `references/`, `templates/`, library charters | apply, patch bump |
   | `scripts/harness.py` | apply, run `lint` on a fixture project, patch or minor bump |
   | `SKILL.md` body | apply, run the skill-creator validator, minor bump |
   | `SKILL.md` description, the risk policy, the memory protocol | propose to the user first; these change what the skill does for every project |

4. Mark the lessons processed, with the version that addressed them.
5. Bump `VERSION`, add the entry to `CHANGELOG.md` with the reasons, add a
   line to `docs/log.md`. If the change reverses an earlier decision, write a
   new decision note in `docs/decisions/` that supersedes it; do not edit the
   old one.

## Validation

Before a minor bump, run the skill-creator validator against the skill root
and fix what it reports. It needs PyYAML, which the system Python lacks, so
run it through `uv`:

```bash
uv run --with pyyaml python "$HOME/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py" "${CLAUDE_SKILL_DIR}"
```

For changes to the playbooks, the evals in `evals/evals.json` are the
regression suite. The skill-creator skill runs them with and without the
skill and shows a benchmark; run it when the change is large enough that a
regression would be expensive, not for every wording fix.

## What not to evolve away

The standing rules in `SKILL.md` section 2 came from failures. A lesson that
says "the ledger is tedious" is a reason to make the ledger easier, not to
drop it. When a lesson argues against a standing rule, write the argument in
a decision note and let the user decide.
