---
name: build
description: Implements the plan that the figma-workflow sync skill wrote and the user approved, in the same chat. Run only when the user types the build command after a sync plan.
effort: high
disable-model-invocation: true
---

# Figma build: implement the approved plan

Typing this command is the user's approval of the most recent plan that the `sync` skill wrote in this chat. Implement exactly that plan in this chat, so the user can watch and steer. The user is usually a designer: report progress in plain language.

**Facts directory:** `docs/figma-workflow/` in the target repository.

## Before editing

1. **Find the plan.** Use the latest plan from the sync skill in this conversation, including any changes the user asked for after it. If there is none, stop: "There's no approved plan in this chat. Start with the sync command and your Figma link." If the user's later changes were large (new frames, a different screen), ask them to run sync again instead.
2. **Re-read the facts files** (`design-system.md`, `prototype.md`, `pitfalls.md`, the screen record if any) and check their `figma-workflow-schema:` line is `1`. Missing or different: stop and say which file.
3. **Branch safety.** Run `git status` and `git branch --show-current` in the target repository.
   - On the default or a shared branch (for example `main`, `master`, `Development`, `Production`): ask with AskUserQuestion to create `figma/<screen-slug>` from it (recommended) or to stay.
   - Uncommitted changes that are not from this chat: do not stash, reset, overwrite or switch away from them. Ask with AskUserQuestion how to proceed; recommend stopping until their owner commits them.
4. **Never open secret configuration files** (for example `Web.config`, `App.config`, `.env`), and never print their contents.

## Implement

Follow the plan's build order. Ask with AskUserQuestion (never plain text) when the plan turns out wrong or a decision is missing; don't improvise a change the design doesn't show.

- **Clickable prototype:** new pages and interactions follow [references/prototype-pattern.md](references/prototype-pattern.md), including the boundary. Apply the prototype marker exactly as `prototype.md` prescribes. If `prototype.md` says the guard behind it is not in place yet, build anyway and say in the summary that the page must not be merged into a shared branch until it is.
- **Sample data:** generate it from the app's data model as the pattern's "Sample data" section says (view models mirror the entities' shapes; edge cases always included; no database, no entity references in the shell). Follow the plan's sample-data section; if the plan has none, derive it before writing the shell.
- **Integrated screens** (no marker): presentation changes only, as the plan says.
- **Reuse:** existing components, classes and tokens from the mapping table. A gap gets the fill the plan proposed, in the canonical stylesheet, as an additive variant or token. No hardcoded hex or pixel values where a token exists; no `!important`; no inline styles or `<style>` blocks in views.
- **Duplicated stylesheets:** edit the copy that `design-system.md` and `pitfalls.md` name as the loaded one. If unsure which copy the page loads, trace the layout's style references before editing.
- **Project files:** for old-style project files that list their contents (for example a `.csproj` with explicit `<Content Include=...>` and `<Compile Include=...>` items), add every new view, stylesheet, script, image, controller and view model. Without the entry the file is silently left out of the published site, or the code doesn't compile. Match the existing item style and ordering.
- **Assets:** download every static image and icon the design uses as the design-to-code skill instructs, into the repository's asset folder; no temporary Figma asset URLs left in code; use exact assets, never redraw or substitute.
- **Copy:** text from the design, verbatim. When starting from an existing page as a base, remove every leftover of its text, names and data.
- **Accessibility basics:** `alt` on images (empty for decorative), labels on inputs, real `button` and `a` elements for controls.

## Check before reporting

Run these on the files you changed (adapt to the stack):

```bash
# shell purity: no data access or server calls in new shells or page scripts
rg -n 'Service|DbContext|Repository|Entities|HttpPost|\$\.ajax|\$\.post|\$\.get\(|fetch\(|XMLHttpRequest' <new controller> <new script>
# leftovers
rg -n 'debugger|console\.log|!important|style="|<style' <changed files>
# HTML insertion of values (check each is escaped or static)
rg -n '\.html\(|innerHTML|Html\.Raw' <changed files>
# every new file is in the project file
for f in <new files>; do rg -q "$(basename "$f")" <project file> || echo "MISSING in project file: $f"; done
```

Also check: every control from the plan's interaction table is wired or listed as inert; every referenced token exists in the token source; every asset file exists and is non-empty.

The app may not run on this machine (for example a Windows-only stack). Don't claim it renders. Say how to preview it, using `prototype.md`'s preview section.

## Finish

1. **Update the screen record** `docs/figma-workflow/screens/<screen-slug>.md` (create it from [references/screen-record.md](references/screen-record.md) if new): Figma link(s), placement, routes, files, today's date as last synced, inert controls, inferred behaviour.
2. **Summarise** in plain language: what was built or changed, what is inert and why, what needs backend, anything not done, and how to preview.
3. **Offer the check:** "To have the work checked independently against the design, type **`/figma-workflow:verify`**."
4. **Offer a commit** on the feature branch (show the message first). Never push or merge; that is for the backend team.
