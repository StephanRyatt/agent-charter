# Mapping table and plan

## Mapping table

One row per distinct design element or value that the implementation needs.

| Figma element / value | Repo equivalent | Match |
|---|---|---|
| Button "Primary / Large" | `btn btn-primary btn-lg` (`path`) | exact |
| `#1A73E8` / variable `color/brand` | `--color-brand` (`path`) | exact |
| Card radius 10px | `--radius-md` = 8px | nearest, flagged |
| Status pill "Pending" | none | gap: add a `badge--pending` variant to the badge styles |

Rules:
- **Role first.** A secondary-text colour maps to the secondary-text token even if a brand token has the same hex. A value match with the wrong role is a finding.
- **Exact**: use the existing component, class or token.
- **Nearest within about one step** of the scale (one spacing step, one type size, a near-identical colour): use the existing one and flag the drift. Use strict fidelity instead only if the difference is visible at a glance, and say so.
- **Gap** (no reasonable match): say so and propose how to fill it, preferring an additive variant or token in the canonical stylesheet over a one-off. Never hardcode silently.
- **Code Connect** mappings are authoritative when `design-system.md` says Code Connect is set up. When it isn't, match from the facts files and say so once in the plan.
- **Never** copy Figma's absolute positioning, fixed pixel layouts or generated class names. Translate to the repository's own layout (flex, grid, its utility classes).
- **Off-system Figma values** (raw hex, detached components) go to the design-side list for the designer.

## When the plan must be full

Write the full plan (all sections below) when any of these hold; otherwise the short plan (differences, mapping table, files, pitfalls) is enough:
- more than one frame, or modals, states or tabs beyond the main view;
- a new page (new route, page shell, data shape);
- changes to shared components, tokens, layouts or menus;
- more than one repository;
- anything that would need backend work to behave as designed.

## Plan template

```markdown
# Plan: <screen name>

**Figma**: <frame link(s)>  **Repository / area**: <...>  **Kind**: new | update | re-implementation
**Placement**: isolated | integrated  **Status in code**: prototype | integrated by backend | new

## What changes
<For an update: each difference — Figma node, code now (path:line), becomes. For new: one paragraph.>
Kept on purpose: <code that differs from the design for a recorded reason, or "none">

## Frames and states            (full plan)
| Frame / state | Node | Route or trigger | In scope |

## Mapping
<the mapping table>

## Interactions                 (full plan)
| Control | In the prototype it will | Or inert because |
Every control either does something visible or is listed as inert. Behaviour the design shows only by implication is marked "inferred".

## Sample data                  (new pages and new lists)
| Screen data | Source entity (model file) | Fields shown, with type, max length, can be empty | Edge cases |
Sample data is generated from the app's data model, never read from a database. Always: longest allowed values, empty optional fields, an empty list, a long list; a `?state=` switch if cheap. Fields with no entity go under "Needs backend".

## Files
| File | New / changed | What |
Include whatever the stack adapter's "Registering new files" requires (for example project-file entries), any tests or stories the adapter calls for, and name which copy of a duplicated stylesheet is edited.

## Build order                  (full plan)
Shared pieces first (tokens, component variants), then the data shape and sample data, then the page shell, then views or components, then the interaction code, then tests or stories.

## Needs backend (not built)
<behaviour that needs saving, real data, permissions or server calls: control — what it would need. Or "none".>

## Design-side items
<off-system Figma values, missing states, controls whose intent is unknown — for the designer to settle in Figma>

## Pitfalls that apply
<from pitfalls.md>

## Not covered / unknowns
<anything not readable from Figma or the code>
```
