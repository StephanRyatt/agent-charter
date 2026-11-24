# Screen record template

File: `docs/figma-workflow/screens/<screen-slug>.md`. Keep the schema line exactly.

```markdown
# <Screen name>

figma-workflow-schema: 3

- **Figma**: <frame URL>  (frame name: "<name>")
- **Other frames in this flow**: <URL — name>, ... (or "none")
- **Viewports**: <viewport>: <frame URL> | follows <reference screen> (no frame) | skipped (user's choice, <YYYY-MM-DD>) | later (noted <YYYY-MM-DD>); ... (one entry per declared viewport)
- **Repository / area**: <repo folder> / <area>
- **Placement**: isolated | integrated (menu entry: <where>)
- **Route(s)**: <URL path(s)>
- **Files**: <page shell>, <data shape>, <views or components>, <styles>, <scripts>, <tests or stories, if any>
- **Last synced**: <YYYY-MM-DD>
- **Intentionally inert controls**: <control — reason>, ... (or "none")
- **Inferred, not shown in the design**: <behaviour — basis>, ... (or "none")
- **Notes**: <anything the next plan must know>
```

Write a Viewports entry for every viewport `design-system.md` declares for the screen's area, as the plan's Viewports line says. *Skipped*: the user decided this screen doesn't get that version. *Later*: still wanted, not built yet.

Do not record prototype or integrated status: it is read from the prototype marker in the code.
