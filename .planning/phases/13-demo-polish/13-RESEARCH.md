# Phase 13: Demo Polish - Research

**Researched:** 2026-03-26
**Domain:** React 18 / React Router 7 / Tailwind v4 — UI copy audit, scroll behavior, document title
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Copy & Label Cleanup**
- Exhaustive sweep of all TSX files for Phase #N references (not limited to known occurrence)
- Remove "Phase 12" label in FeedbackForm.tsx entirely — coordinator context makes it self-evident
- Audit all page headings, button labels, empty states, and section descriptions; replace dev-flavored strings with polished product copy
- Scope: headings, button labels, empty states, and section descriptions (not tooltips or error messages)

**Smooth Scrolling**
- Apply `scroll-behavior: smooth` globally on the `html` element in `src/styles/index.css`
- No route transition animation — smooth scrolling is sufficient for a clean demo
- Scroll to top on every route change via `useEffect` in App.tsx
- No anchor scroll links needed in this phase

**Demo Submission Standards**
- Audit all sidebar/nav items for product-ready naming
- Update `<title>` tags to reflect product name (not Vite/React defaults)
- Write concrete empty states: descriptive messages instead of "Loading..." or null fallbacks
- Verify with grep audit showing zero Phase #N strings remain + manual visual review

### Claude's Discretion
- Specific replacement copy for dev-flavored strings — Claude should write polished, concise product copy consistent with the IA West SmartMatch brand

### Deferred Ideas (OUT OF SCOPE)
- Playwright screenshot capture of each page after polish (Phase 15 handles browser evidence)
- Anchor scroll navigation for Dashboard/LandingPage sections (not needed for demo flow)
- Full tooltip and error message copywriting pass (beyond this phase's scope)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| POLISH-01 | All internal "Phase #N" labels removed from user-facing UI text across all pages | Confirmed single occurrence: `FeedbackForm.tsx:147`; grep pattern documented for exhaustive audit |
| POLISH-02 | All page headings, button labels, and body copy are concrete and demo-ready (no placeholder or dev-flavored text) | Dev-flavored strings catalogued below; replacement copy strategy defined |
| POLISH-03 | Smooth scrolling applied across all pages and view transitions | `scroll-behavior: smooth` already on `html` in `theme.css`; scroll-to-top pattern documented for App.tsx |
</phase_requirements>

---

## Summary

Phase 13 is a surgical UI copy and scroll polish pass on a React 18 + React Router 7 + Tailwind v4 frontend. The codebase is well-structured with all pages under `src/app/pages/` and a shared Layout shell at `src/app/components/Layout.tsx`.

**Confirmed state going in:**
1. `scroll-behavior: smooth` is already applied to `html` in `src/styles/theme.css` (line 155). No CSS change is needed.
2. There is no scroll-to-top hook anywhere in the app. Every route change leaves the scroll position where it was — this must be fixed in `App.tsx`.
3. The only confirmed Phase #N string is `FeedbackForm.tsx:147` ("Phase 12"). A grep audit across all TSX files found no other occurrences.
4. The browser `<title>` in `index.html` already reads "IA West SmartMatch CRM" — no change needed there.
5. Two dev-flavored strings exist on the LandingPage: `"V1.2 public brand"` (nav subtitle, line 56) and `"IA West V1.2 blue / white brand"` (hero pill, line 72). These are internal version labels that must be replaced with product copy.
6. Sidebar nav labels (Dashboard, Opportunities, Volunteers, AI Matching, Pipeline, Calendar, Outreach) are already product-ready.
7. Empty states in AIMatching, Calendar, Dashboard, Pipeline, and Volunteers are already written in the correct "No [entity] yet" / "No [entity] found" pattern and do not need changes.

**Primary recommendation:** Three targeted edits — (1) remove Phase 12 badge from FeedbackForm, (2) replace two dev-flavored version strings on LandingPage, (3) add scroll-to-top `useEffect` to App.tsx (which uses `RouterProvider`, requiring a wrapper component approach).

## Standard Stack

### Core (already installed — no new dependencies needed)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| react-router | 7.13.0 | Routing + location tracking | Already in use; `useLocation` hook provides route change signal |
| react | 18.3.1 | Component model | Already in use |
| tailwindcss | 4.1.12 | Utility CSS | Already in use; theme.css is the global style entry point |

### No new packages required

All three tasks (Phase #N removal, copy replacement, scroll-to-top) are implementable with what is already installed.

## Architecture Patterns

### Recommended Project Structure (unchanged)

```
src/
├── app/
│   ├── App.tsx              # RouterProvider root — add ScrollToTop wrapper here
│   ├── routes.tsx           # createBrowserRouter config — unchanged
│   ├── pages/               # 9 page components — targeted copy edits
│   └── components/
│       └── Layout.tsx       # Shared shell — nav already product-ready
├── components/
│   └── FeedbackForm.tsx     # Remove Phase 12 badge here
└── styles/
    ├── index.css            # @import chain — no change needed
    └── theme.css            # scroll-behavior: smooth already present
```

### Pattern 1: Scroll-to-Top on Route Change

**What:** A component that calls `window.scrollTo(0, 0)` inside a `useEffect` that depends on `location.pathname`. Placed inside the router context so it has access to `useLocation`.

**Why App.tsx needs a wrapper:** `App.tsx` uses `<RouterProvider router={router} />` directly. `RouterProvider` provides the router context, so `useLocation` cannot be called in `App.tsx` itself — it must be called inside a component rendered within that router. The standard solution is to add a `ScrollToTop` component and render it inside the Layout component or as a pathless route child.

**The cleanest insertion point:** Add `ScrollToTop` as a child of the Layout component (it's already rendered on every coordinator route). For the public routes (LandingPage, LoginPage), scroll-to-top at the Layout level won't fire. The correct approach is to add a wrapper `<Root>` component that wraps `<Outlet />` in routes.tsx, or use a pathless layout wrapping all routes.

**Simplest correct approach:** Add `ScrollToTop` directly inside `Layout.tsx` since all authenticated routes go through Layout. For the two public routes (LandingPage, LoginPage), those pages are short enough that no scroll position carries over from a prior public page — acceptable for demo scope.

**Example:**
```tsx
// src/app/components/ScrollToTop.tsx
import { useEffect } from "react";
import { useLocation } from "react-router";

export function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
}
```

```tsx
// src/app/components/Layout.tsx — add near top of Layout return
import { ScrollToTop } from "./ScrollToTop";

export function Layout() {
  // ...existing code...
  return (
    <div className="min-h-screen bg-background">
      <ScrollToTop />
      {/* ...rest of layout... */}
    </div>
  );
}
```

Alternatively, if scroll-to-top is also needed on public route transitions (e.g., navigating from Landing to Login), wrap it in `routes.tsx` at the root level using a pathless layout.

### Pattern 2: Phase Badge Removal

**What:** Delete the entire badge `<div>` in FeedbackForm.tsx (lines 146–148). The `title` and `description` props already communicate the form's context. No replacement copy needed.

**The exact element to remove:**
```tsx
// DELETE these 3 lines from FeedbackForm.tsx:
<div className="rounded-full border border-blue-100 bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700">
  Phase 12
</div>
```

### Pattern 3: LandingPage Dev-Flavored String Replacement

**Strings to replace:**

| Location | Current string | Replacement |
|----------|---------------|-------------|
| `LandingPage.tsx:56` (nav subtitle, `<p>`) | `V1.2 public brand` | `Coordinator Platform` |
| `LandingPage.tsx:72` (hero pill, `<span>`) | `IA West V1.2 blue / white brand` | `IA West Chapter` |

These are the only two dev-flavored label strings found in LandingPage. The rest of the page copy ("Turn West Coast opportunities into coordinated specialist action", "Product story", "Analytics proof", etc.) is already polished and demo-ready.

### Anti-Patterns to Avoid

- **Replacing `scroll-behavior: smooth` in index.css:** It already exists in `theme.css` which is imported by `index.css`. Adding it again is redundant — do not add a duplicate.
- **Calling `useLocation` in App.tsx directly:** App.tsx only renders `<RouterProvider>`. `useLocation` requires being inside a router context — it will throw if called in App.tsx before the RouterProvider mounts.
- **Adding a `<title>` update hook per page:** The `index.html` title "IA West SmartMatch CRM" is already correct. Per-page title management is not in scope for this phase.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead |
|---------|-------------|-------------|
| Scroll-to-top on route change | Custom history listener | `useLocation` + `useEffect` — 5-line pattern, no library needed |
| Phase #N grep audit | Manual file-by-file review | `grep -rn "Phase \d+" src/ --include="*.tsx"` — run this as verification step |

## Common Pitfalls

### Pitfall 1: Scroll behavior already present, don't double-apply

**What goes wrong:** Planner adds `scroll-behavior: smooth` to `index.css` unaware it is already on `html` in `theme.css:155`. This results in a duplicate but harmless declaration — however, it signals the audit wasn't done.

**How to avoid:** The CSS is already complete. Do not add another `scroll-behavior` rule. Only the scroll-to-top React hook is missing.

**Warning signs:** If a task says "add scroll-behavior to index.css", it's based on incorrect assumption.

### Pitfall 2: ScrollToTop component placed outside router context

**What goes wrong:** If `ScrollToTop` is placed in `App.tsx` at the same level as `<RouterProvider>`, calling `useLocation()` will throw "useLocation() may be used only in the context of a `<Router>` component."

**How to avoid:** Place `ScrollToTop` inside any component that is rendered as a child of `RouterProvider` — `Layout.tsx` is the correct location for coordinator routes.

### Pitfall 3: Over-auditing "empty state" copy that is already polished

**What goes wrong:** The existing empty states like "No match results are available for the selected event yet" and "No assignments were found for this day" are already product-quality. Rewriting them wastes time and risks introducing worse copy.

**How to avoid:** Only replace strings that contain dev-internal identifiers (Phase #N, version labels like "V1.2 public brand"). Functional placeholder text that reads naturally to an end user is in scope only if it contains "Loading...", null renders, or similarly bare fallbacks — none of which were found in this audit.

### Pitfall 4: Missing `n/a` fallback in Calendar.tsx

**What:** `Calendar.tsx:749` renders `{assignment.event_cadence || "n/a"}`. This is a data fallback, not UI copy, and falls outside the headings/buttons/empty-states scope. Do not change it.

## Code Examples

### Exhaustive Phase #N Grep (verification command)

```bash
# Run from frontend/src — expected output: zero lines
grep -rn "Phase [0-9]\+" --include="*.tsx" --include="*.ts" .
```

### ScrollToTop Component

```tsx
// src/app/components/ScrollToTop.tsx
import { useEffect } from "react";
import { useLocation } from "react-router";

export function ScrollToTop(): null {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
}
```

### Layout.tsx integration point

```tsx
// At the very start of the Layout return — before sidebar markup
return (
  <div className="min-h-screen bg-background">
    <ScrollToTop />
    {/* existing sidebar markup follows... */}
```

## State of the Art

| Old Approach | Current Approach | Impact |
|--------------|------------------|--------|
| `scroll-behavior: smooth` in `@layer base` (Tailwind v3) | Direct `html { scroll-behavior: smooth; }` in `theme.css` (Tailwind v4) | Already implemented correctly |
| `useHistory` scroll restoration (React Router v5) | `useLocation` `pathname` dep in `useEffect` (React Router v6/v7) | 5-line component, no history API needed |
| Per-page `<Helmet>` title management | Single static `<title>` in `index.html` | Sufficient for hackathon demo scope; already correct |

## Open Questions

1. **Should ScrollToTop also cover public routes (LandingPage, LoginPage)?**
   - What we know: Public routes are short pages; users typically arrive fresh on Landing, then navigate to Login. Scroll position rarely accumulates.
   - What's unclear: If a user scrolls to the bottom of LandingPage and clicks "Sign In", they land on LoginPage at the bottom scroll position — visible on mobile.
   - Recommendation: Wrap all routes in a root-level pathless layout that renders `<ScrollToTop /><Outlet />` so all route changes scroll to top. This is one additional file and a 3-line change to routes.tsx.

2. **LandingPage pill replacement copy validation**
   - What we know: "V1.2 public brand" and "IA West V1.2 blue / white brand" are confirmed dev labels.
   - What's unclear: Whether the planner should use the exact replacement copy in this research or delegate to Claude's discretion at implementation time.
   - Recommendation: The planner should use the copy from the Pattern 3 table above as the working default; implementer may refine.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | None — no test framework configured in this project |
| Config file | None — no vitest.config, jest.config, or similar found |
| Quick run command | n/a |
| Full suite command | n/a |

No automated test infrastructure exists in the project. Manual visual verification is the validation approach for this phase.

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| POLISH-01 | Zero Phase #N strings in TSX files | Smoke (grep) | `grep -rn "Phase [0-9]\+" "Category 3 - IA West Smart Match CRM/frontend/src" --include="*.tsx" --include="*.ts"` — expect no output | N/A — grep command |
| POLISH-02 | No dev-flavored strings in visible headings/pills | Manual visual | Open each page in browser, inspect headings | N/A |
| POLISH-03 | Navigate between routes, scroll position resets to top | Manual visual | Navigate from a scrolled page to a new route, confirm scroll resets | N/A |

### Sampling Rate

- **Per task commit:** Run `grep -rn "Phase [0-9]\+" ... --include="*.tsx"` to confirm POLISH-01
- **Per wave merge:** Open browser, navigate all routes, confirm scroll top behavior
- **Phase gate:** All three requirements pass manual visual review before `/gsd:verify-work`

### Wave 0 Gaps

None — no test framework is being introduced. Validation for this phase is grep + manual visual review. No Wave 0 test file creation is needed.

## Sources

### Primary (HIGH confidence)

- Direct codebase audit — `src/styles/theme.css:153-156` (scroll-behavior already present)
- Direct codebase audit — `src/components/FeedbackForm.tsx:146-148` (Phase 12 badge, confirmed)
- Direct codebase audit — `src/app/pages/LandingPage.tsx:56,72` (V1.2 dev labels, confirmed)
- Direct codebase audit — `src/app/App.tsx` (no useLocation/useEffect, no scroll-to-top hook)
- Direct codebase audit — `index.html:6` (title already "IA West SmartMatch CRM")
- React Router v7 docs pattern — `useLocation` + `useEffect` for scroll restoration
- `package.json` — confirmed react-router@7.13.0, react@18.3.1, tailwindcss@4.1.12

### Secondary (MEDIUM confidence)

- React Router v7 community pattern: `ScrollRestoration` component is available in React Router v7 for data-router mode, but `window.scrollTo(0,0)` in `useEffect` on `pathname` is equally valid and simpler for this use case.

---

## Metadata

**Confidence breakdown:**
- Phase #N audit: HIGH — exhaustive grep confirms single occurrence
- Scroll behavior CSS: HIGH — directly verified in theme.css:155
- Scroll-to-top implementation: HIGH — standard React Router pattern, codebase confirmed no existing implementation
- Copy audit (LandingPage dev labels): HIGH — directly read and confirmed in source
- Empty state audit: HIGH — reviewed all pages, confirmed existing copy is product-ready
- Nav label audit: HIGH — Layout.tsx read directly, all labels are product-ready

**Research date:** 2026-03-26
**Valid until:** 2026-04-25 (stable stack, 30-day window)
