---
name: verify-audit
description: Independent, read-only audit of a frontend implementation against its Figma design (coverage, fidelity, behaviour, design-system reuse), run in a fresh context. Started only by the figma-workflow verify skill, which passes every input.
context: fork
agent: general-purpose
model: opus
effort: high
background: false
user-invocable: false
---

# Figma implementation audit (independent)

Goal: decide whether an implementation matches its design and reuses the repo's **existing** tokens, utilities, and components as much as *sensible*, and turn the gaps into a concrete remediation plan.

You run in a fresh context on purpose: you have not seen how the work was built, so re-derive every expectation from the design and the repository. **You cannot ask the user anything.** Everything you need is in the inputs below; if something essential is missing or contradictory, stop and report exactly what is missing instead of guessing.

**Inputs (from the invoking skill):** $ARGUMENTS

**Read-only.** Do not edit code, tokens, components, facts files or git state. Never open secret configuration files (for example `Web.config`, `App.config`, `.env`) or print their contents. Return the report as your final message; do not write it into the repository. Do not ask whether to execute the plan; the invoking skill does that.

**Target repository:** exactly the absolute path in the inputs' "Repository:" line, never the working directory (which may be a workspace holding several repositories). Read files and run git commands there (`git -C <path>`). If the line is missing or the path is not a git repository, stop and report it.

**Facts directory:** `docs/figma-workflow/` in the target repository. Read every file there first and check each `figma-workflow-schema:` line is `1`; if missing or different, say so in the report and audit without them, marking reuse verdicts as lower confidence.

**"Sensible" is the bar, not 100% reuse.** Reuse is sensible when the existing piece expresses the design's intent and semantics. It is *not* sensible when it would visibly break the design, need heavy overrides (`!important`, deep selectors, fighting internals), stretch a component past its purpose, or couple unrelated things. Hand-written code in those cases is a **pass**, not a finding.

## Workflow

```
- [ ] 1. Scope: Figma node + implementation target
- [ ] 2. Inventory the repo's design system
- [ ] 3. Fetch the design (context, screenshot, variables, Code Connect, metadata tree)
- [ ] 4. Figma-side inventory (every element in the frame -> implemented / placeholder / missing)
- [ ] 5. Extract what the implementation actually uses
- [ ] 6. Audit each style/component decision (reuse)
- [ ] 7. Fidelity check (render, or geometry + assets when you cannot)
- [ ] 8. Behavior and wiring check (8b: prototype boundary and legacy-stack checks)
- [ ] 9. Build the remediation plan and report
```

Reuse is only one of four questions. The audit answers all of them, in this order of risk of being forgotten:
1. **Coverage**: is everything in the design present (logos, icons, images, text, states, modals)?
2. **Fidelity**: do sizes, gaps and type match, including values the code never sets (missing margins, collapsed whitespace)?
3. **Behavior**: is every control wired or linked the way the design implies?
4. **Reuse**: are existing tokens/components used where sensible?

A clean reuse table is not a clean audit. Never give a "merge-worthy" verdict unless steps 4, 7 and 8 were actually done or are listed under "Not verified".

### 1. Scope

Take both from the inputs; if either is missing, stop and report it, never guess:
- **Figma**: `figma.com/design/:fileKey/...?node-id=1-2` → `fileKey`, `nodeId` = `1:2`. For `/branch/:branchKey/` use `branchKey` as `fileKey`.
- **Implementation**: files, component, route, PR, or branch diff. Prefer `git diff <base>...HEAD` (or the PR diff) to isolate what was *added*; pre-existing code is out of scope unless the inputs say otherwise.
- **Depth**: *scoped* (only the nodes and files named, after a build) or *full* (the whole screen, developer report). **Audience**: designer or developer.

If the Figma MCP server's tools are not available in this context, stop and report that; do not audit from the code alone and call it a design audit. Follow the server's own instructions on sessions (open a session with the file key before other file tools, and reuse its id).

### 2. Inventory the design system

Start from the facts files (`design-system.md`, `prototype.md`, `pitfalls.md`, the screen record): they are the repository's own statement of what exists. Verify the parts you rely on against the code; a fact that the code contradicts is a finding for the repository owner. Then fill gaps; do not assume. In order:
1. **Stack/styling approach**: `package.json`; Tailwind, CSS Modules, CSS-in-JS, SCSS, plain CSS, UI library (shadcn, MUI, Radix, Chakra...).
2. **Tokens**: `:root`/`[data-theme]` custom properties, `tailwind.config.*`/`@theme`, `theme.ts`, SCSS vars, `tokens.json`. Colors, spacing, radii, shadows, typography, breakpoints, z-index.
3. **Components**: `components/`, `ui/`, `design-system/`, `packages/*`, library components. Note props/variants/sizes.
4. **Utilities/primitives**: Stack/Container/Grid, typography components, utility classes, mixins.
5. **Conventions**: open 1–2 similar *existing* screens as the style reference; icon/image handling.
6. **Rules/docs**: `AGENTS.md`, `CLAUDE.md`, `.claude/rules`, `.cursor/rules`, README, Storybook. Violations of stated rules are findings.

Use `Grep`/`Glob` on large repos.

### 3. Fetch the design

- Load the Figma plugin's design-to-code skill before requesting design context, as that skill requires (usually named `figma:figma-design-to-code` when the plugin is installed; if only the MCP server is present, the skill it serves as a resource). If neither is available, follow the server's instructions directly and note it under "Not verified".
- Design context (reference only, never final code), a screenshot if none returned, variable definitions, and Code Connect mappings. Code Connect mappings are authoritative.
- Note whether Figma itself uses variables/styles/library components or raw/detached values. Off-system Figma is a **design-side** finding, not an implementation defect.

### 4. Figma-side inventory (coverage)

Start from the design, not the code. Get the metadata tree for the node (save large output to a file and read it in windows) and walk the tree. For every visible (not `hidden="true"`) text, icon instance, image/logo instance, input, button, toggle, tab, table column, modal and state variant, record one line: **implemented / placeholder / missing**, with the implementation `path:line`.

- **Placeholders count as gaps**: initials instead of a logo, a lorem string, a generic icon, a text stand-in for an image. Flag them even if the code is clean.
- **Assets/content**: for each logo, image and icon, say where the asset comes from (exported from Figma, already in the repo, missing). Check variants (e.g. component properties like `Property 1=<brand name>`) that imply per-item artwork.
- **Frames not rendered by the screen**: list every sibling frame (other states, modals, empty/error states) and whether it is reachable in the implementation.
- Take a screenshot per region (filter bar, table rows, modal) to compare against the implementation.
- **Copy**: every text string matches the design verbatim; flag leftovers from a page the screen was copied from (other names, places, sample text).

### 5. Extract what the implementation uses

From the in-scope files, collect every: component usage (and props), token reference, utility class, raw color/px/rem/font value, inline `style`, new CSS rule/file, new token, new component, `!important`/deep-selector override, absolute/fixed positioning, and any edit to shared tokens/components. Run the mechanical scans in [reference.md](reference.md) to make this exhaustive. Cite `path:line` for each.

### 6. Audit (reuse)

Build one table mapping each design element/value to what the implementation did, then classify:

| Verdict | Meaning |
|---|---|
| **Reused** | Correct existing token/component used. |
| **Should reuse** | An exact/semantic match exists but was bypassed. Finding. |
| **Nearest-match drift** | Token used or available is within ~1 scale step of the Figma value. Flag value drift; recommend the token unless the user wants strict fidelity. |
| **Wrong semantic token** | Value matches but role is wrong (e.g. `text/secondary` mapped to a brand color). Finding. |
| **Duplicate** | New component/style/token duplicates an existing one. Finding. |
| **Justified new** | No sensible match; built cleanly in the repo's style. Pass. |
| **Unjustified new/one-off** | Hardcoded value or new token without a reason, or a single-use token. Finding. |
| **Design-system gap** | Value recurs or is a legitimate variant; belongs in the token/component source. Recommendation. |
| **Design-side** | Figma uses off-system values; needs a designer decision. |

Check specifically:
- **Code Connect**: mapped components used at their mapped node?
- **Component reuse**: hand-rolled markup equivalent to an existing component/variant (buttons, inputs, cards, modals, badges, icons, typography)?
- **Token reuse**: hardcoded color/spacing/radius/shadow/font/breakpoint where a token exists?
- **Semantics**: right token for the *role*, not just the value?
- **Override health**: component reuse that needs heavy overrides (maybe the "should reuse" call is wrong; maybe extend with a variant instead).
- **Styling approach**: parallel stylesheet, inline styles, second CSS paradigm, ignoring repo rules.
- **Layout**: absolute positioning copied from Figma instead of flex/grid/primitives.
- **Shared impact**: edits to shared tokens/components that change other screens (should be additive).
- **New tokens**: recurring and system-worthy, or single-use noise?
- **Interactive/a11y basics** where reuse affects them (reused components carry states/focus; hand-rolled ones often drop them). Wiring itself is covered in step 8.

Separate **findings** (backed by `path:line` evidence) from **hypotheses** (e.g. "this override is probably unnecessary"). Label each.

### 7. Fidelity check

Reuse must not cost fidelity. If the inputs give a preview URL, or the app can be run here, render it with whichever browser tool is available (Claude Desktop's built-in browser or Claude in Chrome) and compare against the Figma screenshot: layout, spacing, type, color, assets, states. Never sign in or enter credentials; if the page needs a login the browser doesn't already have, treat it as not rendered. Many legacy server-rendered stacks don't run on every OS; don't try to install or build one. Record where an existing token's drift is visible.

**If you cannot render it, "not rendered" is not the end of the step.** Compensate with a geometry comparison and say it is source-derived, not visual:
1. From the metadata tree, compute for each repeated pattern: element sizes, gaps between siblings (next.x - (prev.x + prev.width)), icon-to-label offsets, paddings, row heights, column widths.
2. For each, trace the implementation: the CSS that sets it, *and the CSS that does not*. Check inherited/global rules (e.g. a shared `::after` icon with no margin), `display` modes, whitespace between inline elements in the markup (`>Label</button>` vs a line break), and component default paddings.
3. List mismatches as findings with Figma value vs code-derived value. Where the answer depends on rendering, put it under "Not verified".

Never claim visual verification without rendering.

### 8. Behavior and wiring check

Figma often has no navigation prototype, so intended behavior is inferred. Do both:
1. **Prototype links in Figma**: scan reactions/interactions in the node (from the design context, or a read-only query if the server offers one). Record real navigation/overlay/open-url links versus hover-only states. If none exist, say "no prototype links; behavior inferred".
2. **Control table**: list every control in the design (buttons, icon buttons, row menus, tabs, toggles, filters, sort, pagination, modal open/close/submit, links, breadcrumbs). For each: expected behavior (from prototype or clear semantics), what the implementation does (`path:line` of handler/href/route), and status:
   - **wired**: does what the design implies, against real data or the server;
   - **wired (local)**: on a prototype page, does it visibly in memory (adds the row, filters the list, shows a local Save confirmation). This is correct for a prototype, not a finding;
   - **inert (listed)**: the screen record or plan lists it as intentionally inert;
   - **stub**: closes a menu, `href="#"`, no-op, and not listed;
   - **unwired**: markup with no handler;
   - **intent unknown**.
3. Intent-unknown controls are design-side follow-ups ("ask design where X goes"), not silently out of scope.

Run the unwired-control scans in [reference.md](reference.md). Stubs that are not listed are findings; listed inert controls are not.

### 8b. Prototype boundary and legacy-stack checks

- **Prototype or integrated**: read the prototype marker convention from `prototype.md`. A page with the marker is a prototype; one without it is integrated by the backend team.
- **Shell purity** (prototype pages): the controller returns only hardcoded sample data (no service, data context, repository or handler; no POST actions), and the page script makes no server calls. Any of these is a **High** finding: the frontend workflow must not do backend work.
- **Sample data** (prototype pages): view-model properties mirror the source entities' names and types for the fields shown; sample values respect their maximum lengths and nullability; the data includes the longest allowed values, empty optional fields, an empty list and a long list. Missing edge cases are **Med** findings (the design's empty and overflow states go untested). No real-looking personal data, no text copied from another page.
- **Marker present** on every new prototype shell; authorization attribute present (its roles are for the backend team to confirm: list them).
- **Integrated pages**: changes are presentation-only; flag any edit to data wiring, server handlers or view-model properties.
- **Project file**: in old-style project files that list contents, every new view, stylesheet, script, image and class is listed (unlisted files are silently left out of the published site, or don't compile).
- **Duplicated stylesheets**: the edited copy is the one the page loads.
- Run the legacy-web scans in [reference.md](reference.md).

### 9. Remediation plan and report

Use the template in [reference.md](reference.md). Plan rules:
- Include coverage, fidelity and wiring fixes, not only reuse fixes. Order to maximize code removed and risk reduced: (1) missing/placeholder elements and assets, (2) Code Connect/component swaps, (3) token substitutions, (4) removing duplicates and parallel styles, (5) layout and spacing fixes, (6) wiring of stubbed/unwired controls, (7) additive design-system additions (new variants/tokens, only when justified), (8) design-side follow-ups.
- Each item: location, finding, evidence, **specific** fix (name the exact token/component/variant), risk to fidelity or other screens, effort (S/M/L), and how to verify.
- Never recommend a fix that breaks fidelity or needs heavy overrides just to hit reuse; say "keep as is" with the reason.
- Keep shared-code changes additive; call out anything that touches other screens.
- Do not execute the plan, and do not ask the user anything: the invoking skill presents the report.
- **Designer audience**: put the "For the designer" section of the template first (plain language, top issues, the design-side to-do list for Figma), then the full report.
- **Scoped depth**: audit only the named nodes and files, and list everything outside that scope as not checked.

## Anti-patterns

- Flagging every hardcoded value without checking if a token sensibly applies.
- Matching by raw value only; ignoring semantic role.
- Penalizing justified one-offs or demanding reuse that needs `!important`.
- Auditing pre-existing code outside the diff/scope.
- Vague fixes ("use tokens") instead of naming the token/component.
- Editing code during the audit.
- Presenting hypotheses as findings, or claiming visual verification without rendering.
- Auditing only from the implementation outward (diffing your own CSS) and never walking the Figma tree.
- Treating "app not rendered" as the end of fidelity checking instead of falling back to geometry and source tracing.
- Missing absent values: scans find wrong values that exist, not margins, assets or handlers that don't.
- Accepting placeholders (initials for logos, text for icons, stub handlers) as "justified" without listing them as gaps.
- Declaring behavior out of scope because Figma has no prototype links; list controls as "intent unknown" instead.
- Auditing code you wrote earlier with the same assumptions; re-derive expectations from the design.
