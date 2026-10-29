# Reference: scans and report template

## Mechanical scans

Run against the in-scope files only (changed files or the target directory). Get changed files with `git diff --name-only <base>...HEAD`. Use `rg`; adapt globs to the repo's file types. Paths can contain spaces or parentheses (route groups such as `app/(prototype)/`): build `FILES` as an array (`mapfile -t FILES < <(...)`) and pass `"${FILES[@]}"`. Hits are keyword matches; check each before calling it a finding.

```bash
FILES=$(git diff --name-only --diff-filter=AM <base>...HEAD | rg '\.(css|scss|sass|less|tsx?|jsx?|vue|svelte|astro|html)$')

# Hardcoded colors
rg -n '#[0-9a-fA-F]{3,8}\b|\b(rgb|rgba|hsl|hsla|oklch|oklab)\(' $FILES

# Hardcoded lengths and font values (px/rem/em in style rules)
rg -n '\b\d+(\.\d+)?(px|rem|em)\b' $FILES
rg -n 'font-(family|size|weight)|line-height|letter-spacing' $FILES

# Inline styles and escape hatches
rg -n 'style=\{\{|style="|!important|:global\(|::v-deep|>>>' $FILES

# Arbitrary Tailwind values (bypass the scale)
rg -n '\[[#0-9a-zA-Z.%-]+(px|rem|em|%)?\]' $FILES | rg '(bg|text|p|m|w|h|gap|rounded|border|top|left|right|bottom|inset|z)-\['

# Absolute/fixed positioning copied from Figma
rg -n 'position:\s*(absolute|fixed)|\b(absolute|fixed)\b' $FILES

# New stylesheets or token definitions
git diff --name-status --diff-filter=A <base>...HEAD | rg '\.(css|scss|sass|less)$'
git diff -U0 <base>...HEAD | rg '^\+\s*(--[\w-]+\s*:|\$[\w-]+\s*:|@theme)'

# Edits to shared code (potential cross-screen impact)
git diff --name-only <base>...HEAD | rg -i '(tokens?|theme|tailwind\.config|design-system|ui/|components/(ui|common|shared)|globals?\.css|:root)'
```

### Scans for what is missing (coverage, spacing, wiring)

Scans above find wrong values that exist. These look for things that are absent or stubbed. The stack adapter adds the stack's own control and handler scans.

```bash
# Placeholder content standing in for assets/icons
rg -n -i 'initials|placeholder|lorem|todo|tbd|dummy|sample' $FILES

# Stub or dead links/buttons
rg -n 'href="#"|href=""|javascript:void|onclick=""' $FILES

# Controls and their handlers: see the stack adapter's audit scans

# Inline label directly against closing tag with an ::after/icon rule: zero gap
rg -n '>[^<\s][^<]*</button>' $FILES
rg -n -g '*.css' '::after|:after' <global style dirs> | rg -v 'margin'

# Images/logos: referenced files that do not exist in the repo
rg -n -o '(src|url)\(?=?["\x27]?[^"\x27) >]+\.(png|jpe?g|svg|webp)' $FILES
```

### Stack-specific scans

Run the "Audit scans" section of the stack adapter (`references/stacks/<adapter>.md` in the plugin). They cover shell purity, escape hatches, control-to-handler wiring, file registration and the stack's typical leftovers.

Manual cross-check (always do it): take the Figma control list from step 8 and tick each against a handler/href/route. An id with markup but no handler is **unwired**; a handler that only closes a menu is a **stub**.

Geometry spot-check recipe (when not rendering): for each repeated pattern in the metadata tree, compute `gap = next.x - (prev.x + prev.width)` and `label_to_icon = icon.x - (label.x + label.width)`, then trace the implementation for the rule that produces that distance. If no rule produces it, the distance is whatever whitespace/defaults give, which is usually 0 or a few px off.

For each hit, check whether a token or component exists (grep the token source for the value, e.g. the hex or px). Not every hit is a finding: one-offs that pass the "sensible" test are passes.

For a reuse metric, tally (counts only, not a gate):
- Values tokenized vs. hardcoded (colors, spacing, radius, type).
- Distinct components reused vs. hand-rolled equivalents.
- New tokens added: recurring vs. single-use.

## Report template

```markdown
# Figma implementation audit: <screen/component>

**Figma**: <url> (node <id>)  **Scope**: <files / PR / diff>  **Depth**: scoped | full  **Rendered & compared**: yes/no (<why not>)

## For the designer        (designer audience: put this first)
- **Overall**: <one or two plain sentences: does it look and behave like the design?>
- **Top issues to fix in code** (at most five, plain language, each with where it shows on screen)
- **To fix in Figma** (design-side to-do): <off-system colours or sizes, detached components, missing states, controls whose behaviour is unclear>
- **Couldn't check**: <for example "not rendered: the page needs a login">

## Verdict
<1-3 sentences covering coverage, fidelity, behavior AND reuse. Do not call it merge-worthy if any of coverage/fidelity/behavior was not checked; say which were not.>
Coverage: <x implemented / y placeholder / z missing>  Wiring: <x wired / x' wired (local) / i inert (listed) / y stub / z unwired / w intent unknown>
Reuse: components <x reused / y hand-rolled>, values <x tokenized / y hardcoded>, new tokens <n (recurring/single-use)>

## Coverage (Figma-side inventory)
| Figma element (node id) | Type | Status (implemented / placeholder / missing) | Implementation (path:line) | Asset source |
|---|---|---|---|---|
Frames/states not reachable in the implementation: <list or "none">

## Fidelity (geometry / visual)
Method: rendered & compared | source-derived only (not rendered)
| Pattern | Figma value | Implementation-derived value | Match? | Cause (path:line) |
|---|---|---|---|---|

## Behavior and wiring
Prototype links in Figma: <real links | hover-only | none; behavior inferred>
| Control (node id) | Expected behavior | Implementation (path:line) | Status (wired / wired (local) / inert (listed) / stub / unwired / intent unknown) |
|---|---|---|---|

## Mapping (reuse)
| Figma element/value | Implementation (path:line) | Verdict | Note |
|---|---|---|---|

## Findings (evidence-backed)
1. **[High|Med|Low] <title>** — `path:line`
   Evidence: <what the code does>. Existing: `<token/component>` (<where defined>).
   Why it matters: <duplication, drift, a11y/state loss, theming breakage...>

## Hypotheses (unverified)
- <item and how to confirm>

## Justified deviations (passes)
- <hand-written/new item> — <why reuse isn't sensible>

## Design-side / design-system gaps
- <Figma off-system values, or recurring values that belong in the token source>

## Remediation plan
| # | Fix (specific) | Location | Risk | Effort | Verify |
|---|---|---|---|---|---|
| 1 | Replace hand-rolled `<div class="btn">` with `<Button variant="secondary" size="sm">` | `path:line` | Low | S | Re-render; compare screenshot |

Order: missing/placeholder elements and assets → component swaps → token substitutions → duplicate/parallel-style removal → layout and spacing fixes → wiring of stubs/unwired controls → additive system additions → design-side follow-ups.

## Not verified
<unrunnable app, missing states/breakpoints in Figma, assumptions. Always state explicitly: whether visual rendering happened, whether geometry was checked, and which controls have unknown intent.>

```

Severity guide: **High** = duplicates a core component or bypasses theming/tokens broadly, or loses states/a11y; **Med** = repeated hardcoded values with an exact token available, wrong semantic token; **Low** = single nearest-match drift, minor one-offs.
