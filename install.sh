#!/usr/bin/env bash
# Install the harness skill for the current user by linking this repository
# into ~/.claude/skills/harness. Re-running is safe.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS="$HOME/.claude/skills"
LINK="$SKILLS/harness"

mkdir -p "$SKILLS"

if [ -L "$LINK" ]; then
  current="$(readlink "$LINK")"
  if [ "$current" = "$HERE" ]; then
    echo "already installed: $LINK -> $HERE"
  else
    echo "relinking: $LINK (was -> $current)"
    ln -sfn "$HERE" "$LINK"
  fi
elif [ -e "$LINK" ]; then
  echo "refusing: $LINK exists and is not a symlink; move it aside first" >&2
  exit 1
else
  ln -s "$HERE" "$LINK"
  echo "installed: $LINK -> $HERE"
fi

command -v python3 >/dev/null || { echo "python3 is required" >&2; exit 1; }
python3 "$HERE/scripts/harness.py" index >/dev/null
if python3 "$HERE/scripts/harness.py" --project "$HERE" lint >/dev/null; then
  echo "library lint: ok"
else
  echo "library lint reported problems; run: python3 scripts/harness.py lint"
fi

if command -v graphify >/dev/null 2>&1; then
  echo "graphify: found"
else
  echo "graphify: not on PATH (the understand phase installs it via the graphify skill when needed)"
fi

echo
echo "Start a new Claude Code session in a project and type /harness."
