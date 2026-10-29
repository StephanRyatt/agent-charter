# Clickable frontend, no backend

**Goal:** the designed screens feel real inside the app's own shell and login, with no persistence and no server calls. Reloading resets everything.

## Boundary

| The frontend workflow builds | The backend team builds |
|---|---|
| Views (templates), stylesheets, page scripts, static assets | Data access, services, saving, real data |
| A thin page shell: a controller action that returns the view with **hardcoded sample data**, and a view model that describes that data | Business rules, validation on the server, server calls from the page |
| Links between the designed screens | Authorization decisions (the role attribute is copied from a similar page and flagged for their confirmation) |
| The prototype marker on every new shell | The guard behind the marker, promotion (removing the marker) |
| Project-file entries for the new files | Configuration, database scripts, pipelines, payment, authentication |

A shell controller never calls a service, data context, repository or handler, has no POST actions, and reads nothing from the database. A page that is already integrated (no marker) only gets presentation changes.

## How it works

- A thin controller action returns a view, with hardcoded sample data from a small view model. It never calls an application service, EF/ORM, or a handler.
- The page sits in the existing layout and gets the normal login and role check, so it looks and loads like a real page. The prototype marker from `prototype.md` goes on the controller.
- One page-level script file holds all interaction as in-memory state: arrays for lists, plus show/hide for tabs and panels.

## What each control does

- **Navigation:** real links between the designed screens (list → editor, Cancel → list).
- **Filters, search, sort, paging:** run over the in-memory array and redraw.
- **Create, edit, delete:** change the array or the DOM, then close the modal or redraw.
- **Save buttons:** show a visible local confirmation only. They do not post.
- **Tabs, section navigation, language tabs:** toggle which panel is visible.
- **Modals:** open and fill them; enable or disable Save based on required fields.
- **Controls the design shows but gives no behaviour for:** highlight them on interaction and show no extra form. Do not invent content. List them as intentionally inert.

## Rules

- Every control either does something visible or is listed as intentionally inert.
- No AJAX, no form posts, no calls to any real data layer.
- Escape user text before putting it into HTML (use text APIs, not HTML insertion, for user values).
- Render repeated rows and action markup from one template, not by copying an existing row.
- Use the layout's real script and style sections, and check that shared libraries (for example jQuery, Bootstrap) load before the page script.
- No `debugger` statements, `console.log` noise, or commented-out blocks left behind.
- Sample data is obviously sample data (plausible, but never real customer names or text copied from another page).
