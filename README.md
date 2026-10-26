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
| | A single reasoning specialist for one bounded, hard question. | agent `council:reasoning-specialist` |

Planned: `spec`, which covers deciding, planning, implementing with acceptance proofs, and review. It is published once its planning step has run end to end on real work.

## Principles

1. **Canonical sources outrank the work.** When they conflict, surface the conflict; don't quietly resolve it in the output.
2. **Missing decisions go to their owner.** An agent stops and asks; it does not invent the answer.
3. **Independence is what makes a review useful.** A reviewer sees the sources and the work, not the author's reasoning.
4. **Effort scales with stakes.** A council is for decisions that are costly to reverse, not for everyday questions.

## Install

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
