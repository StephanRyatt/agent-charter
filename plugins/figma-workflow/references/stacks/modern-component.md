# Stack adapter: modern-component

For component frameworks: React (Next.js, Remix, Vite), Vue (Nuxt), Svelte (SvelteKit) and similar. The repository's facts files win over anything here.

## Page shell

- A **page or route component** (for example `app/<route>/page.tsx` in the Next.js app router, `pages/<route>.vue` in Nuxt, `src/routes/<route>/+page.svelte`) that renders the screen's components with hardcoded sample data. It imports the sample data from a file next to it (for example `sample-data.ts`).
- The **prototype marker** goes where `prototype.md` says. Common forms: a route guard in the page or its layout (for example `if (!isPrototypeEnabled()) notFound()` in Next.js), a feature flag checked the same way, a route group or folder for prototype pages (for example `app/(prototype)/`) guarded by its layout, or middleware that blocks a path prefix. Use exactly the form `prototype.md` names, never a new one.
- Reuse the existing layout and its authentication, so the page loads like a real one. Copy the access check from the most similar existing page and list it for the backend team to confirm.
- A shell can still be `async` to read route or query parameters (for example `await searchParams` in Next.js 15 for the `?state=` switch). That is not data fetching.
- In frameworks that render on the server: the shell does no data fetching on the server either. No loaders or `getServerSideProps` that read data, no server actions, no route handlers, no database client.

## Data shape and data model

- **Data shape**: a TypeScript type or interface for the page's data (or prop types in plain JS), next to the sample data. Components take what they show as props.
- **Data model**: wherever the real data is described. ORM schemas (Prisma `schema.prisma`, Drizzle tables, TypeORM entities), validation schemas (Zod, Yup), generated API types (OpenAPI, GraphQL codegen), or the backend's types. Maximum lengths and nullability come from the schema (`@db.VarChar(120)`, `varchar(..., { length })`, `.max()`, `optional`/`nullable`, `?`).
- Mirror the shape: same field names and types as the data model for the fields shown. Import a *type* from the data model only if the repository already shares types between backend and frontend; never import the ORM client or a data-access module.

## Interaction code

- Interaction lives in the page's client components as local state (`useState`/`useReducer`, Vue `ref`/`reactive`, Svelte stores scoped to the page): arrays for lists, flags for tabs, panels and modals.
- Mark only the components that need it as client components (for example `'use client'` in Next.js), as low in the tree as practical.
- No `fetch`, no data-fetching hooks against real endpoints (`useQuery`, SWR) and no form actions that post. Save buttons show a local confirmation only.
- Frameworks escape text by default. Never use `dangerouslySetInnerHTML`, `v-html` or `{@html}` for user values.
- Render lists with `map`/`v-for`/`{#each}` and stable keys, never index keys for editable lists.

## Styles and tokens

- Use the repository's styling approach only: Tailwind classes from its configured theme, CSS Modules, CSS-in-JS from its theme, or CSS custom properties. Never introduce a second one.
- Tokens: the Tailwind theme (`tailwind.config.*`, or `@theme` in CSS for Tailwind 4), CSS custom properties, or the CSS-in-JS theme object. No arbitrary values (`bg-[#1a73e8]`, `p-[13px]`) where a theme value exists; no inline `style` for values a token covers.
- A gap gets an additive token or theme entry in the canonical file, as the plan proposes.

## Components

- Reuse the repository's components (`components/ui/`, `components/`, a design-system package) and the UI library it already uses (shadcn/ui, MUI, Radix, Chakra, Vuetify...). Pass variants and props; don't fork a component to restyle it.
- New components go where similar ones live, small and prop-driven, with the data shape as their props.
- When Code Connect is set up, the mapped component at each mapped node is the answer.
- Intentionally inert controls: render the normal component with no handler, and list them as inert; the audit's handler scan will show them as unhandled, which the list explains.

## Registering new files

- Usually nothing to register: the framework picks up routes from the folder structure. Check `design-system.md` for exceptions (a route list, a navigation config, barrel `index.ts` exports the repository relies on, a Storybook config that lists stories).

## Build checks

Run on the files the build changed. Hits are keyword matches: a comment naming the data model it mirrors is fine. Route folders can contain parentheses (`app/(prototype)/`), so quote paths or use an array (`mapfile -t FILES < <(git diff --name-only ...)`, then `"${FILES[@]}"`).

```bash
# Shell purity: no data access or server calls in the page, its components or its sample data
rg -n 'fetch\(|axios|useQuery|useSWR|getServerSideProps|loader\s*\(|"use server"|\x27use server\x27|prisma|drizzle|createClient|@/lib/db|from ["\x27].*(db|api|server)["\x27]' <new and changed files>
# Leftovers and escape hatches
rg -n 'debugger|console\.log|!important|style=\{\{|dangerouslySetInnerHTML|v-html|\{@html' <changed files>
# Arbitrary Tailwind values (bypass the theme)
rg -n '(bg|text|p[xytrbl]?|m[xytrbl]?|w|h|gap|rounded|border|shadow)-\[[^\]]+\]' <changed files>
# Types and lint, if the repository has them (use its own scripts from package.json; don't invent new ones)
```

If `package.json` has `typecheck`, `lint` or `test` scripts, run the ones that are fast and say what they reported. Don't add new tooling.

## Audit scans

```bash
# Prototype shell purity (High on a prototype page)
rg -n 'fetch\(|axios|useQuery|useSWR|getServerSideProps|loader\s*\(|use server|prisma|drizzle|createClient|from ["\x27].*(db|api|server)["\x27]' $FILES

# Escape hatches and leftovers
rg -n 'dangerouslySetInnerHTML|v-html|\{@html|debugger|console\.(log|debug)' $FILES

# Inline styles and arbitrary values where theme values exist
rg -n 'style=\{\{|:style=|style="' $FILES
rg -n '(bg|text|p[xytrbl]?|m[xytrbl]?|w|h|gap|rounded|border|shadow)-\[[^\]]+\]' $FILES

# Controls and their handlers (diff the two lists)
rg -n -o '<(button|a|Link|select|input|Button)[^>]*' $FILES
rg -n -o '\b(onClick|onChange|onSubmit|@click|@change|on:click)=' $FILES

# Stub handlers
rg -n '(onClick|@click|on:click)=\{?\(?\)?\s*=>\s*\{\s*\}|href="#"' $FILES

# Index keys on lists
rg -n 'key=\{(i|index|idx)\}' $FILES

# Images without alt
rg -n '<(img|Image)(?![^>]*\balt=)[^>]*>' --pcre2 $FILES

# Forked or duplicated components: new component files whose name matches an existing one
for f in $(git diff --name-only --diff-filter=A <base>...HEAD | rg 'components/'); do
  n=$(basename "$f"); [ "$(git ls-files "*/$n" | wc -l)" -gt 1 ] && echo "DUPLICATE NAME: $f"; done
```

## Tests and stories

- If the repository has component tests (Testing Library, Vitest, Jest, Playwright component tests) and a similar page has them, add the same kind for the new components: renders with the sample data, each edge-case state renders, local interactions work. Use the repository's existing test command.
- If the repository has Storybook, add a story per new component with the sample-data states (default, empty, long, edge) next to existing stories. Don't add Storybook or a test framework where there is none.

## Preview

Usually a local dev server (`npm run dev` or the repository's own script) or a preview deployment per branch. Say which from `prototype.md`. If you can start the dev server and a browser tool is available, look at the page; otherwise say it wasn't rendered.
