# Maintaining agent-charter

- **Bump the version on every content change.** Each plugin's `.claude-plugin/plugin.json` pins `version`. Installed users stay on their cached copy until that string changes, so a change without a bump never reaches them.
- **Validate before pushing:** `claude plugin validate --strict .` and `claude plugin validate --strict plugins/<name>`.
- **Refresh committed copies.** A repository that commits a copy of a skill or agent for cloud sessions needs that copy refreshed after a change here. Name this repository's commit in that PR.
