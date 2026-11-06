# agent-charter

**Decide before you build. Build from the spec. Check against the source.**

AI agents work fast and sound sure. Left alone, they drift from the spec, fill a missing decision with a guess, and grade their own work. A charter is the founding document that grants authority and sets scope. This repository is the charter my AI agents work under: plugins that keep agent work tied to its governing sources, leave each decision with its owner, and get the work checked by an agent that didn't make it.

It is a [Claude Code](https://code.claude.com) plugin marketplace. The skills follow the open Agent Skills format.

## Plugins

| Plugin | What it does | Command |
|---|---|---|
| `decision` | **Stress-test a costly decision while you can still change it.** Bring the problem, the options or the path you chose. Three to five independent specialists weigh the alternatives, each from a different angle, and you get a recommendation with its tradeoffs, what it turns on, and the strongest dissent. You decide; nothing is built. | `/decision:council` |
| | **Compare n approaches to a problem, then build the best.** Distinct solutions are drafted independently: by one agent, or by several in parallel for open-ended problems. The winner is picked on criteria set up front, measured by tests where they can tell it apart, then built. It makes the call; you review the result. n, the model (Opus by default) and the effort scale with the stakes. | `/decision:best-of-n` |
| | **Get an independent answer to one hard question,** such as whether a formula, algorithm or rule holds. A read-only reasoner works it out from your sources in a fresh context and says how to verify its answer. It is an agent, not a command: in Claude Code, type `@` and pick it, or ask for the reasoner. | agent `decision:reasoner` |
| `review` | **Get an independent check that finished work is correct.** Code against its spec, a plan, a decision, a document or filing, yours or someone else's. The reviewer judges it from the governing sources with a checklist suited to each kind of work. Pick report-only or fix mode, and standard or deep scrutiny. | `/review:fresh-eyes` |
| | **See what could go wrong with one plan, how likely, how bad.** For a plan, change, launch, filing or situation: what could happen, not whether the work is correct. The top risks ranked on one page, with honest numbers and their basis, how reversible each is, and the one action that cuts the most risk. | `/review:risks` |
| `figma-workflow` | **Plan a screen from its Figma frame, new or changed.** Every design element is mapped to the repo's own tokens and components, and it says so when nothing changed. Works on server-rendered apps (Razor, jQuery, Bootstrap) and component stacks (React, Vue, Next.js) through stack adapters. Repository facts live in the repo's `docs/figma-workflow/`. | `/figma-workflow:plan` |
| | **Build the approved plan as a clickable prototype.** No backend: real navigation, in-memory state, every control working or listed as inert. Typing it is the approval. | `/figma-workflow:build` |
| | **Check a built screen against its Figma design.** An independent audit of coverage, fidelity, behaviour and design-system reuse, with a to-do list for the designer. | `/figma-workflow:verify` |

`decision` settles what to do before you act. `review` scrutinizes what already exists. `figma-workflow` is a workflow, with steps you run in order.

Planned: a workflow from spec to verified code, covering planning, implementing with acceptance proofs, and review. It is published once its planning step has run end to end on real work.

## Which one?

Pick by the question you're asking:

| Your question | Use | Who decides |
|---|---|---|
| What should we do? A costly decision, still open or already chosen | `/decision:council` | You |
| How should this be built? You're happy to hand over the choice | `/decision:best-of-n` | It does; you review the result |
| Is this work correct against its sources? Finished work, a plan, a decision, a PR | `/review:fresh-eyes` | You act on the findings |
| What could go wrong with this plan, how likely, how bad? | `/review:risks` | You |
| One hard question with a definite answer, in a fresh context | agent `decision:reasoner` | You |

For a plain bug hunt in a diff, Claude Code's own `/code-review` fits better. For a low-stakes or easily reversed question, just ask; none of these is needed.

## figma-workflow and Figma's own tooling

Figma's MCP server, its design-to-code skill and Code Connect turn a frame into code that fits a codebase. figma-workflow uses them and adds the controls a small team needs when a designer, not a frontend developer, ships the UI:

- **An approval gate.** Nothing is built until the designer has seen a plan with a mapping table: every design element against the repo's existing component or token, marked exact, nearest (flagged) or gap.
- **Screens kept in sync over time.** Each built screen gets a record in the repo. When the frame changes, `plan` plans only the differences, keeps what differs on purpose, and says so when nothing changed.
- **A prototype boundary.** Designer-built pages are clickable prototypes with no backend: sample data generated from the app's data model, in-memory interaction, and a prototype marker that keeps them out of production until the backend team promotes them.
- **An independent audit.** `verify` checks coverage, fidelity, behaviour and design-system reuse in a fresh context that never saw the build.
- **The right model for planning.** Planning needs Opus at high effort for the whole conversation. A skill can set the model only for the turn it starts in, so `plan` checks what the session is set to and asks the user to switch in the model menu when it isn't. `plan` and `build` each run the turn they start in at exactly high effort, even when the session is set higher. Later turns, including steering a build, run at the session's effort, so keep the session on High.

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
| `/decision:council` | Yes: three to five, in parallel | Independence and parallelism |
| `/decision:best-of-n` | Yes: one drafter, or n in parallel for an open-ended problem; plus two or three builders in parallel, each in its own worktree, when checks can separate the finalists | Independence (no anchoring on your favorite, and for open-ended problems no single shared framing); isolation of the build; parallelism for the drafts and the measured finalists |
| agent `decision:reasoner` | It is one | Independence on one hard question; enforcement (Opus, no file-editing tools). Called by the user or by a workflow step that names it |
| `/review:fresh-eyes` | Yes: one, or two for deep review | Independence; parallelism for the two deep lenses; enforcement (no file-editing tools; Opus by default) |
| `/review:risks` | No by default. Yes for your own high-stakes work | It needs the context; an independent run removes author bias where that matters |
| `/figma-workflow:plan`, `:build` | No | They need the conversation, questions and one approval; `plan` needs the session on Opus at high effort and checks it, `build` runs on the session model so the user can steer |
| `/figma-workflow:verify` | Yes: one (`verify-worker`, forked) | Independence from the build; enforcement (Opus, high effort) |

## Using these in Claude Code cloud sessions

Cloud sessions don't install plugins from your local settings or from a repository's `.claude/settings.json`. Add this marketplace on claude.ai instead (see Install): plugins enabled on your claude.ai account load in cloud sessions too, as `<plugin>@synced`, with their agents and the same names as locally. Nothing needs committing to your repositories. A repository can turn one off with `"enabledPlugins": {"review@synced": false}` in its `.claude/settings.json`.

## Install

In Claude Code:

```bash
claude plugin marketplace add StephanRyatt/agent-charter
claude plugin install decision@agent-charter
claude plugin install review@agent-charter
claude plugin install figma-workflow@agent-charter
```

To update later, run `claude plugin marketplace update agent-charter`, or turn on auto-update for it under `/plugin` → Marketplaces. To try it from a local clone, use `claude plugin marketplace add ./agent-charter` instead.

On claude.ai: **Customize → Plugins → Add → Add marketplace**, enter `StephanRyatt/agent-charter`, then add the plugins you want. Plugins you add on claude.ai also reach Claude Code on any machine signed in to the same account. To get an update, trigger the sync for the marketplace under Customize → Plugins: it may not pick up a new version on its own, even with auto-sync on. Claude Code then downloads the update the next time it starts; in a session that is already open, run `/reload-plugins`.

Plugin agents run in Claude Code (local and cloud sessions), Cowork and claude.ai chat (checked 2026-10-31). On a surface that can't start one, `fresh-eyes`, `council` and `best-of-n` say so rather than pretend to.

## Upgrading from earlier versions

This release renames the `council` plugin and several skills. In Claude Code, installs from this marketplace move to the new plugin name on their own; two things need one command each. A committed `.claude/settings.json` that enables `council` is rewritten too, so commit that change.

- **`council` is now `decision`.** After the marketplace updates, run `/plugin install decision@agent-charter` once. Until you do, Claude Code reports the plugin as not cached.
- **`/council:decision-council` is now `/decision:council`.**
- **`/council:risk-evaluation` is now `/review:risks`.** If you don't have `review` yet, run `/plugin install review@agent-charter`.
- **`/council:ask-specialist` is retired.** Use the `decision:reasoner` agent instead: in Claude Code, type `@` and pick it, or ask for the reasoner.
- **`/figma-workflow:sync` is now `/figma-workflow:plan`.** The old command still works for one release and points to the new one.
- **Agents:** `council:reasoning-specialist` is now `decision:reasoner`, and `review:fresh-reviewer` is now `review:reviewer`.
- **Old names in other files:** update any workflow, instruction file (such as `CLAUDE.md`) or permission rule (such as `Skill(council:...)`) that names an old skill or agent. Nothing rewrites those for you.
- **On claude.ai:** trigger the sync for the marketplace under Customize → Plugins, add `decision` (and `review` if you want `risks`), then remove `council` if it is still listed. Otherwise your sessions load the old and new skills side by side.

## License

MIT
