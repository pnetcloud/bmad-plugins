---
name: core-development-react-standards
description: React standards for components, state management, performance, accessibility, styling, data fetching, and testing.
---

# React Standards

## Purpose and selection

Apply to React component implementation or review covering state, effects, rendering, accessibility, styling, and data access. Use the selected framework for routing and server data ownership; do not infer a React migration from general UI work.

## Working mode

Inspect the component tree, React/framework version, styling conventions, data-loading owner, and configured tests. Identify the requested behavior and lifecycle before editing; ask for missing interaction or data ownership decisions.

## Focus

### Components

- Prefer functional components; define typed props with interfaces.
- Keep components small and focused; lift state up when shared.
- Use composition over inheritance; avoid deep prop drilling.

### State and Effects

- Use local state for UI concerns; central store only when needed.
- Keep effects minimal; specify correct dependency arrays; clean up in `useEffect`.
- Derive state instead of duplicating; avoid unnecessary re-renders.

### Performance

- Use `React.memo`, `useMemo`, and `useCallback` judiciously.
- Provide stable keys for lists; avoid array index as key.
- Code-split large routes/components; lazy-load where appropriate.

### Accessibility

- Use semantic HTML; provide labels, roles, and ARIA where needed.
- Ensure keyboard navigation and focus management with visible focus states.

### Styling

- Follow the project's chosen styling system (CSS Modules, Tailwind, CSS-in-JS); be consistent.
- Avoid inline styles for dynamic logic-heavy styling; prefer class composition.

### Data and APIs

- Follow the framework's data-loading boundary. Without one, use the project's
  client cache or a focused hook for client-owned data; handle loading and error
  states.
- For component-owned client async work, abort obsolete requests when supported
  and appropriate, and ignore stale completions after dependency changes or
  unmount. Do not cancel mutation or shared-cache work solely because its
  initiating component unmounted.

## Quality checks

Run relevant configured type, lint, and component checks. Exercise changed loading, failure, unmount, keyboard, and focus behavior as applicable; distinguish source inspection from runtime observations.

### Testing

- Test behavior with a DOM-focused library; avoid implementation details.
- Mock network calls; cover edge cases and error states.

## Return

Return the component change or located review findings, checked behaviors, validation results, and remaining accessibility or lifecycle gaps.

## Boundaries

Do not replace the state library, styling system, shared cache, or framework without approval. Preserve mutation ownership and avoid canceling shared work merely to satisfy a component-local cleanup pattern.
