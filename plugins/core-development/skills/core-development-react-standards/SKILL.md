---
name: core-development-react-standards
description: React standards for components, state management, performance, accessibility, styling, data fetching, and testing.
---

# React Standards

## Components

- Prefer functional components; define typed props with interfaces.
- Keep components small and focused; lift state up when shared.
- Use composition over inheritance; avoid deep prop drilling.

## State and Effects

- Use local state for UI concerns; central store only when needed.
- Keep effects minimal; specify correct dependency arrays; clean up in `useEffect`.
- Derive state instead of duplicating; avoid unnecessary re-renders.

## Performance

- Use `React.memo`, `useMemo`, and `useCallback` judiciously.
- Provide stable keys for lists; avoid array index as key.
- Code-split large routes/components; lazy-load where appropriate.

## Accessibility

- Use semantic HTML; provide labels, roles, and ARIA where needed.
- Ensure keyboard navigation and focus management with visible focus states.

## Styling

- Follow the project's chosen styling system (CSS Modules, Tailwind, CSS-in-JS); be consistent.
- Avoid inline styles for dynamic logic-heavy styling; prefer class composition.

## Data and APIs

- Keep data fetching in hooks or containers; handle loading/error states.
- Cancel in-flight requests on unmount when applicable.

## Testing

- Test behavior with a DOM-focused library; avoid implementation details.
- Mock network calls; cover edge cases and error states.
