# Stack adapter: legacy-server-rendered

For server-rendered templates with page-level scripts: ASP.NET MVC with Razor, and similar stacks (Django or Rails templates, PHP, server-side Java templates), usually with jQuery and Bootstrap. The repository's facts files win over anything here.

## Page shell

- A **controller action** (or view function, or route handler) that returns a **view** (template) with hardcoded sample data. One controller per screen or flow, in the folder and with the route convention `prototype.md` names.
- The **prototype marker** goes where `prototype.md` says, usually a class-level attribute on the controller (for example `[PrototypeOnly]` above the authorization attribute).
- Copy the authorization attribute (for example `[Authorize(Roles = "...")]`) from the most similar existing page in the same area, and list its roles in the build summary for the backend team to confirm.
- Sample data is built in private methods in the controller (for example `GetSample...()`). No POST actions.
- Reusable pieces of the page (modals, rows, panels) go in partial views, one per piece, following the area's existing naming (for example `_<Name>Modal.cshtml`).

## Data shape and data model

- **Data shape**: a view-model class per page, in the folder `prototype.md` names.
- **Data model**: ORM models. With Entity Framework database-first, the `.edmx` file holds maximum lengths and nullability, and the generated entity classes usually don't; search the `.edmx` by entity name instead of reading it whole. Code-first entity classes carry them as attributes or fluent configuration; migrations also show them.
- The shell references only the framework (for example `System.*` and `System.Web.Mvc`) and its own view models: entity classes are read for their shape, never referenced.

## Interaction code

- One page-level script file holds all interaction as in-memory state: arrays for lists, show and hide for tabs and panels, modals filled from the arrays.
- Load it through the layout's script section, after the shared libraries. Check which jQuery build the layout loads: a *slim* build has no `$.ajax` and no effects (`fadeIn`, `slideToggle`, `animate`), so use class toggles and CSS transitions.
- Escape user text: use `.text()` and `textContent`, not `.html()` or `innerHTML`, for user values. In views, avoid `Html.Raw` for anything a user typed.
- Render repeated rows from one template (a `<template>` element or a hidden prototype row), not by copying an existing row.

## Styles and tokens

- Tokens are usually CSS custom properties in a `:root` block of a site stylesheet. Several copies of the same stylesheet are common: edit the copy that `design-system.md` names as loaded, and trace the layout's style references if unsure.
- Page styles go in their own stylesheet, linked from the layout's style section. No inline styles or `<style>` blocks in views, no `!important`.
- Bootstrap's spacing and flex utilities usually stand in for a spacing scale. Check which Bootstrap version is actually served (the file, not the package list).

## Components

- Usually no component library: reuse means the CSS framework's classes plus the house classes in `design-system.md`, and existing partials.
- Code Connect rarely applies; mapping lives in `design-system.md`.

## Registering new files

- **Old-style project files** that list their contents (for example a `.csproj` with explicit `<Content Include=...>` and `<Compile Include=...>` items): add every new view, partial, stylesheet, script, image, controller and view model. A missing content entry is silently left out of the published site; a missing compile entry breaks the build or leaves the class out. Match the existing item style (path separators, ordering).
- Bundles: if pages load styles or scripts through bundles, register a new file in the bundle only if `design-system.md` says page files go there.

## Build checks

Run on the files the build changed:

```bash
# Shell purity: no data access or server calls in new shells or page scripts
rg -n 'Service|DbContext|Repository|Entities|HttpPost|\$\.ajax|\$\.post|\$\.get\(|\$\.getJSON|fetch\(|XMLHttpRequest' <new controller> <new script>
# Leftovers
rg -n 'debugger|console\.log|!important|style="|<style' <changed files>
# HTML insertion of values (each must be escaped or static)
rg -n '\.html\(|\.append\(|innerHTML|insertAdjacentHTML|Html\.Raw' <changed files>
# Every new file is in the project file
for f in <new files>; do rg -q "$(basename "$f")" <project file> || echo "MISSING in project file: $f"; done
```

## Audit scans

```bash
# Prototype shell purity (High on a prototype page)
rg -n 'Service|DbContext|Repository|Entities|\[HttpPost\]|\$\.ajax|\$\.post|\$\.get\(|\$\.getJSON|fetch\(|XMLHttpRequest' <shell controllers> <page scripts>

# Debug leftovers
rg -n 'debugger|console\.(log|debug)' $FILES

# Values inserted as HTML (each must be escaped or static), raw output in views
rg -n '\.html\(|\.append\(|innerHTML|insertAdjacentHTML|Html\.Raw' $FILES

# Images without alt, clickable non-buttons
rg -n '<img(?![^>]*\balt=)[^>]*>' --pcre2 $FILES
rg -n '<(div|span)[^>]*\b(onclick|data-toggle|data-bs-toggle)=' $FILES

# Inline style blocks and !important fixes in views
rg -n '<style|style="|!important' $FILES

# Controls in markup, and the handlers bound to them (diff the two lists)
rg -n -o '<(button|a|select|input)[^>]*\b(id|data-action)="[^"]+"' $FILES
rg -n -o '\$\(\s*["\x27][#.][\w-]+["\x27]\s*\)\s*\.(on|click|change)\b|\.on\(\s*["\x27]\w+["\x27]\s*,\s*["\x27][^"\x27]+["\x27]' $FILES

# Handlers that only close or hide something (likely stubs)
rg -n -B1 -A3 '\.(on|click)\(' $FILES | rg -i 'hide|dropdown\(.close|removeClass\("show"\)'

# New files missing from an old-style project file that lists contents
for f in $(git diff --name-only --diff-filter=A <base>...HEAD); do
  rg -q "$(basename "$f")" <project file> || echo "NOT IN PROJECT FILE: $f"; done

# Duplicated stylesheets: same file name in several folders (which copy did the change touch, which does the layout load?)
git ls-files '*.css' | xargs -n1 basename | sort | uniq -d

# Copied-page leftovers: renames and copies, then grep the new file for the old page's names and text
git diff <base>...HEAD -M --stat | rg '=>'
```

## Tests and stories

Usually none. Don't invent test commands; say the page is untested beyond the checks above.

## Preview

These stacks often build and run on one operating system only (for example Windows with Visual Studio). Don't try to install or build one. Say how to preview from `prototype.md`, and don't claim the page renders.
