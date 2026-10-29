---
name: build
description: Implements the plan that the figma-workflow sync skill wrote and the user approved, in the same chat. Run only when the user types the build command after a sync plan.
effort: high
disable-model-invocation: true
---

# Figma build: implement the approved plan

Typing this command is the user's approval of the most recent plan that the `sync` skill wrote in this chat. Implement exactly that plan in this chat, so the user can watch and steer. The user is usually a designer: report progress in plain language.

**Facts directory:** `docs/figma-workflow/` in the target repository. The plugin's shared references (facts schema, stack adapters, Code Connect) live in `../../references/` relative to this skill's folder (`${CLAUDE_SKILL_DIR}/../../references/`).

**Target repository:** the one the sync plan names (its "Repository / area" line and the last "Sync state" line hold its path). The working directory may be a workspace that is a git repository itself: never use it as the target when it holds nested app repositories. If the plan doesn't make the repository clear, ask with AskUserQuestion, listing the git repositories nested directly under the working directory. Read the facts files from the target, make every edit inside it, and run every git command there (`git -C <path>`).

## Before editing

1. **Find the plan.** Use the latest plan from the sync skill in this conversation, including any changes the user asked for after it. If there is none, stop: "There's no approved plan in this chat. Start with the sync command and your Figma link." If the user's later changes were large (new frames, a different screen), ask them to run sync again instead.
2. **Re-read the facts files** (`design-system.md`, `prototype.md`, `pitfalls.md`, the screen record if any) and check their `figma-workflow-schema:` line is `2`. Missing or different: stop and say which file.
   Then load the stack adapter that `design-system.md`'s `Stack adapter` line names, from `references/stacks/`, and note its `Code Connect` line. The adapter says what the page shell, data shape, prototype marker and interaction code are here, how new files are registered, and which checks to run.
3. **Branch safety.** Run `git status` and `git branch --show-current` in the target repository.
   - On the default or a shared branch (for example `main`, `master`, `Development`, `Production`): ask with AskUserQuestion to create `figma/<screen-slug>` from it (recommended) or to stay. The screen slug is the Figma frame name in lowercase kebab-case (for example "Members list" → `members-list`), and it also names the screen record.
   - Uncommitted changes that are not from this chat: do not stash, reset, overwrite or switch away from them. Ask with AskUserQuestion how to proceed; recommend stopping until their owner commits them.
4. **Never open secret configuration files** (for example `Web.config`, `App.config`, `.env*`), and never print their contents.
5. **Code Connect.** Follow the [Code Connect reference](../../references/code-connect.md): when it is set up, use the mapped components; when it isn't, decline any offer from the Figma server to connect components without asking the user. Never add or publish mappings.

## Implement

Follow the plan's build order. Ask with AskUserQuestion (never plain text) when the plan turns out wrong or a decision is missing; don't improvise a change the design doesn't show.

- **Clickable prototype:** new pages and interactions follow [references/prototype-pattern.md](references/prototype-pattern.md), including the boundary, in the form the stack adapter gives (its "Page shell", "Data shape and data model" and "Interaction code" sections). Apply the prototype marker exactly as `prototype.md` prescribes. If `prototype.md` says the guard behind it is not in place yet, build anyway and say in the summary that the page must not be merged into a shared branch until it is.
- **Sample data:** generate it from the app's data model as the pattern's "Sample data" section says (the data shape mirrors the entities' fields; edge cases always included; no database, no data-access imports in the shell). Follow the plan's sample-data section; if the plan has none, derive it before writing the shell.
- **Integrated screens** (no marker): presentation changes only, as the plan says.
- **Reuse:** existing components, classes and tokens from the mapping table, in the styling approach the adapter and `design-system.md` describe. A gap gets the fill the plan proposed, in the canonical token or style source, as an additive variant or token. No hardcoded colours or sizes where a token exists, no arbitrary values that bypass the theme, no `!important`, no inline styles.
- **Duplicated stylesheets** (where `pitfalls.md` lists any): edit the copy that `design-system.md` and `pitfalls.md` name as the loaded one. If unsure which copy the page loads, trace the layout's style references before editing.
- **Registering new files:** whatever the adapter's "Registering new files" section and `pitfalls.md` require (for example every new file in an old-style project file, or a navigation config). A missed registration can silently leave the file out of the published site.
- **Tests and stories:** add them only as the adapter's "Tests and stories" section says (where the repository already has them).
- **Assets:** download every static image and icon the design uses as the design-to-code skill instructs, into the repository's asset folder; no temporary Figma asset URLs left in code; use exact assets, never redraw or substitute.
- **Copy:** text from the design, verbatim. When starting from an existing page as a base, remove every leftover of its text, names and data.
- **Accessibility basics:** `alt` on images (empty for decorative), labels on inputs, real `button` and `a` elements for controls.

## Check before reporting

Run the stack adapter's "Build checks" on the files you changed: shell purity (no data access or server calls), leftovers and escape hatches, and file registration. The scans match keywords: look at each hit, and report a hit in a comment or a harmless name as a false positive rather than rewording code to silence it. Quote file paths (route folders can contain parentheses or spaces).

Also check: every control from the plan's interaction table is wired or listed as inert; every referenced token exists in the token source; every asset file exists and is non-empty.

Follow the adapter's "Preview" section. If the app doesn't run here, don't claim it renders; say how to preview it, using `prototype.md`'s preview section.

## Finish

1. **Update the screen record** `docs/figma-workflow/screens/<screen-slug>.md` (create it from [references/screen-record.md](references/screen-record.md) if new): schema line `figma-workflow-schema: 2`, Figma link(s), placement, routes, files, today's date as last synced, inert controls, inferred behaviour.
2. **Summarise** in plain language: what was built or changed, what is inert and why, what needs backend, anything not done, and how to preview.
3. **Offer the check:** "To have the work checked independently against the design, type **`/figma-workflow:verify`**."
4. **Offer a commit** on the feature branch (show the message first). Stage only the files this build created or changed, by path; never `git add -A` or `git add .`, which can pick up secrets or someone else's work. Never push or merge; that is for the backend team.
