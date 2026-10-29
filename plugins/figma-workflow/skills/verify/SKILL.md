---
name: verify
description: Check a frontend implementation against its Figma design with an independent audit (coverage, fidelity, behaviour, design-system reuse) in a repository that has docs/figma-workflow/ facts files. Use when the user asks to verify, check, review or audit a screen, branch, PR or diff against a Figma design or figma.com link, or types the verify command after a build.
---

# Figma verify: independent check against the design

This skill collects the inputs, then starts the hidden `verify-audit` skill, which runs in a fresh context so it judges the work without this chat's assumptions. The audit cannot ask questions, so gather everything first. You don't audit anything yourself here.

**Facts directory:** `docs/figma-workflow/` in the target repository.

## 1. Check that an independent audit can run

The audit needs a forked subagent with access to the Figma MCP server. If this surface can't start one, or the Figma server's tools are missing, say so plainly and stop. Never audit in this context and call it independent.

## 2. Collect the inputs

Take what this chat already has (a sync plan, a build summary, the screen record), and ask only for what's missing, with the AskUserQuestion tool (never plain text; batch up to four questions):

- **Target repository.** Use the one this chat's sync plan or build used. Otherwise list the git repositories nested directly under the working directory; if there are any, the target is one of them, even when the working directory is itself a git repository (a workspace), so never pick the workspace. Pick from the user's words or the Figma frame's screen record, or ask. No nested repositories: the repository the working directory is in. Pass its absolute path, and run git commands there (`git -C <path>`).
- **Figma**: the frame link(s). Default: from this chat or the screen record. If the record and the user's link differ, ask which one is the design of record.
- **Implementation scope**: the branch and its base (default: the current branch against the repository's default branch, `git merge-base`), a PR, or a list of files. Check that the diff isn't empty.
- **Depth**: *scoped* (only what the last build changed; the default right after a build) or *full* (the whole screen).
- **Audience**: *designer* (plain-language summary and a to-do list for Figma first; the default when the user is the designer) or *developer* (the full report).
- **Preview URL**, if the facts file names one and the page is deployed there. Optional.

Also collect, without asking: the `Stack adapter` and `Code Connect` lines from `design-system.md`, the screen record path, the facts files' paths, the Figma frame names and node ids, the list of changed files, and the intentionally inert controls from the record or build summary.

## 3. Run the audit

Invoke the `verify-audit` skill (the plugin may namespace it, for example `figma-workflow:verify-audit`) with one self-contained brief as its arguments:

```
Repository: <absolute path>   Facts directory: <path>/docs/figma-workflow/
Stack adapter: <legacy-server-rendered | modern-component>   Code Connect: <set up | not set up>
Figma: <link(s) with node ids and frame names>
Scope: <branch>..<base> (merge-base <sha>) | PR <ref> | files: <list>
Changed files: <list>
Depth: scoped | full   Audience: designer | developer
Screen record: <path or "none">   Intentionally inert controls: <list or "none">
Preview URL: <url or "none">
Notes: <anything from this chat the auditor must know as fact, never as opinion of the work>
```

Do not pass your own judgement of the work (what was hard, what you think is fine): independence is the point.

## 4. Present the result

1. For the designer: show the "For the designer" section first, then offer the full report.
2. Separate what to fix in code from what to fix in Figma.
3. Ask with AskUserQuestion whether to apply the code fixes now (all, selected items, or none). Fixes follow the same rules as the build skill: frontend only, existing tokens and components, the prototype pattern, the stack adapter's file registration and checks.
4. Never push or merge.
