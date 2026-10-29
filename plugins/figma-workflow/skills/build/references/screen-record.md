# Screen record template

File: `docs/figma-workflow/screens/<screen-slug>.md`. Keep the schema line exactly.

```markdown
# <Screen name>

figma-workflow-schema: 1

- **Figma**: <frame URL>  (frame name: "<name>")
- **Other frames in this flow**: <URL — name>, ... (or "none")
- **Repository / area**: <repo folder> / <area>
- **Placement**: isolated | integrated (menu entry: <where>)
- **Route(s)**: <URL path(s)>
- **Files**: <controller>, <view model>, <views>, <stylesheet>, <script>
- **Last synced**: <YYYY-MM-DD>
- **Intentionally inert controls**: <control — reason>, ... (or "none")
- **Inferred, not shown in the design**: <behaviour — basis>, ... (or "none")
- **Notes**: <anything the next sync must know>
```

Do not record prototype or integrated status: it is read from the prototype marker in the code.
