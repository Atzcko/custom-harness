# Phase: optimize

The gardener's loop. It runs in the background during `operate` and can be run
on demand. Its purpose is fewer, sharper agents: overlapping ones merge into a
specialist that is very good at one thing, overloaded ones split, unused ones
retire, and drafts that proved themselves move into the library so every
project gets them.

## The risk policy

Changes are automatic by default. The user is asked only when **both** hold:

1. **Altitude.** The agent is high in the chain: tier 0 or 1 (the conductor
   itself is never merged; leads and the architect count as high).
2. **Danger.** At least one of: a `danger:` flag is set, `irreversible: true`,
   the agent is used by two or more projects, or it has a large track record
   (twenty tasks or more) whose memory a merge could blur.

Everything else applies on its own, with three guarantees:

- The originals are archived, never deleted.
- A decision note `H0nn` records what changed and why.
- `undo H0nn` puts it back.

The script decides mechanically so the gardener does not have to argue with
itself:

```bash
harness risk --a tester --b qa-runner
```

`auto` means apply; `ask` means write the proposal and stop.

## One pass

1. **Find candidates.**

   ```bash
   harness overlap
   ```

   Merge candidates are pairs with similar tags, descriptions and tools.
   Split candidates are agents whose charter spans too many areas or whose
   ledger shows unrelated task types. Read the notes before believing the
   numbers; two agents can share vocabulary and still do different jobs.

2. **Decide each candidate** with `risk`. For `auto`:

   ```bash
   harness merge --into firmware-tester --from tester,qa-runner --why "same tools, same tasks, one had the memory"
   ```

   The script archives the sources, scaffolds the merged note with the union
   of tags, tools and skills, keeps the more capable model, carries both
   project-memory sections over, writes the decision note and compiles. Then
   **rewrite the merged charter by hand** so it reads as one agent, not two
   stapled together. Leave the memory sections as they are; they are history.

   For `ask`: write the decision note with the template and `status:
   proposed`, and stop. The conductor presents it.

3. **Promote.** A draft with five or more tasks and at least four in five
   successful is ready:

   ```bash
   harness promote firmware-reviewer
   ```

   Promotion copies the charter to the library, drops the project sections,
   sets the memory scope to portable, and marks the instance as linked. Read
   the promoted charter and remove anything that only makes sense in this
   project; the next project will read it cold.

4. **Retire.** An agent with fewer than three tasks that has not been used in
   sixty days is retired, subject to the same risk policy. Retirement is an
   archive plus a decision note; `undo` brings it back.

5. **Library pass** (`overlap --library`). The same loop over the library,
   which is where cross-project duplicates show up. Library merges affect
   every project that reuses the agent, so `used_in` counts toward danger and
   these are the ones most likely to be `ask`.

6. **Report.** Return the list of decision ids written and which are
   `proposed`. Nothing else; the conductor reads the notes.

## What the gardener does not do

- It does not run git in the project or in the library.
- It does not edit charters of agents it did not merge, split or promote.
- It does not change tiers or models; it writes that in `harness/evolution.md`
  for the conductor, because model choice is a cost decision the user owns.
