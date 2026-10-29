# Facts files: schema 2

The skills are generic. Everything specific to one repository lives in that repository, in the **facts directory**:

```
<repo root>/docs/figma-workflow/
```

This path is the only place the skills look. If your team moves the files, change the path in each skill's "Facts directory" line (sync, build, verify, verify-audit).

Every facts file starts with a title line and then this line, exactly:

```
figma-workflow-schema: 2
```

A skill that finds a file missing, without that line, or on a lower number stops and says which file is missing or outdated and that the repository owner has to add or update it. It never guesses the facts or writes them itself. A higher number than the skill knows: stop and say the plugin needs updating.

**From schema 1 to 2:** add the **Stack adapter** and **Code Connect** lines to `design-system.md` (below), and change the number in every file, screen records included. Nothing else is required to change.

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
- Separate mobile views, or components that render differently on the server.
- Shared layouts and menus that every screen touches.
- Things the frontend workflow must never touch (secret config files, data access, payment, auth configuration, database scripts, API routes).

### 4. `screens/<screen-slug>.md` (one per implemented screen, written by `build`)

```markdown
# <Screen name>

figma-workflow-schema: 2

- **Figma**: <frame URL>  (frame name: "<name>")
- **Other frames in this flow**: <URL — name>, ... (or "none")
- **Repository / area**: <repo folder> / <area, e.g. corporate dashboard>
- **Placement**: isolated | integrated (menu entry: <where>)
- **Route(s)**: <URL path(s)>
- **Files**: <page shell>, <data shape>, <views or components>, <styles>, <scripts>, <tests or stories, if any>
- **Last synced**: <YYYY-MM-DD> against frame version seen on that date
- **Intentionally inert controls**: <control — reason>, ... (or "none")
- **Inferred, not shown in the design**: <behaviour — basis>, ... (or "none")
- **Notes**: <anything the next sync must know>
```

Status (prototype or integrated) is **not** stored here. It is read from the code: a page that still carries the prototype marker is a prototype; one without it has been integrated by the backend team. The record is a hint for finding the screen, not proof: the Figma link the designer gives always wins, and a mismatch is surfaced, never silently resolved.

### Optional

`README.md`: one paragraph on what the repository is, which areas exist (for the placement question), and the index of the files above.
