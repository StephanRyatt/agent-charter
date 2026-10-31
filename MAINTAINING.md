# Maintaining agent-charter

- **Bump the version on every content change.** Each plugin's `.claude-plugin/plugin.json` pins `version`. Installed users stay on their cached copy until that string changes, so a change without a bump never reaches them.
- **Validate before pushing:** `claude plugin validate --strict .` and `claude plugin validate --strict plugins/<name>`.
- **Sync claude.ai after merging.** Installs through claude.ai don't reliably pick up a push to `main` on their own, even with the marketplace's auto-sync on. After merging, trigger the sync for the `agent-charter` marketplace on claude.ai (Customize → Plugins). Claude Code then downloads the new version the next time it starts. In a session that is already open, run `/reload-plugins`.
- **No committed copies.** Cloud sessions get the plugins from the claude.ai account (README, "Using these in Claude Code cloud sessions"), so the claude.ai sync above also updates them. Don't copy skills or agents into other repositories.

## Writing skill copy

A user picks a skill from a few words in a menu. Every level of copy answers the same two questions, at a different length: **what does this do for me**, and **when do I pick it over its neighbors**. Write the shortest level first. Each longer level opens with it, word for word, so the same phrase is recognized everywhere.

| Level | Where it shows | Reader | Length | What it carries |
|---|---|---|---|---|
| Name | The `/` menu and commands | User | 1–3 words | The job, as a noun. Keep it stable: other repositories call skills by name. |
| Lead | The start of `description`, so the first words in the `/` menu and on hover | User and model | ≤ 60 characters | The outcome, as an imperative verb, plus the discriminator that separates it from its neighbors. |
| `description` | Hover, plugin screens, the model's skill listing | User and model | ≤ 250 characters, 2–3 short sentences | The lead, what you get back, and who makes the call or whether anything is built. |
| `when_to_use` | The model's skill listing only | Model | ≤ 700 characters | The phrases users say, who may start it, and "Not for X (use Y)" for each close neighbor. |
| `argument-hint` | After the name, in autocomplete | User | ≤ 40 characters, in `[brackets]` | What to type after the command. |
| Plugin `description` (`plugin.json`, `marketplace.json`) | Plugin browser | User | ≤ 400 characters | One line on the plugin, then each skill's name and lead. |
| README rows | GitHub | User | 1–3 sentences | The lead in bold, then how it works and what you get, in plain words. |
| `SKILL.md` opening | The model, maintainers | Model | One short paragraph and a neighbor list | The lead and the value, then when to use each neighbor instead. |

Rules:

- **Outcome before mechanism.** "Stress-test a costly decision before you commit", not "Convene a council of specialists". The mechanism comes after the lead.
- **One discriminator vocabulary across the set,** so a user learns it once:
  - *before you commit, you decide:* decision-council;
  - *then build the best, it decides:* best-of-n;
  - *one plan:* risk-evaluation;
  - *one hard question:* ask-specialist;
  - *finished work, is it correct:* fresh-eyes. Risk-evaluation asks what could happen even if the work is correct.
- **Plain words on the short levels.** Say "independent", not "fresh context", "lens", "bounded" or "first principles". The body can use the precise terms.
- **"You" always means the user.** Use it on user-facing levels, but never for the agent's own work: write "made in this session", not "yours". Restate who decides in `when_to_use` in the third person ("the user makes the call"), because the model reads `description` too.
- **Each trigger phrase belongs to one skill across the whole marketplace,** other plugins included. An exclusion names the skill that owns the case, and close neighbors exclude each other in both directions.
- **No angle brackets** in `description` or `when_to_use`: they display as `&lt;` and `&gt;`. Use `[brackets]`.
- **Budget:** `description` and `when_to_use` together stay well under the 1,536-character cap of the skill listing.
- **Where the fields work:** `when_to_use` and `argument-hint` are Claude Code fields, as are `model`, `effort` and `context`. This marketplace uses them in plugin skills; `claude plugin validate --strict` accepts them, and plugin installs through claude.ai load them. A standalone claude.ai skill upload rejects them, so strip them from any copy made for that path.
