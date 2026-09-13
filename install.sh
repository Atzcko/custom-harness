#!/usr/bin/env bash
# Install the harness skill for the current user.
#
# - links this repository into every skills folder that exists
#   (~/.agents/skills is the cross-tool standard; ~/.claude, ~/.codex and
#   ~/.gemini are per-tool), creating ~/.agents/skills and ~/.claude/skills
#   when absent
# - links the bundled llm-wiki into the same folders when no llm-wiki is installed
# - writes a `harness` launcher to ~/.local/bin so prompts and playbooks need
#   no tool-specific path
#
# Re-running is safe.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

link_into() {  # link_into <skills-root> <name> <source>
  local root="$1" name="$2" src="$3" link
  link="$root/$name"
  mkdir -p "$root"
  if [ -L "$link" ]; then
    if [ "$(readlink "$link")" = "$src" ]; then
      echo "  ok        $link"
    else
      ln -sfn "$src" "$link"
      echo "  relinked  $link"
    fi
  elif [ -e "$link" ]; then
    echo "  kept      $link (real directory, not a link; left alone)"
  else
    ln -s "$src" "$link"
    echo "  linked    $link"
  fi
}

echo "harness install"

# skills roots: always ~/.agents/skills and ~/.claude/skills; the others only if the tool is present
ROOTS=("$HOME/.agents/skills" "$HOME/.claude/skills")
[ -d "$HOME/.codex" ] && ROOTS+=("$HOME/.codex/skills")
[ -d "$HOME/.gemini" ] && ROOTS+=("$HOME/.gemini/skills")

echo "skill:"
for root in "${ROOTS[@]}"; do
  link_into "$root" harness "$HERE"
done

# bundled llm-wiki, only where no llm-wiki exists at all. A real folder or a
# link to somewhere else (for example the owner's skills repository) counts as
# installed; only our own bundled link does not.
have_wiki=""
for root in "$HOME/.agents/skills" "$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.gemini/skills"; do
  if [ -f "$root/llm-wiki/SKILL.md" ]; then
    if [ -L "$root/llm-wiki" ] && [ "$(readlink "$root/llm-wiki")" = "$HERE/bundled/llm-wiki" ]; then
      continue
    fi
    have_wiki="$root/llm-wiki"
  fi
done
if [ -n "$have_wiki" ]; then
  echo "llm-wiki: installed at $have_wiki (bundled copy at bundled/llm-wiki stays as fallback)"
else
  echo "llm-wiki: not installed; linking the bundled copy"
  for root in "${ROOTS[@]}"; do
    link_into "$root" llm-wiki "$HERE/bundled/llm-wiki"
  done
fi

# launcher
BIN="$HOME/.local/bin"
mkdir -p "$BIN"
cat > "$BIN/harness" <<EOF
#!/usr/bin/env bash
exec python3 "$HERE/scripts/harness.py" "\$@"
EOF
chmod +x "$BIN/harness"
echo "launcher: $BIN/harness"
case ":$PATH:" in
  *":$BIN:"*) ;;
  *) echo "  note: $BIN is not on your PATH; add it, or prompts fall back to the python path" ;;
esac

command -v python3 >/dev/null || { echo "python3 is required" >&2; exit 1; }
python3 "$HERE/scripts/harness.py" index >/dev/null
echo
python3 "$HERE/scripts/harness.py" --project "$HERE" doctor || true
echo
echo "Start a new session in a project (Claude Code, Codex, Gemini CLI) and invoke the harness skill."
