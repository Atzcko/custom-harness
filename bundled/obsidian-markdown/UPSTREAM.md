# Upstream

- **Skill:** obsidian-markdown
- **Origin:** https://github.com/kepano/obsidian-skills (`skills/obsidian-markdown`), MIT licence (see `LICENSE`)
- **Bundled:** 2026-09-14, from the owner's skills repository (`Atzcko/skills`, `skills/obsidian-markdown`)
- **Local changes against upstream:** two references written for a vault that shares a directory with source code, `references/VAULT-IN-A-REPO.md` and `references/DECISION-RECORDS.md`, and the SKILL.md workflow section that points at them. The harness's own templates follow those two references.
- **Role in the harness:** a fallback. The installer links it into the tool folders only where no obsidian-markdown is installed; `harness doctor` reports which copy is in use and whether the bundled one differs from an installed one.

Update by taking the upstream version, re-applying the two references and the workflow paragraph, and changing the date above.
