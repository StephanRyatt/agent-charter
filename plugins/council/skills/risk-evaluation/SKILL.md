---
name: risk-evaluation
description: Estimate what could go wrong with one plan, decision, change, filing, launch or any situation the user names, how likely each risk is, and how bad it would be. Quantifies likelihood, impact and expected cost where that can be done honestly, qualifies reversibility, detection, drivers and the cheapest mitigation, and returns a one-page ranked risk table. Use when the user asks "what's the risk", "evaluate the risk", "how risky is this", "what could go wrong", for a risk assessment, or for a pre-mortem. Not for choosing between options (decision-council) or checking whether finished work is correct (fresh-eyes).
---

# Risk evaluation

Find the risks that matter for one case, put honest numbers on them where possible, and say which one to act on first. The output is a page, not a report.

How it differs from its neighbors:

- `/council:decision-council` chooses between options.
- `/review:fresh-eyes` (when the `review` plugin is installed) finds defects in finished work: whether it is correct, and red-teaming it. Risk evaluation asks what could happen even if the work is correct.
- `risk-evaluation` estimates what could go wrong, how likely it is, and how bad it would be.

It advises; it does not act on the target.

**Where it runs.** By default it runs in the current context, because it needs what this session knows. When the target is work authored or shaped in this session (your own plan, change or recommendation, or one you helped the user form) and the stakes are high, run it in a fresh subagent instead: one `general-purpose` agent on `opus`, given this skill's steps, the target and its sources, but not your own view of the risks. An author tends to underrate the risks of their own work, and a fresh context removes that bias. Check the subagent's table against the sources before you report it. If this surface cannot start a subagent, say that the evaluation is the author's own, and label it so.

## 1. Set the scope

Name three things, in one line each:

- **Target:** the plan, decision, change, filing, launch or situation. If the user did not name one, take the work in front of you in this session.
- **Horizon:** the period the risks are counted over, such as "until the release ships" or "the next 12 months".
- **What counts as failure:** the outcome the user cares about (money, time, users, a legal result, data, reputation).

Ask the user only if a missing answer would change the ranking. Otherwise state your assumption and go on.

## 2. Gather the facts

Read what bears on the target: the files, the plan, the diff, the documents, the rules it must meet. When an outside base rate would anchor a number and a search tool exists, look it up. Keep track of which source each number will rest on.

Do not spend effort here that the decision does not need. A small, reversible change needs a minute of reading, not research.

## 3. Run a quick pre-mortem

Assume it is the end of the horizon and the thing went wrong. List the reasons why. Aim for breadth first: technical, human, external, timing, legal or rule-based, and "we were wrong about the premise".

Then keep only the risks that matter: those that could plausibly happen and would hurt if they did. Usually three to six. Drop the rest without comment.

## 4. Estimate each risk

For each kept risk, give:

- **Likelihood:** a probability, a range, or a calibrated band ("about 1 in 10", "under 5%") over the horizon.
- **Impact:** in the unit that matters (money, days of delay, users affected, a legal or other consequence).
- **Expected cost:** likelihood times impact, as a range, where both are numbers. Otherwise leave it out.
- **Basis and confidence:** label each number **evidence** (a source, data, a measured rate), **inference** (reasoned from evidence), or **guess** (judgment). Say how confident you are: high, medium or low.

Rules:

- Never invent false precision. A range with its basis beats a point estimate with none.
- "Not quantifiable here, because …" is a valid answer. Then rank the risk qualitatively and say what would make it quantifiable.
- Say which numbers rest on which source.

## 5. Qualify each risk

In a few words each:

- **Kind:** for example technical, operational, financial, legal, schedule, security, reputational.
- **Reversibility:** reversible, costly to reverse, or irreversible.
- **Detection:** how early you would notice (before, at, or long after the damage).
- **Driver:** what makes it more or less likely.
- **Cheapest mitigation:** the smallest action that reduces it, and roughly by how much (for example, "a dry run cuts it from ~20% to ~5%").

## 6. Check across the risks

- **Correlation:** do several risks share a cause, so they would happen together? If so, treat them as one larger risk and say so.
- **Tails:** call out any risk with low likelihood but catastrophic or irreversible impact, even when its expected cost is small. Expected cost understates what cannot be undone.
- **Mitigations:** rank them by risk reduction per unit of effort. The best one is often cheap and removes a tail.

## 7. Report

Keep it to about a page:

1. One line with the target, horizon and what counts as failure, plus any assumption you made.
2. A ranked table of the top risks, worst first:

   | # | Risk | Likelihood | Impact | Expected cost or range | Reversibility | Mitigation (and its effect) |
   |---|---|---|---|---|---|---|

   Mark each number's basis (evidence, inference or guess) in the cell or in a short note under the table.
3. Two or three lines:
   - **Overall risk:** low, moderate, high or severe, with a one-clause reason.
   - **Dominant risk:** the one that matters most, and why (often a tail, not the highest expected cost).
   - **Best action:** the one action that most reduces it.

Add a short note only for what the table cannot carry, such as a tail risk or a correlation.

## Domain care

For legal, medical, financial or immigration matters, present probabilities as estimates, not advice. Where an authority or a professional decides the outcome (a court, an agency, a doctor, the published rules), name that source and point to it. Do not give personalized investment advice.

## When to offer more

When the stakes are high and the risk is hard to judge from one context, offer once, in one line, an independent check:

- `/review:fresh-eyes`, when the `review` plugin is installed, to challenge this risk evaluation or the work it covers;
- `/council:decision-council`, when the real question turns out to be choosing between options, for example when two or more credible alternatives to the plan appear during the evaluation.

Do not start either unasked. Both cost several agent runs.
