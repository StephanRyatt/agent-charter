# Facts files: schema 3

The skills are generic. Everything specific to one repository lives in that repository, in the **facts directory**:

```
<repo root>/docs/figma-workflow/
```

This path is the only place the skills look. If your team moves the files, change the path in each skill's "Facts directory" line (plan, build, verify, verify-worker).

Every facts file starts with a title line and then this line, exactly (blank lines between them are fine). The `screens/` folder may be missing until the first screen is built; that is not an error:

```
figma-workflow-schema: 3
```

A skill that finds a file missing, without that line, or on a lower number stops and says which file is missing or outdated and that the repository owner has to add or update it. It never guesses the facts or writes them itself. A higher number than the skill knows: stop and say the plugin needs updating.

**From schema 1 to 2:** add the **Stack adapter** and **Code Connect** lines to `design-system.md` (below), and change the number in every file, screen records included. Nothing else is required to change.

**From schema 2 to 3:** add the **Viewports** section to `design-system.md` (below), and change the number in every file, screen records included. Existing screen records need no Viewports line: `verify` reports a viewport missing from such a screen as pre-existing, not as a finding, and the next `plan` for that screen asks about it. Plugin 0.6.0 and later read only schema 3. Earlier versions' `plan` and `build` stop on it, but their `verify` audits without the facts and misses the viewports, so update the files and every user's plugin together.

## Terms

The skills use stack-neutral words. Each repository's facts say what they mean there.

- **Page shell**: the code that renders one page with hardcoded sample data. A controller action and its view in a server-rendered app; a page or route component in a component framework.
- **Data shape**: the type the page shell passes to the page. A view model, or a props or TypeScript type.
- **Prototype marker**: how a page is marked as a prototype. An attribute, a feature flag, a route guard or an environment check.
- **Data model**: where the app's real data is described. ORM models or entity files, a database schema, migrations, API types or generated types.
- **Stack adapter**: one of the plugin's stack files, which says how the generic steps apply to a kind of stack.

## The four files

### 1. `design-system.md` (required)

What exists in the repository, so nothing is rediscovered or invented per run. It starts, right after the schema line, with these two lines exactly as shown (one value each):

```
- **Stack adapter**: legacy-server-rendered | modern-component
- **Code Connect**: set up | not set up
```

- **Stack adapter**: `legacy-server-rendered` for server templates with page scripts (Razor/MVC, Django or Rails templates, PHP, jQuery, Bootstrap). `modern-component` for component frameworks (React, Vue, Svelte, Next.js, Nuxt). The skills load the matching file from the plugin's `references/stacks/`. Any other value: the skills stop and say so.
- **Code Connect**: whether the Figma library's components are mapped to this repository's components with Figma Code Connect. When it is `set up`, its mappings win over the mapping notes below. When it is `not set up`, the skills don't offer to set it up, and they decline the Figma server's offers to connect components on their own. See the plugin's `references/code-connect.md` for how a project adopts it.

Then:

- **Stack**: framework, view or component layer, CSS approach, JS libraries and versions, icon and image handling.
- **Tokens**: where they are defined (CSS custom properties, a Tailwind config or theme, SCSS variables, a tokens file), naming, the main colour, spacing, radius, shadow and type tokens, and known gaps (values the design uses that have no token).
- **Components and patterns**: reusable components, partials, classes or helpers with their variants (buttons, inputs, tables, modals, badges, cards, tabs, empty states), each with its path and one example usage. Name the Storybook if there is one.
- **Layouts**: which layout each area uses, and how a page adds its own styles and scripts.
- **Stylesheets**: which files are canonical, and every stylesheet that exists as several copies (path of each copy, which one the pages actually load).
- **Reference screens**: one or two existing pages that show the house style.
- **Figma mapping**: Figma library components or variables that map to repository components or tokens.
- **Viewports** (required): see below.

#### Viewports

Every viewport the repository supports, so `plan`, `build` and `verify` cover each one. A desktop-only repository declares one viewport. One entry per viewport, with:

- **Name and width**: a name and a width or width range, for example "phone, up to 767px".
- **Served by**: CSS breakpoints in the same page | a separate view or component the server picks | a separate route or host.
- **Requested by** (for anything but CSS breakpoints): how to get that version, for example a user-agent string, a cookie, a query switch, or the host or route.
- **Tells apart**: a visible sign or source marker that shows which version is on screen, for example a layout class on the page's root element.
- **Per screen** (for a version the server picks): the file or registration that must exist for each screen, so it can be checked in the source without rendering, for example a sibling view named by a suffix.
- **Figma frames**: where its frames usually live (a page, or a naming convention), or "no convention".
- **No frame**: the rule when Figma has no frame for it: follow reference screen `<path>` | ask the designer per screen | not supported (without a frame, the screen doesn't get that version).
- **Areas** (optional): the areas the entry applies to. Default: the whole repository. Use it so that, for example, a desktop-only admin area raises no phone questions.

```markdown
## Viewports

- **desktop**, 768px and up. Served by: CSS breakpoints in the same page. Tells apart: no `layout-phone` class. Figma frames: page "Desktop". No frame: ask the designer per screen.
- **phone**, up to 767px. Served by: a separate view the server picks. Requested by: a phone user-agent string. Tells apart: `layout-phone` class on `<body>`. Per screen: a `<Name>.Phone` view next to the desktop view. Figma frames: page "Mobile", frames named like the desktop ones. No frame: follow reference screen `Views/Home/Index.Phone`. Areas: all except admin.
```

### 2. `prototype.md` (required)

The no-backend prototype convention for this repository.

- **Marker**: the prototype marker used here (for example a `[PrototypeOnly]` attribute, a `prototype` feature flag, or a route guard), and whether the guard behind it is in place yet.
- **Guard behaviour**: in which environments prototype pages are reachable, and what they return elsewhere (for example 404 outside local development and a dev environment, failing closed). A visible "prototype, sample data" banner if the guard adds one.
- **Page shell**: where page shells and data shapes go, route conventions, and the authorization to copy and from which existing page.
- **Sample data**: where the data model lives, and where maximum lengths and nullability are defined. Any approved source of sanitized real records. Prototypes never read a database or call an API.
- **Navigation**: how an *integrated* prototype's menu entry is hidden where prototypes are unreachable.
- **Preview**: how the designer sees a built page (a local dev server, a preview deployment, a VM, or none), and what login it needs.
- **Promotion**: the backend step that turns a prototype into a real page (remove the marker in the same change that adds real data).

### 3. `pitfalls.md` (required)

Repository traps that break builds or fidelity silently. Examples of the kind of entry:

- Project files that must list every new file, or the file is left out of the published site.
- Stylesheets copied into several folders, where only one copy is loaded.
- Global CSS rules (icon pseudo-elements, base margins) that change spacing on new markup.
- Components that render differently on the server. (Separate phone or tablet versions are not a pitfall entry: they belong in the Viewports section of `design-system.md`.)
- Shared layouts and menus that every screen touches.
- Things the frontend workflow must never touch (secret config files, data access, payment, auth configuration, database scripts, API routes).

### 4. `screens/<screen-slug>.md` (one per implemented screen, written by `build`)

```markdown
# <Screen name>

figma-workflow-schema: 3

- **Figma**: <frame URL>  (frame name: "<name>")
- **Other frames in this flow**: <URL — name>, ... (or "none")
- **Viewports**: <viewport>: <frame URL> | follows <reference screen> (no frame) | skipped (user's choice, <YYYY-MM-DD>) | later (noted <YYYY-MM-DD>); ... (one entry per declared viewport)
- **Repository / area**: <repo folder> / <area, e.g. corporate dashboard>
- **Placement**: isolated | integrated (menu entry: <where>)
- **Route(s)**: <URL path(s)>
- **Files**: <page shell>, <data shape>, <views or components>, <styles>, <scripts>, <tests or stories, if any>
- **Last synced**: <YYYY-MM-DD> against frame version seen on that date
- **Intentionally inert controls**: <control — reason>, ... (or "none")
- **Inferred, not shown in the design**: <behaviour — basis>, ... (or "none")
- **Notes**: <anything the next plan must know>
```

In the Viewports line, *skipped* means the user decided this screen doesn't get that version, and `plan` doesn't raise it again; *later* means it is still wanted, and the next `plan` for the screen asks about it again.

Status (prototype or integrated) is **not** stored here. It is read from the code: a page that still carries the prototype marker is a prototype; one without it has been integrated by the backend team. The record is a hint for finding the screen, not proof: the Figma link the designer gives always wins, and a mismatch is surfaced, never silently resolved.

### Optional

`README.md`: one paragraph on what the repository is, which areas exist (for the placement question), and the index of the files above.
