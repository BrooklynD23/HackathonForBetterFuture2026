# API Reference

Base URL (local dev): `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs` (Swagger UI)

---

## Health

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Returns `{"status": "ok"}` |

---

## Portals (`/api/portals`)

All portal data and mock auth.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/portals/auth/mock-login` | Authenticate by email → returns role + redirect path |
| GET | `/api/portals/students` | List all students |
| GET | `/api/portals/students/{id}` | Student profile |
| GET | `/api/portals/students/{id}/recommendations` | AI event recommendations |
| GET | `/api/portals/students/{id}/registrations` | Event registrations + attendance |
| GET | `/api/portals/students/{id}/connection-suggestions` | Peer connection suggestions |
| GET | `/api/portals/students/{id}/nudge` | Retention nudge message |
| GET | `/api/portals/student-connections` | All student connection edges |
| GET | `/api/portals/event-coordinators` | List all coordinators |
| GET | `/api/portals/event-coordinators/{id}` | Coordinator profile |
| GET | `/api/portals/event-coordinators/{id}/threads` | Outreach threads |
| GET | `/api/portals/event-coordinators/{id}/meetings` | Scheduled meetings |
| GET | `/api/portals/event-coordinators/{id}/events` | Events managed by coordinator |
| GET | `/api/portals/volunteers/{id}` | Volunteer profile (match score, fatigue, recovery) |
| GET | `/api/portals/volunteers/{id}/assignments` | Volunteer assignment list with stage + match score |

---

## Matching (`/api/matching`)

8-factor AI matching engine.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/matching/rank` | Rank speakers for an event |
| POST | `/api/matching/batch-rank` | Rank speakers for multiple events |
| GET | `/api/matching/weights` | Current factor weights |
| POST | `/api/matching/weights` | Update factor weights |
| GET | `/api/matching/factors` | Factor metadata + descriptions |

---

## Outreach (`/api/outreach`)

Outreach generation and agentic workflow.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/outreach/generate` | Generate outreach email for a match |
| POST | `/api/outreach/agentic-workflow/stream` | SSE stream — 5-agent workflow (Scout → Copywriter → Scheduler → Planner → Pipeline) |
| GET | `/api/outreach/pipeline` | Current outreach pipeline state |
| PATCH | `/api/outreach/pipeline/{id}` | Update pipeline stage |

---

## Web Crawler (`/api/crawler`)

Gemini-grounded + Tavily web intelligence.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/crawler/feed` | SSE stream of crawl progress |
| POST | `/api/crawler/start` | Trigger a crawl |
| DELETE | `/api/crawler/clear` | Clear crawl results |
| GET | `/api/crawler/results` | Crawl result cache |
| GET | `/api/crawler/seeds` | Configured seed URLs |
| POST | `/api/crawler/seeds` | Add a seed URL |

---

## QR Attendance (`/api/qr`)

QR code generation and attendance tracking.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/qr/generate` | Generate QR code for an event |
| POST | `/api/qr/attendance/checkin` | Log an attendance check-in |
| GET | `/api/qr/attendance/history/{student_id}` | Student attendance history |
| GET | `/api/qr/stats` | Aggregate QR scan stats |

---

## Feedback (`/api/feedback`)

Coordinator accept/decline signals → matching weight learning.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/feedback/submit` | Submit coordinator feedback on a match |
| GET | `/api/feedback/stats` | Acceptance rate, pain score, recommended weight deltas |
| GET | `/api/feedback/weights` | Optimized weight snapshot |

---

## Calendar (`/api/calendar`)

Event coverage and volunteer recovery posture.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/calendar/events` | All calendar events with coverage status |
| GET | `/api/calendar/coverage` | Coverage summary (covered/open counts) |
| GET | `/api/calendar/recovery` | Volunteer recovery posture |

---

## Data (`/api/data`)

Raw CSV dataset access.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/data/volunteers` | Volunteer/speaker dataset |
| GET | `/api/data/events` | Event dataset |
| GET | `/api/data/courses` | Course schedule dataset |
