# Code Connect

Figma Code Connect links components in a Figma library to the components in a code repository. With it, Figma's design context names the real component and its props instead of generating new markup.

figma-workflow works with and without it. `design-system.md` says which applies, with its `Code Connect` line.

## When it is set up

- Read the mappings for every frame (the Figma server's Code Connect map). For a mapped component, use the mapped repository component at that node. The mapping wins over the mapping notes in `design-system.md`, and over a value match.
- A mapped component used where the design shows it is "exact". Hand-written markup in its place is a finding.
- If a mapping points to a component that no longer exists in the repository, say so as a design-system item for the repository owner. Don't guess a replacement.
- The skills never add, change or publish mappings themselves. Those calls write to the Figma file. Mapping is a separate, deliberate task (below).

## When it is not set up

- Don't call the Code Connect tools, and don't offer to set it up during a sync or build.
- If the Figma server or its design-to-code skill asks whether to connect code components, or suggests mappings, decline on the user's behalf without asking them, and carry on with the mapping table. Say once in the plan: "Code Connect isn't set up for this repository, so components were matched from the facts files."
- Matching then comes from the `Figma mapping` and `Components and patterns` sections of `design-system.md`, by role first.

## How a project adopts it

A one-time task for a developer with edit rights on the Figma library, not part of a screen sync:

1. Check the plan: Code Connect needs a Figma plan and seat that include Dev Mode, and a published component library.
2. Pick the components that recur most (buttons, inputs, badges, cards, modals). Mapping a few common ones pays off more than mapping everything.
3. Map them, either with Figma's own Code Connect tooling (the Code Connect CLI and its config file in the repository), or in Claude Code with the Figma plugin's Code Connect skill (`figma:figma-code-connect`, or the skill the Figma MCP server serves). Review each mapping's props against the component's real variants.
4. Commit the Code Connect files with the components they describe, so mappings change in the same review as the code.
5. Change `design-system.md` to `- **Code Connect**: set up`, and trim its `Figma mapping` section to what Code Connect does not cover (variables, tokens).

Server-rendered template stacks usually have few reusable components to map; their mapping lives mostly in `design-system.md`.
