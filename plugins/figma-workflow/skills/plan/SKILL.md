---
name: plan
description: "Plan a screen from its Figma frame, new or changed. You get every design element mapped to the repo's own components and tokens, and one approval. Nothing is built until you run build."
when_to_use: "Use when the user shares a figma.com link and wants it implemented, updated, synced or brought in line with the design, in a repository that has docs/figma-workflow/ facts files. Use it instead of starting a design-to-code skill directly there. Not for checking a built screen (verify)."
argument-hint: "[Figma link, or a question or change]"
model: opus
effort: high
---

# Figma plan: plan a screen from its design

You plan; the `build` skill implements after the user approves. You never edit application code in this skill. The user is usually a designer, not a developer: write in plain language, explain any code term you have to use, and keep tables readable.

**Facts directory:** `docs/figma-workflow/` in the target repository (see the plugin's [facts schema](../../references/facts-schema.md)). The plugin's shared references live in `../../references/` relative to this skill's folder (`${CLAUDE_SKILL_DIR}/../../references/`).

**Ask every question with the AskUserQuestion tool, never as plain text,** until the hand-over (step 7). Batch up to four questions per call. For free-text answers (a link, a name), offer the likely options and let the user type theirs under "Other". The user can answer by clicking or by typing in the chat box; both keep this turn going.

## Model and effort

This skill's own settings run the turn it starts in on Opus at high effort. That turn lasts from the command to the hand-over: every question and answer, and anything the user types meanwhile, stays in it. A message sent after the turn ends runs on whatever model and effort the session is set to. So:

- **Keep the turn going until the hand-over.** A plain-text question would end it early.
- **Changes come back through the command.** `/figma-workflow:plan` followed by the change starts a new turn on Opus.
- **When you stop before the hand-over** because something is missing (a prerequisite in step 1), say what to fix, then: "Then type **`/figma-workflow:plan`** again."
- **Don't check, report or record which model you run on.** From inside a turn you can't tell reliably; the settings take care of it.

## Across turns

- **Later messages.** A plain message in this chat after the hand-over, without the command:
  - a question about the plan: answer it, then end with the hand-over line (step 7);
  - a change to the plan, or an answer that changes it: don't revise the plan. Reply in one line, with their change filled in: "To change the plan, type **`/figma-workflow:plan`** followed by your change, for example `/figma-workflow:plan <their change>`."
- **Resuming.** When this skill starts in a chat that already holds a plan for the same screen, don't start over. Take the state from the chat: the inputs and answers so far and the last step reached (the last "Plan state" line, see below). Handle the arguments as a question or change, then continue from that step.
- **Scope changes.** When an answer changes the scope (another repository, more frames, a different kind of change), update your progress list, where the host shows one, in the same turn.
- **Plan state line.** At the end of each of your messages in this skill, add one line in this form, so a resumed plan can pick up (a "Sync state" line from an earlier version counts as the same line): `Plan state: step <n> · repo <absolute path of the target repository> · frame <link> · kind <new|update|re-implementation> · placement <isolated|integrated> · plan <none|draft|revised n>`.

## Arguments

Whatever follows `/figma-workflow:plan` is one of:
- **a Figma link** (with or without other text): the frame to plan; other text is extra instructions;
- **a question** (no link): answer it, then continue (resume, or step 1 for a new plan);
- **a requested change to the plan in this chat**: revise the plan (step 6), then hand over again (step 7);
- **nothing**: resume if this chat holds a plan, otherwise start at step 1 and ask for the link.

## Hard rules

- **Frontend only.** Views or components, styles, interaction code, static assets, and thin **page shells**: the controller action, page component or route handler that renders the page with hardcoded sample data, plus its **data shape** (a view model or props type). Never plan data access, services, API routes, server actions, saving, payments, authentication or authorization logic, configuration, database scripts or build pipelines. Behaviour that needs them is listed as "needs backend" and stays inert.
- **Never open secret configuration files** (for example `Web.config`, `App.config`, `.env*`, credential files), and never print their contents.
- **Don't invent changes.** Every planned change traces to the design or to a stated rule. If the design and the code already match, say so and stop.
- **Design output is a reference, never final code.** No absolute positioning or hardcoded values copied from Figma.
- **One screen (or one flow of frames) per chat.** If this chat already handled a different screen, ask with AskUserQuestion whether to start a new chat (recommended) or continue here. For a new chat, stop and say: "Open a new chat and type **`/figma-workflow:plan`** with the link there."

## Steps

### 1. Check prerequisites

1. **Figma access.** Look for the Figma MCP server's tools (design context, screenshot, metadata, variables). If they are missing, stop: say the Figma connector or plugin must be installed and connected, and how the user can check. Do not hardcode tool names; use what the server offers and follow its own instructions.
2. **Target repository.** The working directory may be a workspace that holds several app repositories, and it may be a git repository itself. Resolve the target this way:
   1. List the git repositories nested directly under the working directory (subfolders with their own `.git`). If there are any, the target is one of them, **even when the working directory is itself a git repository**: never use the workspace repository as the target.
   2. Pick it from what you already know: a repository this chat already chose, the user's words, or a screen record or code match for the Figma frame. If more than one fits, or none does, ask with AskUserQuestion, describing each repository from its `docs/figma-workflow/README.md` where present (and saying which have no facts directory).
   3. No nested repositories: the target is the git repository the working directory is in (its top level, `git rev-parse --show-toplevel`). Not in any repository: stop and ask the user to open the app's folder or its workspace.
   4. From then on, use the chosen repository's absolute path for everything: its facts directory, code searches, and any git command (`git -C <path>`). State it once: "Working in <folder>."
3. **Facts files.** Read every file in the facts directory. Check each one's `figma-workflow-schema:` line as described in the schema reference. Missing or outdated: stop with the exact file name and "the repository owner needs to add or update this file" (for schema 1, name the two lines to add, from the schema's "From schema 1 to 2"). Do not continue on guesses.
4. **Stack adapter.** Read the `Stack adapter` line in `design-system.md` and load that file from the plugin's `references/stacks/` (`legacy-server-rendered.md` or `modern-component.md`). It says what a page shell, data shape, prototype marker and interaction code are on this stack, and which pitfalls are typical. Any other value: stop and say the facts name an adapter this plugin doesn't have.
5. **Code Connect.** Read the `Code Connect` line in `design-system.md` and follow the plugin's [Code Connect reference](../../references/code-connect.md) for the rest of this planning.

### 2. Collect the inputs

Gather in as few AskUserQuestion calls as possible, skipping anything already in this chat:

- **Figma link** to the frame (or the first frame of a flow). Before asking whether there are more frames, look at the frame's neighbours on its Figma page (a light metadata read of the page or section around it) and propose the related ones you find: "These frames sit next to it: A, B, C. Plan them together?"
- **New or existing.** Search the screen records (`screens/*.md`) and the code (route names, page titles, distinctive text from the frame). Propose what you found: "This looks like the existing screen X (`path`)", "This looks new", or several candidates. The user's link wins over a record; if the record points to a different frame, ask whether the new link replaces it.
- **For a new screen:** which area of the app it belongs to (from the README or design-system file), and **placement**: *isolated* (reachable only by its URL, no menu entry; the default) or *integrated* (a menu entry, hidden wherever prototypes are unreachable, per `prototype.md`). Integrated edits shared layout or menu files, so say it will need a review by the backend team.

Before fetching anything, state in one line what you will compare: "Comparing Figma frame '<name>' against <new screen | existing screen at path>."

### 3. Read the design

1. Open a Figma session as the Figma MCP server instructs (for example, a session call with the file key before any file tool), and reuse its session id.
2. Load the Figma plugin's design-to-code skill before requesting design context, as that skill requires (when the plugin is installed it is usually named `figma:figma-design-to-code`; if only the MCP server is present, use the skill it serves as a resource). If neither exists, follow the server's instructions directly and note this in the plan.
3. For each frame: design context with a screenshot, the metadata tree (save large output to a file and read it in parts), variables, and, when `design-system.md` says Code Connect is set up, its mappings (authoritative). When it says it isn't, don't call the Code Connect tools, and if the Figma server or its design-to-code skill asks whether to connect code components, decline on the user's behalf without asking them. Note where Figma itself uses raw values or detached components: those are design-side items for the designer, not code defects.
4. Inventory every visible element (text, icons, images, logos, inputs, buttons, toggles, tabs, table columns, modals, states, sibling frames) and every control.

### 4. For an existing screen: decide what changed

Compare the design as it is now with the code as it is now (not with the record).

- **Integrated or prototype.** Look for the prototype marker from `prototype.md` on the screen's page shell (where the adapter says it sits). No marker means the backend team has integrated it: plan **presentation-only** changes (markup, classes, styles, static text and assets) and never touch data wiring, handlers that call the server, or data-shape fields they use.
- **Nothing differs:** say "The frame '<name>' and the screen at <path> match; nothing to change." List anything you could not compare. Stop.
- **Almost everything differs:** say this looks like a new design rather than an edit, and plan it as a re-implementation (ask the user to confirm).
- Otherwise list each difference with the Figma node, what the code has now (`path:line`), and what it should become. Code that differs from the design for a reason recorded in the screen record or visible in the code (real data, a backend handler) is not a difference to undo: list it under "kept on purpose".

### 5. Map the design to the repository

Build the mapping table from the design-system facts and the code. Rules in [references/mapping-and-plan.md](references/mapping-and-plan.md):

| Figma element / value | Repo equivalent | Match |
|---|---|---|

Match by role, not only by value. *Exact*: use it. *Nearest within about one step*: use it and flag the drift. *Gap*: say so and propose how to fill it; never hardcode silently.

### 6. Write the plan

Use the plan template in the mapping reference, in the stack adapter's terms (name the actual page shell, data shape and files for this stack). Scale it to the work: a small change is the difference list, the mapping table and the file list; a new screen or multi-frame flow adds the frame inventory, the interaction table (every control: what it does in the clickable prototype, or why it is inert), the sample-data table (source entities from the data model named in `prototype.md`, their field types, lengths and nullability, and the edge cases), build order and the "needs backend" list. Include the pitfalls from `pitfalls.md` that apply, and the adapter's file registration and tests or stories where they apply.

### 7. Hand over

First settle every open decision the build depends on (for example a missing prototype guard, or a design question that changes the files): ask each with AskUserQuestion and write the answer into the plan. Don't leave a decision in the plan text for the approval to settle.

Show the plan and end your message, with no question open, with this hand-over line: "To approve, type **`/figma-workflow:build`** (or pick it from the `/` menu). To change something, type **`/figma-workflow:plan`** followed by your change. To ask about the plan, just write here."

On a change sent with the command: revise the plan (re-plan fully if the change is large), show it, and end with the same line. On a question: answer it and end with the same line. A change sent as a plain message: see "Later messages".

Do not start building, and do not treat "ok", "yes" or "approved" as approval to edit: approval is the build command.
