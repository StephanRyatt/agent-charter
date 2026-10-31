#!/bin/bash
# Install agent-charter plugins in a Claude Code cloud environment, before Claude Code starts.
# From the environment's setup script (README, "Using these in Claude Code cloud sessions"):
#   curl -fsSL https://raw.githubusercontent.com/StephanRyatt/agent-charter/main/cloud/install-plugins.sh | bash -s review council || true
# Never fails the setup: a plugin it can't install is linked from a clone instead, and if that
# fails too, ~/.claude/CLAUDE.md says so, so the session reports it rather than running without it.

set -u
REPO=StephanRyatt/agent-charter
MARKETPLACE=agent-charter
CLONE=${AGENT_CHARTER_CLONE:-/opt/agent-charter}

if [ $# -eq 0 ]; then
  echo "usage: install-plugins.sh PLUGIN..." >&2
  exit 0
fi

failed=()
if command -v claude >/dev/null; then
  # Cloud routines set SKIP_PLUGIN_MARKETPLACE=true, which blocks installs unless overridden per command.
  SKIP_PLUGIN_MARKETPLACE=false claude plugin marketplace add "$REPO" ||
    SKIP_PLUGIN_MARKETPLACE=false claude plugin marketplace update "$MARKETPLACE"
  for plugin in "$@"; do
    SKIP_PLUGIN_MARKETPLACE=false claude plugin install "$plugin@$MARKETPLACE" || failed+=("$plugin")
  done
else
  echo "claude is not on PATH; linking the plugins instead" >&2
  failed=("$@")
fi

if [ ${#failed[@]} -gt 0 ]; then
  # A plugin folder under ~/.claude/skills/ loads as <name>@skills-dir, with no install and no trust check.
  missing=()
  rm -rf "$CLONE"
  if git clone -q --depth 1 "https://github.com/$REPO" "$CLONE"; then
    mkdir -p "$HOME/.claude/skills"
    for plugin in "${failed[@]}"; do
      if [ -f "$CLONE/plugins/$plugin/.claude-plugin/plugin.json" ]; then
        ln -sfn "$CLONE/plugins/$plugin" "$HOME/.claude/skills/$plugin"
        echo "linked $plugin into ~/.claude/skills"
      else
        missing+=("$plugin")
      fi
    done
  else
    missing=("${failed[@]}")
  fi
  if [ ${#missing[@]} -gt 0 ]; then
    mkdir -p "$HOME/.claude"
    printf '\nThis cloud environment could not install the agent-charter plugins %s (setup script, %s). Tell the user at the start of the session.\n' \
      "${missing[*]}" "$(date -u +%F)" >> "$HOME/.claude/CLAUDE.md"
    echo "could not install: ${missing[*]}" >&2
  fi
fi
exit 0
