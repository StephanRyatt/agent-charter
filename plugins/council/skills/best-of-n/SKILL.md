---
name: best-of-n
description: Have one fresh-context subagent work out the best n genuinely distinct solutions to a problem from first principles, compare their tradeoffs, then build the winner (or a hybrid of the strongest parts) and explain briefly why it won. Use when the user asks for "best of n", "best of 3", "give me the best of several approaches", "explore options then build the best", "try a few approaches and pick one", or wants a solution built only after a first-principles comparison. Optionally takes n, a model and a reasoning level.
---

# Best of n

Have one subagent find the best n distinct solutions to a problem, compare them, and build the best one. The value comes from two things: **first principles** (solutions derived from what the problem requires, not from the first idea or from convention) and **a fresh context** (the subagent hasn't seen your own preferred answer, so it can't anchor on it).

Neighbors:

- `/council:decision-council` chooses between options for a consequential decision, with several independent specialists, and builds nothing.
- `/review:fresh-eyes` (when the `review` plugin is installed) reviews work that is already finished.
- Best of n is for a problem where you want the solution built, after a first-principles comparison.

## 1. Check that a subagent is available

The work must run in a separate agent. If this surface cannot start one (for example, claude.ai chat), say so. Offer to run it in Claude Code or Cowork. Never simulate the subagent in this context and present the result as independent. If the user still wants a same-context attempt, label it as such.

## 2. Settle n, the model and the effort

Take any of the three the user gave. Choose the rest:

- **n.** From how consequential the problem is:
  - **2** for a contained, easily reversed problem;
  - **3** as the usual default;
  - **4–5** for a problem that is costly to reverse or high-stakes.

  Don't go above 5: past that, the extra solutions are variations, not new approaches.
- **Model.** `opus`, unless the user named another.
- **Effort.** From the problem's difficulty and stakes:
  - **low** or **medium** for a small, well-understood problem;
  - **high** as the usual default;
  - **xhigh** for a hard or costly-to-reverse problem;
  - **max** only for the hardest, highest-stakes problems, or when the user asks.

Say what you chose in one line, with the reason for each choice you made yourself. For example: "n = 3, opus, high effort: a contained refactor, but it touches the public API."

## 3. Gather the facts and write the brief

The subagent starts with zero context. Anything it needs must be in the brief, and anything that would anchor it must stay out.

First gather the facts. If the problem touches a codebase or system, inspect it yourself (read-only) and put what you found in the brief as stated facts. Ask the user only if a missing answer would change the solutions materially; otherwise state your assumption in the brief and mark it as one.

**Put in the brief:**

- **The problem**, stated as what must be achieved, not as a solution.
- **Constraints**: what must hold, what must not change, and the limits on time, cost, dependencies and compatibility.
- **Success criteria**: how a solution will be judged done and good. Make them checkable where you can.
- **Sources**: the relevant files, docs, specs, and the project's own instructions (`CLAUDE.md`, `AGENTS.md`), by path or link.
- **Scope of the build**: what the deliverable is (code changes, a document, a plan) and where it may change files.
- **n**, and the instructions and output format below.

**Keep out of the brief:** your own preferred solution, your leaning, and any ranking of approaches. Don't list candidate solutions. If the user proposed one, include it as a constraint only if they require it; otherwise leave it out, so it competes on equal terms (you can check in step 5 whether it was covered).

**Instructions to the subagent:**

1. Work out the best n solutions from first principles: start from what the problem requires and its constraints, not from the first idea or the usual pattern.
2. Make them genuinely distinct: different approaches, not variations of one. Reject strawmen: each solution must be one a competent person could defend.
3. Compare them against the success criteria and the constraints, including their tradeoffs, cost, risk and reversibility. Judge by the criteria, not by preference.
4. Build the best one. That can be one of the n, or a hybrid that takes the strongest parts of several, if the comparison supports it. A hybrid that merely averages two solutions doesn't count. Build the actual deliverable, within the scope given. Don't commit, push, publish, send or merge.
5. Check the result against the success criteria (for code, run the relevant tests and checks), then report.

**Output format:**

- the n solutions, one or two lines each;
- a comparison table: solutions against the success criteria and the main tradeoffs;
- the choice (or hybrid) and why it won, briefly;
- what was built and where (files changed, or the deliverable itself);
- checks run and their results;
- what remains unverified.

## 4. Launch the subagent

Start one `general-purpose` agent with the brief. Pass the model through the Agent tool's `model` parameter and the effort through its `effort` parameter. Start a new agent each time; never reuse one that has seen your reasoning.

## 5. Check the result

Don't accept the report as given. Check:

- **It built what it said.** Read the changed files or the deliverable.
- **It meets the success criteria.** Re-run the checks it ran, and any it skipped.
- **The solutions were really distinct**, and the winner was judged on the criteria, not on preference.
- **It stayed in scope.** It changed only what the user asked for. Undo anything outside that scope, and say so.

Fix small gaps yourself. If the build fails the success criteria in substance, say so, and ask whether to fix it here or run again with a sharper brief.

## 6. Report

Report briefly:

- n, model and effort, and why;
- the n solutions in a line each, and the winner and why it won;
- what was built and where;
- checks run and their results;
- what remains unverified, and any decisions only the user can make.

Nothing gets committed, pushed, published, sent or merged unless the user asked.
