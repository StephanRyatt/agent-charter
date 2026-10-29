# Clickable frontend, no backend

**Goal:** the designed screens feel real inside the app's own layout and login, with no persistence and no server calls. Reloading resets everything.

This file is stack-neutral. The stack adapter named in `design-system.md` says what each part is in this repository (its "Page shell", "Data shape and data model" and "Interaction code" sections).

## Boundary

| The frontend workflow builds | The backend team builds |
|---|---|
| Views or components, stylesheets, interaction code, static assets | Data access, services, saving, real data |
| A thin **page shell** that renders the page with **hardcoded sample data**, and the **data shape** that describes that data | Business rules, server-side validation, server calls from the page, API routes |
| Links between the designed screens | Authorization decisions (the access check is copied from a similar page and flagged for their confirmation) |
| The **prototype marker** on every new page shell | The guard behind the marker, and promotion (removing the marker) |
| Whatever registration the stack needs for new files (the adapter's "Registering new files") | Configuration, database scripts, pipelines, payment, authentication |

A page shell never calls a service, data context, repository, ORM client, API or server action, accepts no posted data, and reads nothing from a database. A page that is already integrated (no marker) only gets presentation changes.

## How it works

- The page shell renders the page with hardcoded sample data typed by its data shape. It never touches a database or an API.
- The page sits in the existing layout and gets the normal login and access check, so it looks and loads like a real page. The prototype marker goes exactly where `prototype.md` says.
- All interaction is in-memory state in the page's own interaction code: arrays for lists, plus show and hide for tabs, panels and modals.

## Sample data, generated from the data model

No developer is needed and no database is read. The sample data comes from the app's own data model:

1. **Find the entities** the screen shows in the data model `prototype.md` names (ORM models, a schema file, migrations, API types). Search by entity name; don't read a huge model file whole. Never open configuration files for connection strings.
2. **Read their shape**: field names and types, maximum lengths, which fields can be empty (nullable, optional or not required), enumerations and lookups, relations the screen shows.
3. **Mirror the shape in the data shape**: same field names and types as the entity for every field the screen shows, so promotion is a swap of the data source, not a rewrite. Include the entity's id even when it isn't shown, as the key for lists and row actions. Fields the design shows that no entity has: name them clearly and list them under "needs backend".
4. **Generate realistic sample data** that respects those types and lengths (plausible names, dates, amounts; never real customer data or text copied from another page), and always include edge cases:
   - the longest allowed values for names and texts (at the maximum length);
   - empty or missing optional fields;
   - an empty list (the empty state);
   - a long list (enough rows to page, scroll or wrap).
5. **State switch, if cheap**: a query parameter such as `?state=empty` (or `long`, `edge`) that makes the page shell use that variant, so each state can be previewed without editing code.
6. The page shell depends only on the framework and its own data shape and sample data: the data model is read for its shape, never imported as a data-access module.

## What each control does

- **Navigation:** real links between the designed screens (list → editor, Cancel → list).
- **Filters, search, sort, paging:** run over the in-memory list and redraw.
- **Create, edit, delete:** change the in-memory list, then close the modal or redraw.
- **Save buttons:** show a visible local confirmation only. They do not post.
- **Tabs, section navigation, language tabs:** toggle which panel is visible.
- **Modals:** open and fill them; enable or disable Save based on required fields.
- **Controls the design shows but gives no behaviour for:** highlight them on interaction and show no extra form. Do not invent content. List them as intentionally inert.

## Rules

- Every control either does something visible or is listed as intentionally inert.
- No server calls of any kind (AJAX, `fetch`, data-fetching hooks, server actions, form posts) and no calls to a real data layer.
- Escape user text: never insert user values as raw HTML (the adapter names the escape hatches to avoid).
- Render repeated rows and action markup from one template or component, not by copying an existing row.
- Use the layout's real ways to add page styles and scripts, and check that shared libraries load before the page's own code.
- No `debugger` statements, `console.log` noise, or commented-out blocks left behind.
- Text the pattern forces but the design doesn't show (a no-results message, a local Save confirmation): short and neutral, and listed under "Inferred, not shown in the design" in the screen record.
- No existing access check to copy (a new app, or none on similar pages): add none, and list "access check" under "needs backend" in the summary.
- Sample data is obviously sample data (plausible, but never real customer names or text copied from another page).
