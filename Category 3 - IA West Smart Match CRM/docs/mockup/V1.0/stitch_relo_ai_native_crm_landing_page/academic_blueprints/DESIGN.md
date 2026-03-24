# Design System Specification: The Academic Curator

## 1. Overview & Creative North Star
The "Academic Curator" is a design system built for the intersection of institutional prestige and data-driven precision. Moving away from the "standard CRM" look, this system adopts an **Editorial High-End** aesthetic. It prioritizes the weight of information through sophisticated spatial relationships rather than rigid lines.

**Creative North Star: The Digital Atelier**
Think of the interface as a high-end academic journal or a curated gallery. We use intentional asymmetry, expansive breathing room (negative space), and tonal layering to guide the user. The goal is to make volunteer coordination feel like a prestigious mission, not a data-entry chore. We achieve this by breaking the "box-in-a-box" layout, opting instead for overlapping surfaces and typographic authority.

---

## 2. Colors & Surface Architecture
Our palette is rooted in "IA West Blue" and a range of sophisticated neutrals. The primary objective is to create a sense of calm and institutional trust.

### The "No-Line" Rule
Standard 1px borders are strictly prohibited for defining sections. To separate the "Sidebar" from the "Main Content" or "Dashboard Modules," use background shifts. 
*   **Example:** A `surface-container-low` (#f2f4f7) sidebar resting against a `surface` (#f7f9fc) workspace.

### Surface Hierarchy & Nesting
Treat the UI as physical layers of fine paper. Depth is created by nesting containers using the following tiers:
- **Level 0 (Base):** `surface` (#f7f9fc) - The infinite canvas.
- **Level 1 (Sections):** `surface-container-low` (#f2f4f7) - Large layout regions.
- **Level 2 (Cards):** `surface-container-lowest` (#ffffff) - Actionable content units. This "pops" against the darker base.
- **Level 3 (Popovers):** `surface-container-highest` (#e0e3e6) - Overlays and temporary states.

### Signature Textures
- **The Glass & Gradient Rule:** For primary CTAs or Hero backgrounds, do not use flat hex codes. Apply a subtle linear gradient from `primary` (#005394) to `primary-container` (#2b6cb0) at a 135-degree angle.
- **Backdrop Blur:** Floating navigation or top bars must use `surface_container_lowest` at 80% opacity with a `24px` backdrop-blur to allow underlying data colors to bleed through softly.

---

## 3. Typography
The typography system relies on the interplay between the condensed, authoritative **Inter Tight** and the highly legible **Inter**.

- **Display & Headlines (Inter Tight, 600-700):** These are your "Editorial Anchors." Use `display-md` for main dashboard greetings and `headline-sm` for card titles. The tight tracking conveys a sense of modern academic rigor.
- **Body & UI (Inter, 400-500):** Used for all data points and long-form text. 
- **The Hierarchy Rule:** Never use color alone to show importance. Use the scale—jumping from `label-md` for metadata to `title-lg` for primary names—to create a clear visual path for the coordinator's eye.

---

## 4. Elevation & Depth
We reject traditional "Material" drop shadows in favor of **Tonal Layering**.

- **Layering Principle:** To lift a volunteer profile card, place a `surface-container-lowest` (#ffffff) card on a `surface-container` (#eceef1) background. The contrast in lightness provides all the "lift" required.
- **Ambient Shadows:** Only for floating elements (modals, dropdowns). Use: `box-shadow: 0 12px 40px rgba(25, 28, 30, 0.06);`. The shadow color must be a tinted version of `on-surface` (#191c1e), never pure black.
- **The "Ghost Border" Fallback:** If a border is required for accessibility in forms, use `outline-variant` (#c1c7d2) at **20% opacity**. It should feel felt, not seen.

---

## 5. Components

### Buttons
- **Primary:** Gradient fill (`primary` to `primary-container`), white text, 0.75rem (md) radius.
- **Secondary:** `surface-container-high` background with `on-surface` text. No border.
- **Tertiary:** Text only, using `primary` color, with a 2px `surface-tint` underline on hover.

### Input Fields
- **Styling:** Use `surface-container-lowest` for the field background. 
- **States:** On focus, do not use a heavy border; use a 2px "Ghost Border" of `primary` and a subtle `EBF8FF` (Accent soft tint) glow.
- **Labeling:** Always use `label-md` sitting 8px above the input field, never inside.

### Cards & Lists
- **The Divider Ban:** Never use `<hr>` tags or border-bottoms between list items. Use `spacing-4` (1rem) or `spacing-6` (1.5rem) of vertical white space to separate entries.
- **Radii:** All cards must use `xl` (1.5rem / 24px) or `lg` (1rem / 16px) corner radii to soften the data-heavy nature of a CRM.

### Volunteer Status Chips
- **Selection Chips:** Use `secondary-fixed` for the background and `on-secondary-fixed-variant` for text. High contrast, low saturation—keeping it academic and professional.

---

## 6. Do’s and Don’ts

### Do:
- **Embrace Asymmetry:** Align primary data to the left and metadata to the extreme right to create an editorial layout feel.
- **Use High-Scale Contrast:** A `display-sm` header next to a `label-sm` timestamp creates a premium, intentional look.
- **Apply Large Radii:** Keep the 18px-24px radii consistent to maintain the "Institutional" but "Approachable" vibe.

### Don’t:
- **Don't use 100% Black:** Always use `on-surface` (#191c1e) for text to maintain a soft, ink-on-paper feel.
- **Don't use Dividers:** If you feel the need to draw a line, try adding `8px` of extra white space instead.
- **Don't use Default Shadows:** Standard "Drop Shadows" make the interface look like a legacy enterprise app. Stick to Tonal Layering.