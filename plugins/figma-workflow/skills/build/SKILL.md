---
name: build
description: "Build the approved plan as a clickable prototype. No backend: real navigation, sample data, every control working or listed as inert. Only you can start it; typing it approves the plan."
argument-hint: "[none: approves the plan above]"
model: opus
effort: high
disable-model-invocation: true
---

# Figma build: implement the approved plan

Typing this command is the user's approval of the most recent plan that the `plan` skill wrote in this chat. Implement exactly that plan in this chat, so the user can watch and steer. The user is usually a designer: report progress in plain language.

**Facts directory:** `docs/figma-workflow/` in the target repository. The plugin's shared references (facts schema, stack adapters, Code Connect) live in `../../references/` relative to this skill's folder (`${CLAUDE_SKILL_DIR}/../../references/`).

**Target repository:** the one the plan names (its "Repository / area" line and the last "Plan state" line, or "Sync state" from an earlier version, hold its path). The working directory may be a workspace that is a git repository itself: never use it as the target when it holds nested app repositories. If the plan doesn't make the repository clear, ask with AskUserQuestion, listing the git repositories nested directly under the working directory. Read the facts files from the target, make every edit inside it, and run every git command there (`git -C <path>`).

## Before editing

1. **Find the plan.** Use the latest plan the plan skill showed in this conversation, including its revisions. Build only what that plan shows. If there is none, stop: "There's no approved plan in this chat. Start with `/figma-workflow:plan` and your Figma link." If the user asked for a change after the latest plan and no revised plan shows it, ask with AskUserQuestion:
   - "Plan it first" (recommended): stop and say "Type **`/figma-workflow:plan`** followed by the change, then **`/figma-workflow:build`** again."
   - "Build without it": build the plan as shown, and list the change under "not done" in the summary.
2. **Re-read the facts files** (`design-system.md`, `prototype.md`, `pitfalls.md`, the screen record if any) and check their `figma-workflow-schema:` line is `3`. Missing or lower: stop and say which file is missing or outdated and that the repository owner has to add or update it. Higher: stop and say the plugin needs updating. `design-system.md` without a Viewports section, or with no entry for the screen's area: stop and say the repository owner has to add it (the schema's "From schema 2 to 3").
   Then load the stack adapter that `design-system.md`'s `Stack adapter` line names, from `references/stacks/`, and note its `Code Connect` line. The adapter says what the page shell, data shape, prototype marker and interaction code are here, how new files are registered, and which checks to run.
3. **Branch safety.** Run `git status` and `git branch --show-current` in the target repository.
   - On the default or a shared branch (for example `main`, `master`, `Development`, `Production`): ask with AskUserQuestion to create `figma/<screen-slug>` from it (recommended) or to stay. The screen slug is the Figma frame name in lowercase kebab-case (for example "Members list" → `members-list`), and it also names the screen record.
   - Uncommitted changes that are not from this chat: do not stash, reset, overwrite or switch away from them. Ask with AskUserQuestion how to proceed; recommend stopping until their owner commits them.
4. **Never open secret configuration files** (for example `Web.config`, `App.config`, `.env*`), and never print their contents.
5. **Code Connect.** Follow the [Code Connect reference](../../references/code-connect.md): when it is set up, use the mapped components; when it isn't, decline any offer from the Figma server to connect components without asking the user. Never add or publish mappings.

## Implement

Follow the plan's build order. Ask with AskUserQuestion (never plain text) when the plan turns out wrong or a decision is missing; don't improvise a change the design doesn't show. The one exception: a viewport the plan says follows a reference screen (below).

- **Read the design yourself:** before writing a frame's code, view that frame's screenshot yourself and pull its design context where you need it, as the design-to-code skill instructs. The plan's tables and any subagent's inventory add detail but never replace this.
- **Clickable prototype:** new pages and interactions follow [references/prototype-pattern.md](references/prototype-pattern.md), including the boundary, in the form the stack adapter gives (its "Page shell", "Data shape and data model" and "Interaction code" sections). Apply the prototype marker exactly as `prototype.md` prescribes. If `prototype.md` says the guard behind it is not in place yet, build anyway and say in the summary that the page must not be merged into a shared branch until it is.
- **Sample data:** generate it from the app's data model as the pattern's "Sample data" section says (the data shape mirrors the entities' fields; edge cases always included; no database, no data-access imports in the shell). Follow the plan's sample-data section; if the plan has none, derive it before writing the shell.
- **Integrated screens** (no marker): presentation changes only, as the plan says.
- **Viewports:** build each viewport the plan's Viewports line covers, served the way `design-system.md`'s Viewports entry says (CSS breakpoints, a separate view or component the server picks, or a separate route or host). One with a frame is built from that frame. One the plan says follows a reference screen is built from that screen's layout and patterns, with this screen's content; list what you took from it under "Inferred, not shown in the design" in the screen record. Don't build a viewport the plan marks *skipped* or *later*.
- **Reuse:** existing components, classes and tokens from the mapping table, in the styling approach the adapter and `design-system.md` describe. A gap gets the fill the plan proposed, in the canonical token or style source, as an additive variant or token. No hardcoded colours or sizes where a token exists, no arbitrary values that bypass the theme, no `!important`, no inline styles.
- **Duplicated stylesheets** (where `pitfalls.md` lists any): edit the copy that `design-system.md` and `pitfalls.md` name as the loaded one. If unsure which copy the page loads, trace the layout's style references before editing.
- **Registering new files:** whatever the adapter's "Registering new files" section and `pitfalls.md` require (for example every new file in an old-style project file, or a navigation config). A missed registration can silently leave the file out of the published site.
- **Tests and stories:** add them only as the adapter's "Tests and stories" section says (where the repository already has them).
- **Assets:** download every static image and icon the design uses as the design-to-code skill instructs, into the repository's asset folder; no temporary Figma asset URLs left in code; use exact assets, never redraw or substitute.
- **Copy:** text from the design, verbatim. When starting from an existing page as a base, remove every leftover of its text, names and data.
- **Accessibility basics:** `alt` on images (empty for decorative), labels on inputs, real `button` and `a` elements for controls.

## Check before reporting

Run the stack adapter's "Build checks" on the files you changed: shell purity (no data access or server calls), leftovers and escape hatches, and file registration. The scans match keywords: look at each hit, and report a hit in a comment or a harmless name as a false positive rather than rewording code to silence it. Quote file paths (route folders can contain parentheses or spaces).

Also check: each viewport the plan covers has its files, registered as the Viewports entry and the adapter say (for a version the server picks, the entry's per-screen file or registration exists for this screen); every control from the plan's interaction table is wired or listed as inert; every referenced token exists in the token source; every asset file exists and is non-empty.

**Render and compare.** Follow the adapter's "Preview" section. When the page can be rendered, render each built frame at its frame's width (for a modal or state, open it the way the prototype does) and compare it with that frame's Figma screenshot: layout, spacing, type, colour, assets. A viewport the server picks is requested the way its Viewports entry says, not by width alone; confirm with its "Tells apart" sign which version is on screen. If it can't be requested that way, or the sign shows another version, that viewport wasn't rendered: never compare another version in its place. Never sign in or enter credentials yourself: if the page needs a login the browser doesn't have, ask the user with AskUserQuestion to sign in in that browser, or to skip rendering. Fix the gaps, or list them in the summary. If the page can't be rendered here, don't claim it renders: say so in the summary, and how to preview it, using `prototype.md`'s preview section.

## Finish

1. **Update the screen record** `docs/figma-workflow/screens/<screen-slug>.md` (create it from [references/screen-record.md](references/screen-record.md) if new): schema line `figma-workflow-schema: 3`, Figma link(s), the Viewports line (one entry per declared viewport, as the plan's Viewports line says, with today's date on *skipped* and *later*), placement, routes, files, today's date as last synced, inert controls, inferred behaviour.
2. **Summarise** in plain language: what was built or changed, for which viewports (and which follow a reference screen, are skipped or left for later), per viewport whether it was rendered and compared and the visual gaps left, what is inert and why, what needs backend, anything not done, and how to preview.
3. **Offer the check:** "To have the work checked independently against the design, type **`/figma-workflow:verify`**."
4. **Offer a commit** on the feature branch (show the message first). Stage only the files this build created or changed, by path; never `git add -A` or `git add .`, which can pick up secrets or someone else's work. Never push or merge; that is for the backend team.
