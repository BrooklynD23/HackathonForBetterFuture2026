# Hackathon For Better Future 2026 - Category 3 SmartMatch CRM

## What This Is

This repository contains the IA West SmartMatch CRM hackathon build, with the active implementation in `Category 3 - IA West Smart Match CRM/`. The app is a Streamlit demo for event discovery, speaker matching, outreach generation, and coordinator-driven agent orchestration.

## Core Value

A coordinator can use voice or text to command an AI assistant that orchestrates parallel agents for event discovery, speaker matching, and outreach, with human approval gating every action.

## Shipped Milestones

- **v1.0 Sprint 5 Closeout (2026-03-21):** Runtime reliability fixes, documentation/governance reconciliation, and adversarial closeout audit remediation. Archive: [milestones/v1.0-ROADMAP.md](milestones/v1.0-ROADMAP.md)
- **v2.0 Jarvis Agent Coordinator (2026-03-24):** Voice I/O foundation, coordinator HITL state machine, agent tool wrappers with result bus, and NemoClaw-enabled live dashboard. Archive: [milestones/v2.0-ROADMAP.md](milestones/v2.0-ROADMAP.md)

## Current State

- Command Center supports text and voice interaction paths.
- Approval cards gate every proposed agent action.
- Tool wrappers dispatch discovery, ranking, outreach, and contact workflows.
- Swimlane dashboard renders real-time per-agent statuses.
- Demo-first constraints remain in effect (single-tenant, no production auth/scaling).

## Next Milestone Goals

- Define next milestone requirements from deferred scope (`VOICE-05`, `VOICE-06`, `ORCH-05`, `DASH-04`, and operational hardening items).
- Execute human UAT for microphone, speech synthesis, and end-to-end rehearsal paths.
- Convert accepted v2 technical debt into explicit phased backlog items with verification criteria.

## Constraints

- **Tech stack:** Python + Streamlit + pandas + Plotly + Gemini runtime, plus KittenTTS and NemoClaw integration paths.
- **Verification standard:** No phase is complete without direct test/demo evidence.
- **Human-in-the-loop:** No autonomous execution without coordinator approval.
- **Demo-first delivery:** Features must remain demoable inside Streamlit.

---
*Last updated: 2026-03-24 after v2.0 milestone completion*
