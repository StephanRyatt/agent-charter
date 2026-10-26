# agent-charter

**Build from the spec. Check against the source.**

A charter is the founding document that grants authority and sets scope. This repository is the charter my AI agents work under: plugins that keep agent work tied to its governing sources, and that get it checked by fresh eyes before it ships.

It is a [Claude Code](https://code.claude.com) plugin marketplace. The skills follow the open Agent Skills format.

## Plugins

| Plugin | What it does | Command |
|---|---|---|
| `review` | Fresh eyes on any work: code against its spec, a plan, a decision, a document or filing, yours or someone else's. Independent reviewers judge it from the governing sources and first principles, with a checklist suited to each kind of work. Pick report-only or fix mode, and standard or deep scrutiny. | `/review:fresh-eyes` |
| `council` | Several independent specialists analyze one consequential decision, each through a different lens, and their disagreements are synthesized into a recommendation. | `/council:decision-council` |
| | A fresh subagent works out the best n distinct solutions from first principles, compares their tradeoffs, and builds the winner or a hybrid. n, the model (Opus by default) and the effort scale with the stakes. | `/council:best-of-n` |
| | What could go wrong, how likely, how bad: the top risks quantified honestly (likelihood, impact, expected cost, with each number's basis) and qualified (reversibility, detection, cheapest mitigation), on one page. | `/council:risk-evaluation` |
| | One bounded, hard question put to a fresh reasoning specialist, with its answer checked against the sources. | `/council:ask-specialist` (agent `council:reasoning-specialist`) |

Planned: `spec`, which covers deciding, planning, implementing with acceptance proofs, and review. It is published once its planning step has run end to end on real work.

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
4. **Enforcement.** A different model or effort, or tool limits the agent's own definition enforces, such as a read-only reviewer pinned to Opus.

A skill stays in the current context when:

- it needs the conversation, the user's preferences, or questions and approvals along the way (deciding, planning with the user, settling one question at a time);
- it is sequential or small, so a cold start costs more than it saves;
- it is mechanical or driven by a script (git operations, filling in a template);
- it takes side-effecting steps that need the user's approval in the moment (merge, delete, send).

Every skill that starts a subagent also checks that the surface can start one, and says so plainly when it can't. It never simulates independence in one context.

| Skill | Subagent? | Reason |
|---|---|---|
| `/review:fresh-eyes` | Yes: one, or two for deep review | Independence; parallelism for the two deep lenses; enforcement (read-only, Opus) |
| `/council:decision-council` | Yes: three to five, in parallel | Independence and parallelism |
| `/council:best-of-n` | Yes: one | Independence (no anchoring on your favorite); isolation of the build |
| `/council:risk-evaluation` | No by default. Yes for your own high-stakes work | It needs the context; an independent run removes author bias where that matters |
| `/council:ask-specialist` | Yes: one | Independence on one hard question. Started by the user, or by a workflow step that names it |

## Install

Not published yet: these commands work once the repository is public on GitHub. Until then, add it from a local clone with `claude plugin marketplace add <path-to-clone>`.

In Claude Code:

```bash
claude plugin marketplace add StephanRyatt/agent-charter
claude plugin install review@agent-charter
claude plugin install council@agent-charter
```

On claude.ai: **Customize → Plugins → Add marketplace**, enter `StephanRyatt/agent-charter`, then add `review` and `council`.

Plugin agents run in Claude Code and Cowork. In claude.ai chat they don't, so `fresh-eyes` and the council say they can't start independent reviewers there, rather than pretend to.

## License

MIT
