#!/usr/bin/env python3
"""List every agent skill installed on this machine, one line each.

Scans the folders the coding agents read (Claude Code, Codex, Gemini CLI,
Cursor, OpenCode, the shared ~/.agents/skills), the current project's
.claude/skills and .agents/skills, and Claude Code plugins. Symlinks are
resolved, so a skill linked into five tools is listed once.

Each skill is tagged with who owns it, because that decides how it may be
changed:

  own     inside a git repository, not under vendor/  -> edit in place
  adapted own, but derived from upstream (UPSTREAM.md) -> edit; merge upstream by hand
  vendor  under a repository's vendor/                 -> do not edit
  plugin  shipped by a Claude Code plugin              -> do not edit
  local   a plain folder, no repository                -> edit, but unversioned

  inventory.py                       table of every skill
  inventory.py --query "pdf form"    same, ranked by overlap with the words
  inventory.py --json                machine-readable, with full descriptions
  inventory.py --show NAME           print that skill's SKILL.md

Standard library only.
"""

import argparse
import json
import re
import sys
from pathlib import Path

HOME = Path.home()
TOOL_ROOTS = [
    HOME / ".claude/skills",
    HOME / ".agents/skills",
    HOME / ".codex/skills",
    HOME / ".gemini/skills",
    HOME / ".cursor/skills",
    HOME / ".config/opencode/skills",
]
STOP = set("a an and or the to of for in on with by is are be this that it as at from use when user "
           "any not do does your you i me my we our can will should into via also".split())


def frontmatter(text: str) -> dict:
    """Parse the top-level scalar keys of a YAML frontmatter block, including
    folded (>) and literal (|) multi-line values."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    out, key, buf = {}, None, []
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", line)
        if m:
            if key:
                out[key] = " ".join(buf).strip()
            key, val = m.group(1), m.group(2).strip()
            buf = [] if val in (">", "|", ">-", "|-", "") else [val.strip('"').strip("'")]
        elif key and line.startswith((" ", "\t")):
            buf.append(line.strip())
    if key:
        out[key] = " ".join(buf).strip()
    return out


def git_root(p: Path):
    for d in [p, *p.parents]:
        if (d / ".git").exists():
            return d
    return None


def project_roots() -> list:
    cwd = Path.cwd()
    stop = git_root(cwd) or cwd
    roots = []
    for d in [cwd, *cwd.parents]:
        roots += [d / ".claude/skills", d / ".agents/skills"]
        if d == stop or d == HOME:
            break
    return roots


def plugin_roots() -> list:
    """(skills folder, plugin name) for every installed Claude Code plugin."""
    f = HOME / ".claude/plugins/installed_plugins.json"
    try:
        data = json.loads(f.read_text())
    except (OSError, ValueError):
        return []
    out = []
    for name, installs in (data.get("plugins") or {}).items():
        for inst in installs or []:
            p = inst.get("installPath")
            if p:
                out.append((Path(p) / "skills", name.split("@")[0]))
    return out


def classify(real: Path):
    root = git_root(real)
    if real.parent.name == "vendor":
        return "vendor", root
    if not root:
        return "local", None
    return ("adapted" if (real / "UPSTREAM.md").exists() else "own"), root


def collect() -> list:
    seen, skills = set(), []

    def add(skill_dir: Path, where: str, plugin=None):
        md = skill_dir / "SKILL.md"
        if not md.is_file():
            return
        real = skill_dir.resolve()
        if real in seen:
            for s in skills:
                if s["path"] == str(real) and where not in s["seen_in"]:
                    s["seen_in"].append(where)
            return
        seen.add(real)
        fm = frontmatter(md.read_text(encoding="utf-8", errors="ignore"))
        kind, repo = ("plugin", None) if plugin else classify(real)
        skills.append({
            "name": (f"{plugin}:" if plugin else "") + (fm.get("name") or skill_dir.name),
            "owner": kind,
            "description": fm.get("description", ""),
            "path": str(real),
            "repo": str(repo) if repo else None,
            "seen_in": [where],
        })

    for root in project_roots():
        if root.is_dir():
            for d in sorted(root.iterdir()):
                add(d, "project")
    for root in TOOL_ROOTS:
        if root.is_dir():
            label = str(root).replace(str(HOME), "~")
            for d in sorted(root.iterdir()):
                if not d.name.startswith("."):
                    add(d, label)
    for root, plugin in plugin_roots():
        if root.is_dir():
            for d in sorted(root.iterdir()):
                add(d, "plugin", plugin=plugin)
    return skills


def stem(w: str) -> str:
    for suf in ("ing", "ies", "es", "s", "ed"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


def words(s: str) -> set:
    return {stem(w) for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 2 and w not in STOP}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--query", help="rank skills by word overlap with this text")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--show", metavar="NAME", help="print one skill's SKILL.md")
    ap.add_argument("--width", type=int, default=110, help="description width in the table")
    a = ap.parse_args()

    skills = collect()

    if a.show:
        hits = [s for s in skills if s["name"] == a.show or s["name"].split(":")[-1] == a.show]
        if not hits:
            print(f"no skill named {a.show}", file=sys.stderr)
            return 1
        s = hits[0]
        print(f"# {s['name']}  [{s['owner']}]  {s['path']}\n")
        print(Path(s["path"], "SKILL.md").read_text(encoding="utf-8", errors="ignore"))
        return 0

    if a.query:
        q = words(a.query)
        for s in skills:
            name_w = words(s["name"].replace("-", " "))
            s["score"] = 3 * len(q & name_w) + len(q & words(s["description"]))
        skills = sorted((s for s in skills if s["score"] > 0), key=lambda s: -s["score"])

    if a.json:
        json.dump(skills, sys.stdout, indent=2)
        print()
        return 0

    repos = sorted({s["repo"] for s in skills if s["repo"]})
    for s in skills:
        d = s["description"]
        d = d if len(d) <= a.width else d[: a.width - 1] + "…"
        score = f"{s['score']:>3} " if a.query else ""
        print(f"{score}{s['name']:<34} {s['owner']:<7}  {d}")
    print(f"\n{len(skills)} skill(s)" + (" matching" if a.query else "") +
          (f"; repositories: {', '.join(repos)}" if repos else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
