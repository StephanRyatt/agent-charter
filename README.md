# agent-charter

**Build from the spec. Check against the source.**

A charter is the founding document that grants authority and sets scope. This repository is the charter my AI agents work under: plugins that keep agent work tied to its governing sources, and that get it checked by fresh eyes before it ships.

It is a [Claude Code](https://code.claude.com) plugin marketplace. The skills follow the open Agent Skills format.

## Plugins

| Plugin | What it does | Command |
|---|---|---|
| `review` | **Get an independent check that finished work is correct.** Code against its spec, a plan, a decision, a document or filing, yours or someone else's. The reviewer judges it from the governing sources with a checklist suited to each kind of work. Pick report-only or fix mode, and standard or deep scrutiny. | `/review:fresh-eyes` |
| `council` | **Stress-test a costly decision before you commit.** Three to five independent specialists weigh the options, each from a different angle, and you get a recommendation with its tradeoffs, what it turns on, and the strongest dissent. You make the call; nothing is built. | `/council:decision-council` |
| | **Compare n approaches to a problem, then build the best.** Distinct solutions are drafted independently: by one agent, or by several in parallel for open-ended problems. The winner is picked on criteria set up front, measured by tests where they can tell it apart, then built. It makes the call; you review the result. n, the model (Opus by default) and the effort scale with the stakes. | `/council:best-of-n` |
| | **See what could go wrong with one plan, how likely, how bad.** For a plan, change, launch, filing or situation: what could happen, not whether the work is correct. The top risks ranked on one page, with honest numbers and their basis, how reversible each is, and the one action that cuts the most risk. | `/council:risk-evaluation` |
| | **Get an independent, deep answer to one hard question,** such as whether a formula, algorithm or rule holds. A reasoning specialist works it out from your sources, and its answer is checked before you get it. | `/council:ask-specialist` (agent `council:reasoning-specialist`) |
| `figma-workflow` | Governance for Figma to frontend, on top of Figma's own tooling. Plans a screen from its Figma frame, new or changed, with a mapping to the repo's own tokens and components, and says so when nothing changed. Works on server-rendered apps (Razor, jQuery, Bootstrap) and component stacks (React, Vue, Next.js) through stack adapters. Repository facts live in the repo's `docs/figma-workflow/`. | `/figma-workflow:sync` |
| | Builds the approved plan in the same chat as a clickable prototype with no backend: real navigation, in-memory state, every control working or listed as inert. Typing it is the approval. | `/figma-workflow:build` |
| | An independent audit of the result against the design: coverage, fidelity, behaviour, design-system reuse, with a to-do list for the designer. | `/figma-workflow:verify` |

Planned: `spec`, which covers deciding, planning, implementing with acceptance proofs, and review. It is published once its planning step has run end to end on real work.

## Which one?

Pick by what you have in hand and who makes the call:

| You have | Use | What it does for you |
|---|---|---|
| A costly call that is yours to make, with or without options | `/council:decision-council` | Stress-test a costly decision before you commit. You decide. |
| A problem you're happy to hand over | `/council:best-of-n` | Compare n approaches to a problem, then build the best. It decides. |
| One plan, change, launch or situation | `/council:risk-evaluation` | See what could go wrong with one plan, how likely, how bad. |
| One hard question with a definite answer | `/council:ask-specialist` | Get an independent, deep answer to one hard question. |
| Finished work, including a plan or a decision already made | `/review:fresh-eyes` | Get an independent check that finished work is correct (a red team included). |

For a low-stakes or easily reversed question, just ask; none of these is needed.

## figma-workflow and Figma's own tooling

Figma's MCP server, its design-to-code skill and Code Connect turn a frame into code that fits a codebase. figma-workflow uses them and adds the controls a small team needs when a designer, not a frontend developer, ships the UI:

- **An approval gate.** Nothing is built until the designer has seen a plan with a mapping table: every design element against the repo's existing component or token, marked exact, nearest (flagged) or gap.
- **Screens kept in sync over time.** Each built screen gets a record in the repo. When the frame changes, `sync` plans only the differences, keeps what differs on purpose, and says so when nothing changed.
- **A prototype boundary.** Designer-built pages are clickable prototypes with no backend: sample data generated from the app's data model, in-memory interaction, and a prototype marker that keeps them out of production until the backend team promotes them.
- **An independent audit.** `verify` checks coverage, fidelity, behaviour and design-system reuse in a fresh context that never saw the build.
- **The right model for each step.** Planning runs on Opus at high effort; building runs on the session's model, usually Sonnet, so the designer can steer it cheaply.

Code Connect is optional. When a repo has it, its mappings win; when it doesn't, the skills match components from the repo's facts files and don't push you into setting it up. The plugin's `references/code-connect.md` says how to adopt it.

## Principles

1. **Canonical sources outrank the work.** When they conflict, surface the conflict; don't quietly resolve it in the output.
2. **Missing decisions go to their owner.** An agent stops and asks; it does not invent the answer.
3. **Independence is what makes a review useful.** A reviewer sees the sources and the work, not the author's reasoning.
4. **Effort scales with stakes.** A council is for decisions that are costly to reverse, not for everyday questions.

## When a skill uses a subagent

A subagent starts with no context. It has to rebuild what it needs, and it can't ask the user anything. That cost pays off only for a reason that can't be had in the current context. A skill starts one only for at least one of these four reasons:

1. **Independence.** The judgment would be anchored by what this context already believes: reviewing your own work, generating options without your favorite in view, estimating the risk of a plan you wrote. Fresh context is the whole point.
2. **Parallelism.** Several independent pieces can run at once, and must not see each other: council seats, the two lenses of a deep review.
3. **Context isolation.** A large read or search whose details the caller doesn't need, only its conclusion.
4. **Enforcement.** A different model or effort, or tool limits the agent's own definition enforces, such as a reviewer whose definition removes the file-editing tools and asks for Opus. Read-only beyond that is an instruction, not a hard limit: reviewers keep Bash so they can run git and validators.

A skill stays in the current context when:

- it needs the conversation, the user's preferences, or questions and approvals along the way (deciding, planning with the user, settling one question at a time);
- it is sequential or small, so a cold start costs more than it saves;
- it is mechanical or driven by a script (git operations, filling in a template);
- it takes side-effecting steps that need the user's approval in the moment (merge, delete, send).

Every skill that starts a subagent also checks that the surface can start one, and says so plainly when it can't. It never simulates independence in one context.

| Skill | Subagent? | Reason |
|---|---|---|
| `/review:fresh-eyes` | Yes: one, or two for deep review | Independence; parallelism for the two deep lenses; enforcement (no file-editing tools; Opus by default) |
| `/council:decision-council` | Yes: three to five, in parallel | Independence and parallelism |
| `/council:best-of-n` | Yes: one drafter, or n in parallel for an open-ended problem; plus two or three builders in parallel, each in its own worktree, when checks can separate the finalists | Independence (no anchoring on your favorite, and for open-ended problems no single shared framing); isolation of the build; parallelism for the drafts and the measured finalists |
| `/council:risk-evaluation` | No by default. Yes for your own high-stakes work | It needs the context; an independent run removes author bias where that matters |
| `/council:ask-specialist` | Yes: one | Independence on one hard question. Started by the user, or by a workflow step that names it |
| `/figma-workflow:sync`, `:build` | No | They need the conversation, questions and one approval; `sync` runs on Opus for the turn, `build` on the session model so the user can steer |
| `/figma-workflow:verify` | Yes: one (`verify-audit`, forked) | Independence from the build; enforcement (Opus, high effort) |

## Using these in Claude Code cloud sessions

Cloud sessions don't install plugins from your local settings or from a repository's `.claude/settings.json`. Add this marketplace on claude.ai instead (see Install): plugins enabled on your claude.ai account load in cloud sessions too, as `<plugin>@synced`, with their agents and the same names as locally. Nothing needs committing to your repositories. A repository can turn one off with `"enabledPlugins": {"review@synced": false}` in its `.claude/settings.json`.

## Install

In Claude Code:

```bash
claude plugin marketplace add StephanRyatt/agent-charter
claude plugin install review@agent-charter
claude plugin install council@agent-charter
claude plugin install figma-workflow@agent-charter
```

To update later, run `claude plugin marketplace update agent-charter`, or turn on auto-update for it under `/plugin` → Marketplaces. To try it from a local clone, use `claude plugin marketplace add ./agent-charter` instead.

On claude.ai: **Customize → Plugins → Add → Add marketplace**, enter `StephanRyatt/agent-charter`, then add the plugins you want. Plugins you add on claude.ai also reach Claude Code on any machine signed in to the same account. To get an update, trigger the sync for the marketplace under Customize → Plugins: it may not pick up a new version on its own, even with auto-sync on. Claude Code then downloads the update the next time it starts; in a session that is already open, run `/reload-plugins`.

Plugin agents run in Claude Code (local and cloud sessions), Cowork and claude.ai chat (checked 2026-10-31). On a surface that can't start one, `fresh-eyes` and the council say so rather than pretend to.

## License

MIT
