# Phase 13: Demo Polish - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 13 delivers a submission-ready user-facing experience: all internal Phase #N labels removed, every visible text string polished to concrete product copy, smooth scrolling enabled globally, navigation labels and browser titles updated for demo presentation.

</domain>

<decisions>
## Implementation Decisions

### Copy & Label Cleanup
- Exhaustive sweep of all TSX files for Phase #N references (not limited to known occurrence)
- Remove "Phase 12" label in FeedbackForm.tsx entirely — coordinator context makes it self-evident
- Audit all page headings, button labels, empty states, and section descriptions; replace dev-flavored strings with polished product copy
- Scope: headings, button labels, empty states, and section descriptions (not tooltips or error messages)

### Smooth Scrolling
- Apply `scroll-behavior: smooth` globally on the `html` element in `src/styles/index.css`
- No route transition animation — smooth scrolling is sufficient for a clean demo
- Scroll to top on every route change via `useEffect` in App.tsx
- No anchor scroll links needed in this phase

### Demo Submission Standards
- Audit all sidebar/nav items for product-ready naming
- Update `<title>` tags to reflect product name (not Vite/React defaults)
- Write concrete empty states: descriptive messages instead of "Loading..." or null fallbacks
- Verify with grep audit showing zero Phase #N strings remain + manual visual review

### Claude's Discretion
- Specific replacement copy for dev-flavored strings — Claude should write polished, concise product copy consistent with the IA West SmartMatch brand

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/styles/index.css` — global CSS entry point, right place for `scroll-behavior: smooth`
- `src/styles/theme.css` — V1.2 design tokens (Inter font, blue/white palette)
- `src/app/App.tsx` — route container, location to add scroll-to-top `useEffect`
- `src/app/components/Layout.tsx` — shared shell; nav labels live here
- `src/app/components/figma/ImageWithFallback.tsx` — existing fallback pattern (relevant for Phase 14)

### Established Patterns
- Tailwind v4 with custom theme tokens in `theme.css`
- shadcn/ui components throughout (`src/app/components/ui/`)
- React Router for navigation (routes defined in `src/app/routes.tsx`)
- V1.2 blue/white professional theme established in Phase 09.1

### Integration Points
- Phase #N string to remove: `FeedbackForm.tsx:147` ("Phase 12") — confirmed
- Pages to audit for copy: Landing, Login, Dashboard, AIMatching, Calendar, Opportunities, Outreach, Pipeline, Volunteers (8 pages + Layout nav)
- Browser `<title>` likely set in `index.html` or per-page via document.title

</code_context>

<specifics>
## Specific Ideas

- "Phase 12" in FeedbackForm should be removed entirely, not replaced with another label
- Smooth scroll: global CSS approach is preferred over per-component implementation
- Empty states should read as: "No [entity] scheduled yet" / "No matches found" patterns — concrete, not generic

</specifics>

<deferred>
## Deferred Ideas

- Playwright screenshot capture of each page after polish (Phase 15 handles browser evidence)
- Anchor scroll navigation for Dashboard/LandingPage sections (not needed for demo flow)
- Full tooltip and error message copywriting pass (beyond this phase's scope)

</deferred>
