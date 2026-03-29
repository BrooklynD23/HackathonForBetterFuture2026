---
phase: 15-build-quality-playwright-evidence
plan: 01
subsystem: infra
tags: [vite, rollup, manualChunks, build, vendor-splitting]

requires:
  - phase: 14-visual-resilience
    provides: completed React frontend with mock data wiring and DemoModeBadge

provides:
  - "Clean production build with zero chunk-size warnings via manualChunks vendor splitting"
  - "4 named vendor chunks: vendor-react (230 kB), vendor-charts (412 kB), vendor-ui (32 kB), vendor-emotion (merged)"

affects:
  - "15-02-playwright-evidence: build output dir exists and is valid for Playwright test runs"

tech-stack:
  added: []
  patterns:
    - "manualChunks function in vite.config.ts rollupOptions.output for vendor chunk splitting"
    - "Chunk assignment by node_modules path substring matching"

key-files:
  created: []
  modified:
    - "Category 3 - IA West Smart Match CRM/frontend/vite.config.ts"

key-decisions:
  - "Use manualChunks function (not object) so @emotion/* merges into index if tree-shaken, avoiding zero-size chunk error"
  - "Split by library family: react/router, recharts/d3, mui/radix-ui, emotion — keeps each chunk under 500 kB"
  - "All existing vite.config.ts settings (plugins, resolve, server, proxy, assetsInclude) remain unchanged per user decision"

patterns-established:
  - "manualChunks: id.includes('node_modules') guard first, then specific library path checks, return chunk name string or undefined"

requirements-completed: [BUILD-01]

duration: ~6min
completed: 2026-03-27
---

# Phase 15 Plan 01: Build Quality — Vendor Chunk Splitting Summary

**manualChunks config in vite.config.ts splits the 1042 kB monolithic vendor bundle into 4 named chunks all under 500 kB, eliminating Vite's chunk-size warnings on production build**

## Performance

- **Duration:** ~6 min
- **Started:** 2026-03-27T23:47:50Z
- **Completed:** 2026-03-27T23:53:50Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments

- Added `build.rollupOptions.output.manualChunks` to `vite.config.ts` with 4 vendor chunk patterns
- Production build now exits 0 with zero chunk-size warnings (previously showed "Some chunks are larger than 500 kB")
- Confirmed: vendor-react 230.91 kB, vendor-charts 412.33 kB, vendor-ui 31.92 kB, index 364.53 kB — all under 500 kB
- All existing config preserved: plugins (react, tailwindcss), resolve alias, server/proxy, assetsInclude

## Task Commits

1. **Task 1: Add manualChunks vendor splitting to vite.config.ts** - `9185b15` (feat)

**Plan metadata:** (docs commit to follow)

## Files Created/Modified

- `Category 3 - IA West Smart Match CRM/frontend/vite.config.ts` — Added `build.rollupOptions.output.manualChunks` function with 4 vendor chunk patterns

## Decisions Made

- `@emotion/` packages did not produce a separate `vendor-emotion` chunk because `@mui/` tree-shaking merged them into the main `index` bundle. This is expected behavior — the result is still under 500 kB with no warnings.
- Used a function form for `manualChunks` (not an object) to handle dynamic path matching cleanly.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - build completed cleanly on first attempt.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- BUILD-01 satisfied: `npm run build` exits 0, zero chunk-size warnings
- `dist/` directory now exists with properly chunked assets ready for Playwright evidence tests (15-02)
- No blockers for Phase 15 Plan 02

---
*Phase: 15-build-quality-playwright-evidence*
*Completed: 2026-03-27*
