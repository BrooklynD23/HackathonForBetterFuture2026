# Phase 18: Tech Debt Cleanup — Code Fixes — Research

**Researched:** 2026-03-28
**Domain:** TypeScript type safety (motion/react), Python datetime API, documentation gaps
**Confidence:** HIGH

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DEBT-01 | `WithSource<T>` in `frontend/src/lib/api.ts` includes `"csv"` source type and `isMockData` is true when source is `"csv"` | `WithSource.source` union is `"live" \| "demo"` — `"csv"` missing; all page consumers check `=== "demo"` only; fix is a two-line type + logic change in api.ts and all fetch* helpers |
| DEBT-02 | Crawler timestamp in `src/api/routers/crawler.py` calls `.isoformat()` so each crawl event gets a distinct timestamp | Line 101 assigns `now = datetime.now(timezone.utc).isoformat` (missing `()`) — `now` is a bound method reference, not the string; every call to `now()` succeeds but produces a fresh call each time so no deduplication — wait: actually the bug is the OPPOSITE: `now` is `datetime.now(timezone.utc).isoformat` which is a BOUND METHOD on a FIXED datetime object; calling `now()` always returns the same frozen string |
| DEBT-03 | DB-01–CRAWLER-03 added to REQUIREMENTS.md traceability table with Phase 17 mapped | Already added to REQUIREMENTS.md (verified in file), but DEBT-03 itself is still `[ ]` pending — the fix is marking DEBT-03 complete |
| DEBT-04 | framer-motion TypeScript errors in LandingPage.tsx and LoginPage.tsx resolved; `npm run build` reports zero TS errors from those files | 7 TS2322 errors confirmed by `npx tsc --noEmit`; root cause: `ease: number[]` but `Easing` type requires `BezierDefinition` = `readonly [number, number, number, number]` 4-tuple |
</phase_requirements>

---

## Summary

Phase 18 closes four targeted code-level debt items from the v3.1 audit. Three are surgical one-to-three line fixes; one (DEBT-03) is a documentation-only completion check. All bugs are confirmed in the live codebase.

**DEBT-01** (`WithSource<T>`): The interface on line 864 of `frontend/src/lib/api.ts` declares `source: "live" | "demo"` — `"csv"` is absent. The Layer 2 fallback (CSV) produces `source: "csv"` from the backend but the frontend type silently widens it to `live`. All five page components derive `isMockData` exclusively from `source === "demo"`, so a CSV fallback is never flagged as mock data.

**DEBT-02** (crawler timestamp bug): Line 101 of `src/api/routers/crawler.py` reads `now = datetime.now(timezone.utc).isoformat` — without parentheses. This assigns `now` to the bound `.isoformat` method of the single datetime object created at that instant. Every call to `now()` throughout the crawl returns the same frozen timestamp string. Events in one crawl session all share the same `crawled_at` / `timestamp`.

**DEBT-03** (REQUIREMENTS.md traceability): The DB-01–CRAWLER-03 rows were already added to REQUIREMENTS.md during the phase itself (verified at lines 33–43 and 100–106 of REQUIREMENTS.md). DEBT-03 is "add them" — they are present. The plan task is to mark DEBT-03 complete and verify nothing was missed.

**DEBT-04** (motion TypeScript errors): Both `LandingPage.tsx` and `LoginPage.tsx` import from `"motion/react"` (the correct import for `motion` v12). The TS errors (`TS2322`) arise because `ease: [0.16, 1, 0.3, 1]` is inferred as `number[]` by TypeScript, but the `motion-utils` `Easing` type requires `BezierDefinition = readonly [number, number, number, number]`. Adding `as const` to the array literal (or typing the containing object as `const`) makes TypeScript infer the 4-tuple, satisfying `BezierDefinition`.

**Primary recommendation:** All four fixes are atomic. Execute as a single plan (18-01-PLAN.md) with four independent tasks in one wave.

---

## Standard Stack

### Core (already installed — no new dependencies)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| motion | 12.23.24 | Animation (React) | Already installed; `motion/react` is the correct import path for v12+ |
| TypeScript | ^5.6.3 | Type checking | Project standard; `npx tsc --noEmit` is the verification command |
| Python datetime | stdlib | Timestamp generation | Standard library; `.isoformat()` is the correct method call |

### No new dependencies required

All four fixes use existing packages. No `npm install` or `pip install` needed.

---

## Architecture Patterns

### Pattern 1: TypeScript const-assertion for literal tuple types

**What:** `as const` on an array literal forces TypeScript to infer a readonly tuple type instead of `number[]`.

**When to use:** Any time a plain array literal must satisfy a typed tuple parameter.

**Example:**
```typescript
// BEFORE (TS2322 error — ease inferred as number[])
const introReveal = {
  transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1] },
};

// AFTER (ease inferred as readonly [number, number, number, number] = BezierDefinition)
const introReveal = {
  transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1] as const },
} as const;
```

`BezierDefinition` in `motion-utils` is defined as `readonly [number, number, number, number]`.
`Easing = EasingDefinition | EasingFunction` where `EasingDefinition` includes `BezierDefinition`.
A `number[]` does NOT satisfy `BezierDefinition` — the `as const` assertion is required.

Source: verified in `node_modules/motion-utils/dist/index.d.ts` line 72–83.

### Pattern 2: WithSource union extension

**What:** Add `"csv"` to the source union and update `isMockData` logic in each fetch helper.

**When to use:** Any time a new fallback source tier is added to the 3-layer architecture.

**Example:**
```typescript
// BEFORE (api.ts line 864-866)
export interface WithSource<T> {
  data: T;
  source: "live" | "demo";
}

// AFTER — add "csv" to union
export interface WithSource<T> {
  data: T;
  source: "live" | "demo" | "csv";
  isMockData: boolean;
}
```

Each `fetch*` helper currently computes `const source: "live" | "demo"`. After the fix:
```typescript
// Pattern for each fetch helper (fetchSpecialists, fetchEvents, fetchPipeline, etc.)
const rawSource = payload[0]?.source;
const source: "live" | "demo" | "csv" =
  rawSource === "demo" ? "demo" : rawSource === "csv" ? "csv" : "live";
const isMockData = source === "demo" || source === "csv";
return { data: payload as unknown as T[], source, isMockData };
```

Page components that currently do `result.source === "demo"` will need updating to use `result.isMockData` OR the check `source === "demo" || source === "csv"`.

**Scope of page-level changes:** Five pages check `result.value.source === "demo"`:
- `Dashboard.tsx` lines 291, 292, 296, 299, 308, 316
- `Pipeline.tsx` — similar pattern
- `Volunteers.tsx` — similar pattern
- `Calendar.tsx` — similar pattern
- `AIMatching.tsx` — similar pattern

The safest fix is to add `isMockData: boolean` to `WithSource<T>` and derive it inside each `fetch*` helper, then update page checks to use `result.value.isMockData` instead of `result.value.source === "demo"`. This localizes the logic and makes future source tiers trivial.

### Pattern 3: Python datetime fresh-call pattern

**What:** Assign a callable or call fresh each time — never bind a method from a frozen datetime object.

**When to use:** Any time a timestamp must be unique per event.

**The bug (line 101, crawler.py):**
```python
# WRONG — now is the bound .isoformat method of ONE frozen datetime object
now = datetime.now(timezone.utc).isoformat

# CORRECT option A — lambda that creates a fresh datetime on each call
now = lambda: datetime.now(timezone.utc).isoformat()

# CORRECT option B — inline function
def now() -> str:
    return datetime.now(timezone.utc).isoformat()
```

Source: verified by reading `src/api/routers/crawler.py` line 101.

### Pattern 4: REQUIREMENTS.md traceability verification

**What:** Confirm the already-added rows are present and well-formed, then mark DEBT-03 complete.

Looking at REQUIREMENTS.md lines 33–43 and 100–106:
- DB-01–DB-04 and CRAWLER-01–CRAWLER-03 ARE already in the file under "v3.1 Phase 17 Requirements (Previously Unregistered)" (lines 33–43) with `[x]` status.
- The traceability table at lines 100–106 already has all seven rows mapped to Phase 17.
- DEBT-03's checkbox (`- [ ] **DEBT-03**`) needs to become `- [x] **DEBT-03**` and the traceability table row `DEBT-03 | Phase 18 | Pending` needs to become `Complete`.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Bezier easing type satisfaction | Custom `type BezierTuple` alias | `as const` assertion on the literal | The `motion-utils` type is already correct; `as const` is zero-cost |
| Crawler timestamp uniqueness | Caching/deduplication logic | Fix the method-reference bug | The root cause is a missing `()` — no new logic needed |
| New `isMockData` computation | Per-page logic scattered across 5 files | Centralize in `WithSource<T>` interface + fetch helpers | Single source of truth already pattern-established in api.ts |

---

## Common Pitfalls

### Pitfall 1: Spread-propagated const-assertion losing tuple type

**What goes wrong:** `{ ...introReveal, transition: { ...introReveal.transition, delay: 0.1 } }` spreads a `const`-asserted object but the spread result loses the tuple inference for `ease`.

**Why it happens:** `LoginPage.tsx` line 76 uses `{ ...panelReveal.transition, delay: 0.08 }`. If `panelReveal` is declared with `as const`, spreading its `.transition` creates a new mutable object and `ease` reverts to `readonly [number, number, number, number]` — which actually IS fine because it's still the tuple type. Verify after fix.

**How to avoid:** After applying `as const`, run `npx tsc --noEmit` to confirm zero errors in both files before declaring done.

**Warning signs:** Residual TS2322 on the spread lines (76 in LoginPage.tsx, 129 in LandingPage.tsx) even after top-level `as const`.

### Pitfall 2: `WithSource` isMockData field breaks existing callers

**What goes wrong:** If `isMockData` is added as a required field to `WithSource<T>`, every `fetch*` helper must be updated — missing one will cause a TS error on the return type.

**Why it happens:** There are 8+ `fetch*` functions in api.ts. Easy to miss one.

**How to avoid:** Add `isMockData: boolean` to the interface, then search for all `return { data: ..., source }` patterns in api.ts and add `isMockData` to each. `npx tsc --noEmit` will catch any missed ones.

**Warning signs:** TS2740 "missing property isMockData" errors after updating the interface.

### Pitfall 3: Page-level `source === "demo"` checks become stale

**What goes wrong:** After adding `isMockData` to `WithSource`, page code still checks `result.value.source === "demo"` and ignores `"csv"` fallback.

**Why it happens:** Five pages (Dashboard, Pipeline, Volunteers, Calendar, AIMatching) have inline source checks. Updating the interface alone doesn't update the page logic.

**How to avoid:** Replace `result.value.source === "demo"` with `result.value.isMockData` in all 5 pages. Grep for `=== "demo"` in `frontend/src/app/pages/` to find all instances.

**Warning signs:** Demo Mode badge never shows when backend serves CSV source.

### Pitfall 4: `as const` on the whole object breaks mutations

**What goes wrong:** If `introReveal` or `panelReveal` are declared `as const`, their properties become `readonly`. Spreading them into JSX props is fine (props are never mutated), but explicitly mutating fields in the object literal would fail.

**Why it happens:** These objects are module-level constants never mutated — `as const` is safe. But double-check there are no push/assign operations on them.

**How to avoid:** Confirm `introReveal` and `panelReveal` are pure declaration objects with no mutation. Both files show only spreading in JSX — safe.

---

## Code Examples

### Fix for DEBT-02 (crawler.py timestamp)

```python
# File: src/api/routers/crawler.py, line 101
# BEFORE
now = datetime.now(timezone.utc).isoformat

# AFTER
def _now() -> str:
    """Return current UTC time as ISO-8601 string. Called fresh per event."""
    return datetime.now(timezone.utc).isoformat()
```

Then replace all `now()` calls in `_run_crawl` and `_run_crawl_body` with `_now()`. Since `_run_crawl` already passes `now` as a parameter to `_run_crawl_body`, the call sites in `_run_crawl_body` are `now()` — these all work correctly once `now` is a real callable that creates a fresh datetime. Alternatively, inline `datetime.now(timezone.utc).isoformat()` at each call site.

The simplest change: on line 101, change:
```python
now = datetime.now(timezone.utc).isoformat
```
to:
```python
def now() -> str:
    return datetime.now(timezone.utc).isoformat()
```

Source: verified in `src/api/routers/crawler.py` lines 99–121.

### Fix for DEBT-01 (WithSource + isMockData)

```typescript
// frontend/src/lib/api.ts, replace lines 864-867
export interface WithSource<T> {
  data: T;
  source: "live" | "demo" | "csv";
  isMockData: boolean;
}

// Pattern for each fetch* helper (example: fetchSpecialists)
export async function fetchSpecialists(): Promise<WithSource<Specialist[]>> {
  const raw = await requestJson<unknown>("/api/data/specialists");
  const payload = toRecordArray(raw);
  const rawSource = (payload[0] as Record<string, unknown>)?.source;
  const source: "live" | "demo" | "csv" =
    rawSource === "demo" ? "demo" : rawSource === "csv" ? "csv" : "live";
  return { data: payload as unknown as Specialist[], source, isMockData: source !== "live" };
}
```

### Fix for DEBT-04 (framer-motion / motion TS errors)

```typescript
// OPTION A: as const on each ease array (minimal change, surgical)
const introReveal = {
  initial: { opacity: 0, y: 24 },
  whileInView: { opacity: 1, y: 0 },
  transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1] as const },
  viewport: { once: true, amount: 0.35 },
} as const;

// OPTION B: as const on panelReveal in LoginPage.tsx
const panelReveal = {
  initial: { opacity: 0, y: 24 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.65, ease: [0.16, 1, 0.3, 1] as const },
} as const;
```

Note: the spread on LoginPage.tsx line 76:
```typescript
transition={{ ...panelReveal.transition, delay: 0.08 }}
```
After `as const`, `panelReveal.transition.ease` will be `readonly [0.16, 1, 0.3, 1]` which satisfies `BezierDefinition`. The spread creates a new object but preserves the tuple type.

Source: verified `motion-utils` type definitions — `BezierDefinition = readonly [number, number, number, number]`.

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `framer-motion` package | `motion` package (import from `"motion/react"`) | motion v11+ (2024) | LandingPage.tsx and LoginPage.tsx already use `"motion/react"` — correct. The "framer-motion TypeScript errors" label in the roadmap refers to TS errors in the files that use motion, not to a wrong import path. |
| `ease: number[]` | `ease: readonly [number, number, number, number]` (`BezierDefinition`) | motion v11 stricter types | Requires `as const` assertion or explicit typing |

**Note on framer-motion naming:** The roadmap calls these "framer-motion TypeScript errors" because the animation library was historically called framer-motion. The project already migrated to the `motion` package. The TS errors are purely from the `ease` array type mismatch, not from a wrong package import.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest (Python) + tsc --noEmit (TypeScript) |
| Config file | No pytest.ini found at project root — uses defaults |
| Quick run command (Python) | `cd "Category 3 - IA West Smart Match CRM" && python -m pytest tests/ -x -q 2>&1 \| tail -5` |
| TS check command | `cd "Category 3 - IA West Smart Match CRM/frontend" && npx tsc --noEmit` |
| Full suite command | `python -m pytest tests/ -v` |

### Phase Requirements to Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DEBT-01 | `WithSource.source` accepts `"csv"`; `isMockData` true when source is `"csv"` | unit (TypeScript) | `npx tsc --noEmit` (type check) | ❌ Wave 0 — add inline assertion or TS test |
| DEBT-02 | Each crawler event gets a distinct timestamp | unit (Python) | `python -m pytest tests/ -k crawler -x` | ❌ Wave 0 — no test for timestamp uniqueness yet |
| DEBT-03 | REQUIREMENTS.md traceability rows present and DEBT-03 marked complete | manual-only | Visual inspection of REQUIREMENTS.md | ✅ (manual) |
| DEBT-04 | `npm run build` / `npx tsc --noEmit` reports zero TS errors in LandingPage.tsx and LoginPage.tsx | build check | `npx tsc --noEmit 2>&1 \| grep -E "LandingPage\|LoginPage"` | ✅ existing tsc run |

### Sampling Rate

- **Per task:** `npx tsc --noEmit` for TS tasks; targeted pytest for Python task
- **Per wave merge:** Full `npx tsc --noEmit` + `npm run build`
- **Phase gate:** Zero TS errors in LandingPage.tsx and LoginPage.tsx; crawler test passes; REQUIREMENTS.md verified

### Wave 0 Gaps

- [ ] `tests/test_crawler_timestamp.py` — covers DEBT-02 (timestamp uniqueness per event)
- [ ] TypeScript type-level assertion for DEBT-01 — a compile-time test that `"csv"` is valid for `WithSource.source` (can be a `.ts` file with `satisfies` or a simple tsc check)

*(The TypeScript gap can be validated entirely via `npx tsc --noEmit` after the fix — no separate test file strictly required for DEBT-04.)*

---

## Open Questions

1. **DEBT-01: Should page components switch to `result.value.isMockData` or keep `source === "demo" || source === "csv"`?**
   - What we know: Adding `isMockData` to `WithSource<T>` centralizes logic. Pages currently have the check inline.
   - What's unclear: Whether any page accesses `.source` for purposes other than `isMockData` (e.g., displaying a source label).
   - Recommendation: Add `isMockData` to `WithSource<T>` and update pages to use it. The `.source` field stays for diagnostic display.

2. **DEBT-02: Should `now` remain a parameter passed to `_run_crawl_body` or be called inline?**
   - What we know: `_run_crawl` defines `now` and passes it to `_run_crawl_body(now)`. This is a testability hook.
   - What's unclear: Whether tests mock `now` for deterministic timestamps.
   - Recommendation: Change `now` to `lambda: datetime.now(timezone.utc).isoformat()` (or a def) on line 101, keeping the parameter-passing pattern intact. This preserves the testability interface.

---

## Sources

### Primary (HIGH confidence)

- Direct file inspection: `src/api/routers/crawler.py` line 101 — bug confirmed by reading
- Direct file inspection: `frontend/src/lib/api.ts` lines 864–888 — `"csv"` absent from union confirmed
- `npx tsc --noEmit` output — 7 TS2322 errors confirmed, exact error messages captured
- `node_modules/motion-utils/dist/index.d.ts` lines 72–83 — `BezierDefinition`, `Easing` type definitions verified
- `frontend/package.json` — `"motion": "12.23.24"` confirmed, no `framer-motion` package present
- `.planning/REQUIREMENTS.md` lines 33–43, 100–116 — DB-01–CRAWLER-03 rows already present; DEBT-03 still `[ ]`

### Secondary (MEDIUM confidence)

- Pattern: `as const` for tuple inference — standard TypeScript technique, confirmed applicable by type inspection

### Tertiary (LOW confidence)

- None

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all dependencies confirmed present, no new installs needed
- Architecture: HIGH — bugs confirmed by direct code inspection and tsc output
- Pitfalls: HIGH — spread/const interaction verified against motion-utils types

**Research date:** 2026-03-28
**Valid until:** 2026-04-28 (stable libraries; motion v12 types are stable)
