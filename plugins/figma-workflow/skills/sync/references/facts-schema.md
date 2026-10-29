# Facts files: schema 1

The skills are generic. Everything specific to one repository lives in that repository, in the **facts directory**:

```
<repo root>/docs/figma-workflow/
```

This path is the only place the skills look. If your team moves the files, change the path in each skill's "Facts directory" line (sync, build, verify, verify-audit).

Every facts file starts with a title line and then this line, exactly:

```
figma-workflow-schema: 1
```

A skill that finds a file missing, without that line, or on a lower number stops and says which file is missing or outdated and that the repository owner has to add or update it. It never guesses the facts or writes them itself. A higher number than the skill knows: stop and say the plugin needs updating.

## The four files

### 1. `design-system.md` (required)

What exists in the repository, so nothing is rediscovered or invented per run.

- **Stack**: framework, view engine, CSS approach, JS libraries and versions (e.g. jQuery, Bootstrap), icon and image handling.
- **Tokens**: where they are defined (file path), naming, the main colour, spacing, radius, shadow and type tokens, and known gaps (values the design uses that have no token).
- **Components and patterns**: reusable partials, classes or helpers with their variants (buttons, inputs, tables, modals, badges, cards, tabs, empty states), each with its path and one example usage.
- **Layouts**: which layout each area uses, its script and style sections, and the load order of shared scripts.
- **Stylesheets**: which files are canonical, and every stylesheet that exists as several copies (path of each copy, which one the pages actually load).
- **Reference screens**: one or two existing pages that show the house style.
- **Figma mapping**: Figma library components or variables that map to repo components or tokens (Code Connect, if used, wins).

### 2. `prototype.md` (required)

The no-backend prototype convention for this repository.

- **Marker**: how a prototype page is marked (for example a `[PrototypeOnly]` attribute on the controller), and whether the guard behind it is in place yet.
- **Guard behaviour**: in which environments prototype pages are reachable, and what they return elsewhere (for example 404 outside `localhost` and `dev`, failing closed). A visible "prototype, sample data" banner if the guard adds one.
- **Sample data**: where the data model lives (entity classes, model file, where maximum lengths and nullability are defined), and any approved source of sanitized real records. Prototypes never read a database.
- **Where shells go**: controller and view-model locations, route conventions, the authorization attribute to copy and from which existing page.
- **Navigation**: how an *integrated* prototype's menu entry is hidden where prototypes are unreachable.
- **Preview**: how the designer sees a built page (a preview environment, a VM, or none), and what login it needs.
- **Promotion**: the backend step that turns a prototype into a real page (remove the marker in the same change that adds real data).

### 3. `pitfalls.md` (required)

Repository traps that break builds or fidelity silently. Examples of the kind of entry:

- Old-style project files that must list every new view, stylesheet and script, or the file is left out of the published site.
- Stylesheets copied into several folders, where only one copy is loaded.
- Global CSS rules (icon pseudo-elements, base margins) that change spacing on new markup.
- Separate mobile views selected by user-agent sniffing.
- Shared layouts and menus that every screen touches.
- Things the frontend workflow must never touch (secret config files, data access, payment, auth configuration, database scripts).

### 4. `screens/<screen-slug>.md` (one per implemented screen, written by `build`)

```markdown
# <Screen name>

figma-workflow-schema: 1

- **Figma**: <frame URL>  (frame name: "<name>")
- **Other frames in this flow**: <URL — name>, ... (or "none")
- **Repository / area**: <repo folder> / <area, e.g. corporate dashboard>
- **Placement**: isolated | integrated (menu entry: <where>)
- **Route(s)**: <URL path(s)>
- **Files**: <controller>, <view model>, <views>, <stylesheet>, <script>
- **Last synced**: <YYYY-MM-DD> against frame version seen on that date
- **Intentionally inert controls**: <control — reason>, ... (or "none")
- **Inferred, not shown in the design**: <behaviour — basis>, ... (or "none")
- **Notes**: <anything the next sync must know>
```

Status (prototype or integrated) is **not** stored here. It is read from the code: a page that still carries the prototype marker is a prototype; one without it has been integrated by the backend team. The record is a hint for finding the screen, not proof: the Figma link the designer gives always wins, and a mismatch is surfaced, never silently resolved.

### Optional

`README.md`: one paragraph on what the repository is, which areas exist (for the placement question), and the index of the files above.
