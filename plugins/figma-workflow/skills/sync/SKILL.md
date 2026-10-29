---
name: sync
description: Front door for turning a Figma frame into a frontend screen in a repository that has docs/figma-workflow/ facts files. Plans a new screen or an update to an existing one from its Figma link, with a mapping table and one approval, then hands over to the build skill. Use when the user shares a figma.com link and wants it implemented, updated, synced or brought in line with the design in such a repository; use it instead of starting a design-to-code skill directly there.
model: opus
effort: high
---

# Figma sync: plan a screen from its design

You plan; the `build` skill implements after the user approves. You never edit application code in this skill. The user is usually a designer, not a developer: write in plain language, explain any code term you have to use, and keep tables readable.

**Facts directory:** `docs/figma-workflow/` in the target repository (see [references/facts-schema.md](references/facts-schema.md)).

**Ask every question with the AskUserQuestion tool, never as plain text.** A plain-text question ends your turn, and the next turn runs on a different model without this skill's instructions. Batch up to four questions per call. For free-text answers (a link, a name), offer the likely options and let the user type theirs under "Other".

## Hard rules

- **Frontend only.** Views, styles, page scripts, static assets, and thin page shells (a controller action and view model that only return hardcoded sample data). Never plan data access, services, saving, payments, authentication or authorization logic, configuration, database scripts or build pipelines. Behaviour that needs them is listed as "needs backend" and stays inert.
- **Never open secret configuration files** (for example `Web.config`, `App.config`, `.env`, credential files), and never print their contents.
- **Don't invent changes.** Every planned change traces to the design or to a stated rule. If the design and the code already match, say so and stop.
- **Design output is a reference, never final code.** No absolute positioning or hardcoded values copied from Figma.
- **One screen (or one flow of frames) per chat.** If this chat already handled a different screen, recommend a new chat before continuing.

## Steps

### 1. Check prerequisites

1. **Figma access.** Look for the Figma MCP server's tools (design context, screenshot, metadata, variables). If they are missing, stop: say the Figma connector or plugin must be installed and connected, and how the user can check. Do not hardcode tool names; use what the server offers and follow its own instructions.
2. **Target repository.** If the working directory is not a git repository, list the git repositories directly under it and ask which one this screen belongs to (use the facts directory's README, where present, to describe each one).
3. **Facts files.** Read every file in the facts directory. Check each one's `figma-workflow-schema:` line as described in the schema reference. Missing or outdated: stop with the exact file name and "the repository owner needs to add or update this file". Do not continue on guesses.

### 2. Collect the inputs

Gather in as few AskUserQuestion calls as possible, skipping anything already in this chat:

- **Figma link** to the frame (or the first frame of a flow). If the user has several frames, ask for all of them.
- **New or existing.** Search the screen records (`screens/*.md`) and the code (route names, page titles, distinctive text from the frame). Propose what you found: "This looks like the existing screen X (`path`)", "This looks new", or several candidates. The user's link wins over a record; if the record points to a different frame, ask whether the new link replaces it.
- **For a new screen:** which area of the app it belongs to (from the README or design-system file), and **placement**: *isolated* (reachable only by its URL, no menu entry; the default) or *integrated* (a menu entry, hidden wherever prototypes are unreachable, per `prototype.md`). Integrated edits shared layout or menu files, so say it will need a review by the backend team.

Before fetching anything, state in one line what you will compare: "Comparing Figma frame '<name>' against <new screen | existing screen at path>."

### 3. Read the design

1. Open a Figma session as the Figma MCP server instructs (for example, a session call with the file key before any file tool), and reuse its session id.
2. Load the Figma plugin's design-to-code skill before requesting design context, as that skill requires (when the plugin is installed it is usually named `figma:figma-design-to-code`; if only the MCP server is present, use the skill it serves as a resource). If neither exists, follow the server's instructions directly and note this in the plan.
3. For each frame: design context with a screenshot, the metadata tree (save large output to a file and read it in parts), variables, and any Code Connect mappings (authoritative). Note where Figma itself uses raw values or detached components: those are design-side items for the designer, not code defects.
4. Inventory every visible element (text, icons, images, logos, inputs, buttons, toggles, tabs, table columns, modals, states, sibling frames) and every control.

### 4. For an existing screen: decide what changed

Compare the design as it is now with the code as it is now (not with the record).

- **Integrated or prototype.** Look for the prototype marker from `prototype.md` in the screen's controller. No marker means the backend team has integrated it: plan **presentation-only** changes (markup, classes, styles, static text and assets) and never touch data wiring, handlers that call the server, or view-model properties they use.
- **Nothing differs:** say "The frame '<name>' and the screen at <path> match; nothing to change." List anything you could not compare. Stop.
- **Almost everything differs:** say this looks like a new design rather than an edit, and plan it as a re-implementation (ask the user to confirm).
- Otherwise list each difference with the Figma node, what the code has now (`path:line`), and what it should become. Code that differs from the design for a reason recorded in the screen record or visible in the code (real data, a backend handler) is not a difference to undo: list it under "kept on purpose".

### 5. Map the design to the repository

Build the mapping table from the design-system facts and the code. Rules in [references/mapping-and-plan.md](references/mapping-and-plan.md):

| Figma element / value | Repo equivalent | Match |
|---|---|---|

Match by role, not only by value. *Exact*: use it. *Nearest within about one step*: use it and flag the drift. *Gap*: say so and propose how to fill it; never hardcode silently.

### 6. Write the plan

Use the plan template in the mapping reference. Scale it to the work: a small change is the difference list, the mapping table and the file list; a new screen or multi-frame flow adds the frame inventory, the interaction table (every control: what it does in the clickable prototype, or why it is inert), the sample-data table (source entities from the data model named in `prototype.md`, their field types, lengths and nullability, and the edge cases), build order and the "needs backend" list. Include the pitfalls from `pitfalls.md` that apply.

### 7. Hand over

End with the plan and exactly this instruction:

> To approve this plan, type **`/figma-workflow:build`** (or pick the build command from the `/` menu). To change something first, tell me what; for a large change, I'll re-plan.

Do not start building, and do not treat "ok", "yes" or "approved" as approval to edit: approval is the build command.
