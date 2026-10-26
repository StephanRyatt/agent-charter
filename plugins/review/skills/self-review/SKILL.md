---
name: self-review
description: Have an independent reviewer with fresh context challenge what was just done (code, a document, a plan, a filing, a decision) against the governing sources and first principles, then resolve the confirmed findings. Use when the user asks for a self-review, a fresh-eyes or independent check of recent work, or when a workflow calls for review before handing work over.
---

# Self-review

Have the `fresh-reviewer` agent independently challenge the work just done, then resolve its confirmed findings here. When this skill comes from the `review` plugin, the agent is named `review:fresh-reviewer`. Review policy (what to look for, the finding format, read-only limits) lives in that agent. Do not restate or override it in the handoff.

## 1. Check that a fresh context is available

The review's value is independence: a reviewer that has not seen the author's reasoning. That needs a subagent.

If this surface cannot start one (for example, claude.ai chat, where plugin agents do not run), say so plainly. Offer to run the review in Claude Code or Cowork instead. Do not quietly review in the same context and call it independent. If the user still wants a same-context check, label it as such.

## 2. Determine the review target

Identify one coherent slice of what was just done:

- In a code repository: the current branch's unmerged diff.
- In a documents or knowledge project: the files created or changed in this task, or the specific deliverable (a letter, a form answer set, an evidence list, a plan).
- For a decision or recommendation: the text of it and the inputs it relied on.

Review that slice, not the whole project.

## 3. Gather the governing evidence, by reference

- **Requirements:** the task, issue, brief, or acceptance checklist.
- **Governing sources:** the project's own instructions (`CLAUDE.md`, `AGENTS.md`, knowledge files), its canonical documents, and authoritative outside sources the work must conform to (official rules, forms and their instructions, specifications).
- **Approved decisions** that bear on the work.
- **Validation evidence:** commands run and their results, checklists completed, sources consulted.

If required validation has not been run, run it first so the reviewer can inspect the evidence.

## 4. Invoke the reviewer

Start a new `fresh-reviewer` in fresh, isolated context.

- Do not reuse an authoring subagent or its context.
- Point it to the sources gathered above. Do not brief it with your conclusions, your rationale, or the problems you suspect.
- Do not override its model.

## 5. Adjudicate

Verify each finding independently against the governing evidence. Do not accept findings mechanically. Reject invalid, subjective, duplicate or out-of-scope findings, each with a brief reason.

## 6. Fix and validate

Fix the confirmed findings here, then re-run the validation for what changed.

If the fixes materially changed the substance (the design, the core logic, the strategy, or a decision), start one new `fresh-reviewer` for the changed part. Otherwise, do not repeat the review.

## 7. Report

Report concisely:

- findings confirmed and fixed;
- findings rejected, and why;
- checks run, and their results;
- any remaining uncertainty, or decisions only the user can make.

Do not merge, push, file, send or publish anything unless the user explicitly asked for it.
