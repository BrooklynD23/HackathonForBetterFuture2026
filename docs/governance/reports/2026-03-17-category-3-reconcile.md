# Category 3 Documentation Reconciliation — 2026-03-17

## Scope

- `PRD_SECTION_CAT3.md`
- `Category 3 - IA West Smart Match CRM/PLAN.md`
- `Category 3 - IA West Smart Match CRM/.status.md`
- `Category 3 - IA West Smart Match CRM/docs/SPRINT_PLAN.md`
- `Category 3 - IA West Smart Match CRM/docs/sprints/*.md`

## Safe Reconciliations Applied

- Repointed Category 3 governance links to the actual portfolio doc paths under `archived/general_project_docs/`.
- Re-established the execution authority chain: `SPRINT_PLAN.md` and `PRD_SECTION_CAT3.md` are canonical; `PLAN.md` is background-only.
- Standardized the import/runtime contract on `from src...` and `streamlit run src/app.py`.
- Standardized the embedding contract on 68 embedded rows with flat cache artifacts under `cache/`.
- Standardized the match-result contract on `total_score` plus full factor keys such as `topic_relevance`.
- Standardized the event contract so Sprint 2+ consumers read literal CSV headers first, then Sprint 2 discovery keys.
- Standardized the scrape cache contract on hashed JSON files under `cache/scrapes/`.
- Added the missing email-cache contract under `cache/emails/`.
- Fixed Sprint 4 cloud/demo guidance to preserve Sprint 2's `scrape_university()` dict return shape.
- Added explicit custom-URL SSRF/private-network rejection rules for discovery.
- Added entry-point docs so future agents can distinguish canonical docs from historical review artifacts.

## Remaining Notes

- Raw Category 3 source assets still live under `archived/Categories list/Category 3 IA West Smart Watch/`; implementation setup is expected to stage working copies into `Category 3 - IA West Smart Match CRM/data/`.
- The adversarial review report is retained as history, but it now carries a notice that it targets the pre-reconciliation draft.
