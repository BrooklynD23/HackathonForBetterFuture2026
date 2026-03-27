"""Create the demo fallback SQLite database used by Phase 14 visual resilience."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEMO_DB_PATH = PROJECT_ROOT / "data" / "demo.db"

SPECIALISTS = [
    {
        "name": "Dr. Sarah Chen",
        "board_role": "President",
        "metro_region": "Los Angeles - West",
        "company": "TechBridge AI",
        "title": "VP Data Science",
        "expertise_tags": "AI strategy, machine learning, hackathons",
        "initials": "DSC",
    },
    {
        "name": "Marcus Webb",
        "board_role": "Vice President",
        "metro_region": "San Diego",
        "company": "West Coast Ventures",
        "title": "Startup Advisor",
        "expertise_tags": "founder coaching, venture readiness, pitch review",
        "initials": "MW",
    },
    {
        "name": "Priya Nair",
        "board_role": "Treasurer",
        "metro_region": "Bay Area",
        "company": "Cloud Harbor",
        "title": "Director of Product Analytics",
        "expertise_tags": "analytics, dashboards, product strategy",
        "initials": "PN",
    },
    {
        "name": "James Rodriguez",
        "board_role": "Secretary",
        "metro_region": "Orange County",
        "company": "Insight Works",
        "title": "Research Operations Lead",
        "expertise_tags": "research ops, customer insight, survey design",
        "initials": "JR",
    },
    {
        "name": "Dr. Emily Park",
        "board_role": "Member-at-Large",
        "metro_region": "Portland",
        "company": "Civic Data Lab",
        "title": "Principal Research Scientist",
        "expertise_tags": "ethics, civic tech, responsible AI",
        "initials": "DEP",
    },
    {
        "name": "Kevin O'Brien",
        "board_role": "Member-at-Large",
        "metro_region": "Seattle",
        "company": "Retail Signal",
        "title": "Head of Market Intelligence",
        "expertise_tags": "retail analytics, segmentation, growth",
        "initials": "KOB",
    },
    {
        "name": "Aisha Johnson",
        "board_role": "Programs Chair",
        "metro_region": "Sacramento",
        "company": "Community Insight Partners",
        "title": "Program Director",
        "expertise_tags": "community outreach, partnerships, event programming",
        "initials": "AJ",
    },
    {
        "name": "Dr. Michael Torres",
        "board_role": "Education Chair",
        "metro_region": "Phoenix",
        "company": "Desert State University",
        "title": "Professor of Information Systems",
        "expertise_tags": "higher ed, data literacy, student engagement",
        "initials": "DMT",
    },
    {
        "name": "Lisa Chang",
        "board_role": "Membership Chair",
        "metro_region": "San Francisco",
        "company": "North Bay Research",
        "title": "Client Services Director",
        "expertise_tags": "membership growth, account strategy, sponsorships",
        "initials": "LC",
    },
    {
        "name": "Robert Kim",
        "board_role": "Member-at-Large",
        "metro_region": "Las Vegas",
        "company": "Signal Path Consulting",
        "title": "Innovation Consultant",
        "expertise_tags": "innovation programs, operations, executive workshops",
        "initials": "RK",
    },
]

CPP_EVENTS = [
    {
        "Event / Program": "AI for a Better Future Hackathon",
        "Category": "Innovation",
        "Recurrence (typical)": "Annual spring hackathon",
        "Host / Unit": "Cal Poly Pomona",
        "Volunteer Roles (fit)": "Keynote, mentor, judge",
        "Primary Audience": "Students and early-career builders",
        "Public URL": "https://www.insightsassociation.org/ai-hackathon",
        "Point(s) of Contact (published)": "Innovation Programs Team",
        "Contact Email / Phone (published)": "programs@iawest.org",
    },
    {
        "Event / Program": "ITC Conference",
        "Category": "Conference",
        "Recurrence (typical)": "Annual fall conference",
        "Host / Unit": "Insights Association",
        "Volunteer Roles (fit)": "Speaker, panelist",
        "Primary Audience": "Industry practitioners",
        "Public URL": "https://www.insightsassociation.org/itc",
        "Point(s) of Contact (published)": "Conference Team",
        "Contact Email / Phone (published)": "events@iawest.org",
    },
    {
        "Event / Program": "Bronco Startup Challenge",
        "Category": "Competition",
        "Recurrence (typical)": "Quarterly pitch challenge",
        "Host / Unit": "Cal Poly Pomona Entrepreneurship Center",
        "Volunteer Roles (fit)": "Judge, workshop lead",
        "Primary Audience": "Student founders",
        "Public URL": "https://www.insightsassociation.org/bronco-startup",
        "Point(s) of Contact (published)": "CPP Entrepreneurship Center",
        "Contact Email / Phone (published)": "startup@cpp.edu",
    },
    {
        "Event / Program": "IA West Annual Summit",
        "Category": "Summit",
        "Recurrence (typical)": "Annual member summit",
        "Host / Unit": "IA West Chapter",
        "Volunteer Roles (fit)": "Keynote, moderator, networking host",
        "Primary Audience": "Chapter members and sponsors",
        "Public URL": "https://www.insightsassociation.org/ia-west-summit",
        "Point(s) of Contact (published)": "Chapter Leadership",
        "Contact Email / Phone (published)": "leadership@iawest.org",
    },
    {
        "Event / Program": "Tech Career Fair",
        "Category": "Career Fair",
        "Recurrence (typical)": "Biannual campus fair",
        "Host / Unit": "West Coast Career Consortium",
        "Volunteer Roles (fit)": "Panelist, recruiter, mentor",
        "Primary Audience": "Undergraduate and graduate students",
        "Public URL": "https://www.insightsassociation.org/tech-career-fair",
        "Point(s) of Contact (published)": "Career Partnerships Team",
        "Contact Email / Phone (published)": "careerfair@iawest.org",
    },
]

EVENT_CALENDAR = [
    {
        "IA Event Date": "2026-04-09",
        "Region": "Los Angeles - West",
        "Nearby Universities": "Cal Poly Pomona, UCLA, USC",
        "Suggested Lecture Window": "Apr 7-10",
        "Course Alignment": "AI product strategy",
    },
    {
        "IA Event Date": "2026-04-18",
        "Region": "Bay Area",
        "Nearby Universities": "UC Berkeley, San Jose State, Stanford",
        "Suggested Lecture Window": "Apr 15-18",
        "Course Alignment": "Analytics and product insight",
    },
    {
        "IA Event Date": "2026-04-24",
        "Region": "San Diego",
        "Nearby Universities": "UC San Diego, SDSU",
        "Suggested Lecture Window": "Apr 22-25",
        "Course Alignment": "Founder storytelling and research",
    },
    {
        "IA Event Date": "2026-05-02",
        "Region": "Portland",
        "Nearby Universities": "Portland State, Oregon State",
        "Suggested Lecture Window": "Apr 30-May 3",
        "Course Alignment": "Ethics and civic innovation",
    },
    {
        "IA Event Date": "2026-05-14",
        "Region": "Phoenix",
        "Nearby Universities": "Arizona State, Grand Canyon University",
        "Suggested Lecture Window": "May 12-15",
        "Course Alignment": "Student talent development",
    },
]

PIPELINE_STAGE_ORDER = {
    "Matched": "0",
    "Contacted": "1",
    "Confirmed": "2",
    "Attended": "3",
    "Member Inquiry": "4",
}

PIPELINE_STAGE_SEQUENCE = (
    ["Matched"] * 15
    + ["Contacted"] * 12
    + ["Confirmed"] * 8
    + ["Attended"] * 4
    + ["Member Inquiry"]
)

CALENDAR_EVENTS = [
    {
        "event_id": "demo-event-01",
        "event_name": "AI for a Better Future Hackathon",
        "event_date": "2026-04-09",
        "region": "Los Angeles - West",
        "nearby_universities": ["Cal Poly Pomona", "UCLA", "USC"],
        "suggested_lecture_window": "Apr 7-10",
        "course_alignment": "AI product strategy",
        "coverage_status": "covered",
        "coverage_label": "IA covered",
        "coverage_ratio": 0.83,
        "assigned_volunteers": ["Dr. Sarah Chen", "Marcus Webb"],
        "assignment_count": 2,
        "open_slots": 1,
        "status_color": "#005394",
    },
    {
        "event_id": "demo-event-02",
        "event_name": "ITC Conference",
        "event_date": "2026-04-18",
        "region": "Bay Area",
        "nearby_universities": ["UC Berkeley", "San Jose State", "Stanford"],
        "suggested_lecture_window": "Apr 15-18",
        "course_alignment": "Analytics and product insight",
        "coverage_status": "partial",
        "coverage_label": "Partial coverage",
        "coverage_ratio": 0.52,
        "assigned_volunteers": ["Priya Nair"],
        "assignment_count": 1,
        "open_slots": 2,
        "status_color": "#c47c00",
    },
    {
        "event_id": "demo-event-03",
        "event_name": "Bronco Startup Challenge",
        "event_date": "2026-04-24",
        "region": "San Diego",
        "nearby_universities": ["UC San Diego", "SDSU"],
        "suggested_lecture_window": "Apr 22-25",
        "course_alignment": "Founder storytelling and research",
        "coverage_status": "covered",
        "coverage_label": "IA covered",
        "coverage_ratio": 0.78,
        "assigned_volunteers": ["Marcus Webb", "Lisa Chang"],
        "assignment_count": 2,
        "open_slots": 1,
        "status_color": "#005394",
    },
    {
        "event_id": "demo-event-04",
        "event_name": "IA West Annual Summit",
        "event_date": "2026-05-02",
        "region": "Portland",
        "nearby_universities": ["Portland State", "Oregon State"],
        "suggested_lecture_window": "Apr 30-May 3",
        "course_alignment": "Ethics and civic innovation",
        "coverage_status": "partial",
        "coverage_label": "Partial coverage",
        "coverage_ratio": 0.47,
        "assigned_volunteers": ["Dr. Emily Park"],
        "assignment_count": 1,
        "open_slots": 2,
        "status_color": "#c47c00",
    },
    {
        "event_id": "demo-event-05",
        "event_name": "Tech Career Fair",
        "event_date": "2026-05-14",
        "region": "Phoenix",
        "nearby_universities": ["Arizona State", "Grand Canyon University"],
        "suggested_lecture_window": "May 12-15",
        "course_alignment": "Student talent development",
        "coverage_status": "needs_coverage",
        "coverage_label": "Needs volunteers",
        "coverage_ratio": 0.18,
        "assigned_volunteers": [],
        "assignment_count": 0,
        "open_slots": 3,
        "status_color": "#d14343",
    },
]

CALENDAR_ASSIGNMENTS = [
    {
        "assignment_id": "demo-assignment-01",
        "event_id": "demo-event-01",
        "event_name": "AI for a Better Future Hackathon",
        "event_date": "2026-04-09",
        "calendar_event_date": "2026-04-09",
        "region": "Los Angeles - West",
        "calendar_region": "Los Angeles - West",
        "volunteer_name": "Dr. Sarah Chen",
        "speaker_name": "Dr. Sarah Chen",
        "volunteer_title": "VP Data Science",
        "volunteer_company": "TechBridge AI",
        "speaker_region": "Los Angeles - West",
        "stage": "Attended",
        "stage_order": 3,
        "match_score": 0.93,
        "rank": 1,
        "travel_burden": 0.12,
        "event_cadence": 0.28,
        "recent_assignment_count": 2,
        "days_since_last_assignment": 18,
        "volunteer_fatigue": 0.18,
        "recovery_status": "Available",
        "recovery_label": "Available",
        "coverage_status": "covered",
        "coverage_label": "IA covered",
        "status_color": "#005394",
        "status_tone": "blue",
        "coverage_ratio": 0.83,
    },
    {
        "assignment_id": "demo-assignment-02",
        "event_id": "demo-event-02",
        "event_name": "ITC Conference",
        "event_date": "2026-04-18",
        "calendar_event_date": "2026-04-18",
        "region": "Bay Area",
        "calendar_region": "Bay Area",
        "volunteer_name": "Priya Nair",
        "speaker_name": "Priya Nair",
        "volunteer_title": "Director of Product Analytics",
        "volunteer_company": "Cloud Harbor",
        "speaker_region": "Bay Area",
        "stage": "Confirmed",
        "stage_order": 2,
        "match_score": 0.89,
        "rank": 1,
        "travel_burden": 0.21,
        "event_cadence": 0.41,
        "recent_assignment_count": 3,
        "days_since_last_assignment": 9,
        "volunteer_fatigue": 0.46,
        "recovery_status": "Needs Rest",
        "recovery_label": "Needs Rest",
        "coverage_status": "partial",
        "coverage_label": "Partial coverage",
        "status_color": "#c47c00",
        "status_tone": "amber",
        "coverage_ratio": 0.52,
    },
    {
        "assignment_id": "demo-assignment-03",
        "event_id": "demo-event-03",
        "event_name": "Bronco Startup Challenge",
        "event_date": "2026-04-24",
        "calendar_event_date": "2026-04-24",
        "region": "San Diego",
        "calendar_region": "San Diego",
        "volunteer_name": "Marcus Webb",
        "speaker_name": "Marcus Webb",
        "volunteer_title": "Startup Advisor",
        "volunteer_company": "West Coast Ventures",
        "speaker_region": "San Diego",
        "stage": "Confirmed",
        "stage_order": 2,
        "match_score": 0.87,
        "rank": 1,
        "travel_burden": 0.18,
        "event_cadence": 0.36,
        "recent_assignment_count": 4,
        "days_since_last_assignment": 6,
        "volunteer_fatigue": 0.62,
        "recovery_status": "Needs Rest",
        "recovery_label": "Needs Rest",
        "coverage_status": "covered",
        "coverage_label": "IA covered",
        "status_color": "#005394",
        "status_tone": "blue",
        "coverage_ratio": 0.78,
    },
]

QR_STATS = {
    "generated_count": 5,
    "scan_count": 42,
    "membership_interest_count": 12,
    "conversion_rate": round(12 / 42, 4),
    "unique_speakers": 5,
    "unique_events": 5,
    "filters": {"speaker_name": None, "event_name": None, "referral_code": None},
    "referral_codes": [
        {
            "referral_code": "IAW-SARAHAI24",
            "speaker_name": "Dr. Sarah Chen",
            "speaker_title": "VP Data Science",
            "speaker_company": "TechBridge AI",
            "event_name": "AI for a Better Future Hackathon",
            "generated_at": "2026-03-18T09:00:00Z",
            "destination_url": "https://www.insightsassociation.org/join",
            "scan_url": "http://127.0.0.1:8000/api/qr/scan/IAW-SARAHAI24",
            "scan_count": 15,
            "membership_interest_count": 5,
            "conversion_rate": 0.3333,
            "last_scanned_at": "2026-03-24T18:05:00Z",
            "qr_data_url": None,
        },
        {
            "referral_code": "IAW-MARCUSITC",
            "speaker_name": "Marcus Webb",
            "speaker_title": "Startup Advisor",
            "speaker_company": "West Coast Ventures",
            "event_name": "ITC Conference",
            "generated_at": "2026-03-19T10:15:00Z",
            "destination_url": "https://www.insightsassociation.org/join",
            "scan_url": "http://127.0.0.1:8000/api/qr/scan/IAW-MARCUSITC",
            "scan_count": 9,
            "membership_interest_count": 2,
            "conversion_rate": 0.2222,
            "last_scanned_at": "2026-03-24T15:10:00Z",
            "qr_data_url": None,
        },
        {
            "referral_code": "IAW-PRIYABRON",
            "speaker_name": "Priya Nair",
            "speaker_title": "Director of Product Analytics",
            "speaker_company": "Cloud Harbor",
            "event_name": "Bronco Startup Challenge",
            "generated_at": "2026-03-20T08:45:00Z",
            "destination_url": "https://www.insightsassociation.org/join",
            "scan_url": "http://127.0.0.1:8000/api/qr/scan/IAW-PRIYABRON",
            "scan_count": 7,
            "membership_interest_count": 2,
            "conversion_rate": 0.2857,
            "last_scanned_at": "2026-03-23T13:20:00Z",
            "qr_data_url": None,
        },
        {
            "referral_code": "IAW-EMILYSUMM",
            "speaker_name": "Dr. Emily Park",
            "speaker_title": "Principal Research Scientist",
            "speaker_company": "Civic Data Lab",
            "event_name": "IA West Annual Summit",
            "generated_at": "2026-03-21T11:30:00Z",
            "destination_url": "https://www.insightsassociation.org/join",
            "scan_url": "http://127.0.0.1:8000/api/qr/scan/IAW-EMILYSUMM",
            "scan_count": 6,
            "membership_interest_count": 2,
            "conversion_rate": 0.3333,
            "last_scanned_at": "2026-03-23T17:45:00Z",
            "qr_data_url": None,
        },
        {
            "referral_code": "IAW-LISACAREER",
            "speaker_name": "Lisa Chang",
            "speaker_title": "Client Services Director",
            "speaker_company": "North Bay Research",
            "event_name": "Tech Career Fair",
            "generated_at": "2026-03-22T14:10:00Z",
            "destination_url": "https://www.insightsassociation.org/join",
            "scan_url": "http://127.0.0.1:8000/api/qr/scan/IAW-LISACAREER",
            "scan_count": 5,
            "membership_interest_count": 1,
            "conversion_rate": 0.2,
            "last_scanned_at": "2026-03-22T18:55:00Z",
            "qr_data_url": None,
        },
    ],
    "recent_scans": [
        {
            "referral_code": "IAW-SARAHAI24",
            "speaker_name": "Dr. Sarah Chen",
            "event_name": "AI for a Better Future Hackathon",
            "scanned_at": "2026-03-24T18:05:00Z",
            "membership_interest": True,
        },
        {
            "referral_code": "IAW-MARCUSITC",
            "speaker_name": "Marcus Webb",
            "event_name": "ITC Conference",
            "scanned_at": "2026-03-24T15:10:00Z",
            "membership_interest": False,
        },
        {
            "referral_code": "IAW-PRIYABRON",
            "speaker_name": "Priya Nair",
            "event_name": "Bronco Startup Challenge",
            "scanned_at": "2026-03-23T13:20:00Z",
            "membership_interest": True,
        },
    ],
}

FEEDBACK_STATS = {
    "total_feedback": 8,
    "accepted": 5,
    "declined": 3,
    "acceptance_rate": 0.625,
    "attended_count": 4,
    "membership_interest_count": 3,
    "membership_interest_rate": 0.6,
    "average_coordinator_rating": 4.2,
    "average_match_score_accepted": 0.86,
    "average_match_score_declined": 0.68,
    "pain_score": 18.4,
    "decline_reasons": [
        {"reason": "Schedule conflict", "count": 2},
        {"reason": "Topic mismatch", "count": 1},
    ],
    "event_outcomes": [
        {"outcome": "attended", "count": 4},
        {"outcome": "rescheduled", "count": 1},
    ],
    "trend": [
        {"date": "2026-03-12", "feedback_count": 2, "accepted": 1, "declined": 1, "acceptance_rate": 0.5},
        {"date": "2026-03-16", "feedback_count": 2, "accepted": 1, "declined": 1, "acceptance_rate": 0.5},
        {"date": "2026-03-20", "feedback_count": 2, "accepted": 2, "declined": 0, "acceptance_rate": 1.0},
        {"date": "2026-03-24", "feedback_count": 2, "accepted": 1, "declined": 1, "acceptance_rate": 0.5},
    ],
    "default_weights": {
        "topic_relevance": 0.22,
        "role_fit": 0.18,
        "geographic_proximity": 0.18,
        "calendar_fit": 0.12,
        "volunteer_fatigue": 0.10,
        "event_urgency": 0.05,
        "coverage_diversity": 0.05,
        "historical_conversion": 0.05,
        "student_interest": 0.05,
    },
    "current_weights": {
        "topic_relevance": 0.24,
        "role_fit": 0.17,
        "geographic_proximity": 0.16,
        "calendar_fit": 0.13,
        "volunteer_fatigue": 0.11,
        "event_urgency": 0.05,
        "coverage_diversity": 0.05,
        "historical_conversion": 0.05,
        "student_interest": 0.04,
    },
    "suggested_weights": {
        "topic_relevance": 0.24,
        "role_fit": 0.17,
        "geographic_proximity": 0.16,
        "calendar_fit": 0.13,
        "volunteer_fatigue": 0.11,
        "event_urgency": 0.05,
        "coverage_diversity": 0.05,
        "historical_conversion": 0.05,
        "student_interest": 0.04,
    },
    "recommended_adjustments": [
        {
            "factor": "topic_relevance",
            "from_weight": 0.22,
            "to_weight": 0.24,
            "delta": 0.02,
            "rationale": "Accepted matches consistently aligned to event themes.",
        },
        {
            "factor": "volunteer_fatigue",
            "from_weight": 0.10,
            "to_weight": 0.11,
            "delta": 0.01,
            "rationale": "Recent staffing load should weigh slightly more heavily for follow-up scheduling.",
        },
    ],
    "weight_history": [
        {
            "timestamp": "2026-03-14T08:00:00Z",
            "total_feedback": 3,
            "accepted": 2,
            "declined": 1,
            "acceptance_rate": 0.6667,
            "pain_score": 22.1,
            "weights": {
                "topic_relevance": 0.23,
                "role_fit": 0.18,
                "geographic_proximity": 0.17,
                "calendar_fit": 0.12,
                "volunteer_fatigue": 0.10,
                "event_urgency": 0.05,
                "coverage_diversity": 0.05,
                "historical_conversion": 0.05,
                "student_interest": 0.05,
            },
            "baseline_weights": {
                "topic_relevance": 0.22,
                "role_fit": 0.18,
                "geographic_proximity": 0.18,
                "calendar_fit": 0.12,
                "volunteer_fatigue": 0.10,
                "event_urgency": 0.05,
                "coverage_diversity": 0.05,
                "historical_conversion": 0.05,
                "student_interest": 0.05,
            },
            "adjustments": [
                {
                    "factor": "topic_relevance",
                    "from_weight": 0.22,
                    "to_weight": 0.23,
                    "delta": 0.01,
                    "rationale": "Early wins favored topic-aligned speakers.",
                }
            ],
        },
        {
            "timestamp": "2026-03-24T09:30:00Z",
            "total_feedback": 8,
            "accepted": 5,
            "declined": 3,
            "acceptance_rate": 0.625,
            "pain_score": 18.4,
            "weights": {
                "topic_relevance": 0.24,
                "role_fit": 0.17,
                "geographic_proximity": 0.16,
                "calendar_fit": 0.13,
                "volunteer_fatigue": 0.11,
                "event_urgency": 0.05,
                "coverage_diversity": 0.05,
                "historical_conversion": 0.05,
                "student_interest": 0.04,
            },
            "baseline_weights": {
                "topic_relevance": 0.22,
                "role_fit": 0.18,
                "geographic_proximity": 0.18,
                "calendar_fit": 0.12,
                "volunteer_fatigue": 0.10,
                "event_urgency": 0.05,
                "coverage_diversity": 0.05,
                "historical_conversion": 0.05,
                "student_interest": 0.05,
            },
            "adjustments": [
                {
                    "factor": "topic_relevance",
                    "from_weight": 0.22,
                    "to_weight": 0.24,
                    "delta": 0.02,
                    "rationale": "Accepted matches consistently aligned to event themes.",
                },
                {
                    "factor": "volunteer_fatigue",
                    "from_weight": 0.10,
                    "to_weight": 0.11,
                    "delta": 0.01,
                    "rationale": "Recent staffing load should weigh slightly more heavily for follow-up scheduling.",
                },
            ],
        },
    ],
}


def build_pipeline_rows() -> list[dict[str, str]]:
    speaker_names = [entry["name"] for entry in SPECIALISTS]
    event_names = [entry["Event / Program"] for entry in CPP_EVENTS]
    rows: list[dict[str, str]] = []
    for index, stage in enumerate(PIPELINE_STAGE_SEQUENCE):
        event_name = event_names[index % len(event_names)]
        speaker_name = speaker_names[(index * 3) % len(speaker_names)]
        score = max(0.58, 0.94 - (index * 0.009))
        rows.append(
            {
                "event_name": event_name,
                "speaker_name": speaker_name,
                "match_score": f"{score:.2f}",
                "rank": str((index % 8) + 1),
                "stage": stage,
                "stage_order": PIPELINE_STAGE_ORDER[stage],
            }
        )
    return rows


def create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE specialists (
            name TEXT,
            board_role TEXT,
            metro_region TEXT,
            company TEXT,
            title TEXT,
            expertise_tags TEXT,
            initials TEXT
        );

        CREATE TABLE cpp_events (
            "Event / Program" TEXT,
            Category TEXT,
            "Recurrence (typical)" TEXT,
            "Host / Unit" TEXT,
            "Volunteer Roles (fit)" TEXT,
            "Primary Audience" TEXT,
            "Public URL" TEXT,
            "Point(s) of Contact (published)" TEXT,
            "Contact Email / Phone (published)" TEXT
        );

        CREATE TABLE pipeline (
            event_name TEXT,
            speaker_name TEXT,
            match_score TEXT,
            rank TEXT,
            stage TEXT,
            stage_order TEXT
        );

        CREATE TABLE event_calendar (
            "IA Event Date" TEXT,
            Region TEXT,
            "Nearby Universities" TEXT,
            "Suggested Lecture Window" TEXT,
            "Course Alignment" TEXT
        );

        CREATE TABLE calendar_events (
            event_id TEXT,
            event_name TEXT,
            event_date TEXT,
            region TEXT,
            nearby_universities TEXT,
            suggested_lecture_window TEXT,
            course_alignment TEXT,
            coverage_status TEXT,
            coverage_label TEXT,
            coverage_ratio REAL,
            assigned_volunteers TEXT,
            assignment_count INTEGER,
            open_slots INTEGER,
            status_color TEXT
        );

        CREATE TABLE calendar_assignments (
            assignment_id TEXT,
            event_id TEXT,
            event_name TEXT,
            event_date TEXT,
            calendar_event_date TEXT,
            region TEXT,
            calendar_region TEXT,
            volunteer_name TEXT,
            speaker_name TEXT,
            volunteer_title TEXT,
            volunteer_company TEXT,
            speaker_region TEXT,
            stage TEXT,
            stage_order INTEGER,
            match_score REAL,
            rank INTEGER,
            travel_burden REAL,
            event_cadence REAL,
            recent_assignment_count INTEGER,
            days_since_last_assignment INTEGER,
            volunteer_fatigue REAL,
            recovery_status TEXT,
            recovery_label TEXT,
            coverage_status TEXT,
            coverage_label TEXT,
            status_color TEXT,
            status_tone TEXT,
            coverage_ratio REAL
        );

        CREATE TABLE qr_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payload_json TEXT NOT NULL
        );

        CREATE TABLE feedback_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payload_json TEXT NOT NULL
        );
        """
    )


def insert_seed_data(connection: sqlite3.Connection) -> None:
    connection.executemany(
        """
        INSERT INTO specialists (
            name, board_role, metro_region, company, title, expertise_tags, initials
        ) VALUES (
            :name, :board_role, :metro_region, :company, :title, :expertise_tags, :initials
        )
        """,
        SPECIALISTS,
    )
    connection.executemany(
        """
        INSERT INTO cpp_events (
            "Event / Program", Category, "Recurrence (typical)", "Host / Unit",
            "Volunteer Roles (fit)", "Primary Audience", "Public URL",
            "Point(s) of Contact (published)", "Contact Email / Phone (published)"
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        [
            (
                record["Event / Program"],
                record["Category"],
                record["Recurrence (typical)"],
                record["Host / Unit"],
                record["Volunteer Roles (fit)"],
                record["Primary Audience"],
                record["Public URL"],
                record["Point(s) of Contact (published)"],
                record["Contact Email / Phone (published)"],
            )
            for record in CPP_EVENTS
        ],
    )
    connection.executemany(
        """
        INSERT INTO pipeline (
            event_name, speaker_name, match_score, rank, stage, stage_order
        ) VALUES (
            :event_name, :speaker_name, :match_score, :rank, :stage, :stage_order
        )
        """,
        build_pipeline_rows(),
    )
    connection.executemany(
        """
        INSERT INTO event_calendar (
            "IA Event Date", Region, "Nearby Universities",
            "Suggested Lecture Window", "Course Alignment"
        ) VALUES (
            ?, ?, ?, ?, ?
        )
        """,
        [
            (
                record["IA Event Date"],
                record["Region"],
                record["Nearby Universities"],
                record["Suggested Lecture Window"],
                record["Course Alignment"],
            )
            for record in EVENT_CALENDAR
        ],
    )
    connection.executemany(
        """
        INSERT INTO calendar_events (
            event_id, event_name, event_date, region, nearby_universities,
            suggested_lecture_window, course_alignment, coverage_status,
            coverage_label, coverage_ratio, assigned_volunteers,
            assignment_count, open_slots, status_color
        ) VALUES (
            :event_id, :event_name, :event_date, :region, :nearby_universities,
            :suggested_lecture_window, :course_alignment, :coverage_status,
            :coverage_label, :coverage_ratio, :assigned_volunteers,
            :assignment_count, :open_slots, :status_color
        )
        """,
        [
            {
                **record,
                "nearby_universities": json.dumps(record["nearby_universities"]),
                "assigned_volunteers": json.dumps(record["assigned_volunteers"]),
            }
            for record in CALENDAR_EVENTS
        ],
    )
    connection.executemany(
        """
        INSERT INTO calendar_assignments (
            assignment_id, event_id, event_name, event_date, calendar_event_date,
            region, calendar_region, volunteer_name, speaker_name, volunteer_title,
            volunteer_company, speaker_region, stage, stage_order, match_score, rank,
            travel_burden, event_cadence, recent_assignment_count,
            days_since_last_assignment, volunteer_fatigue, recovery_status,
            recovery_label, coverage_status, coverage_label, status_color,
            status_tone, coverage_ratio
        ) VALUES (
            :assignment_id, :event_id, :event_name, :event_date, :calendar_event_date,
            :region, :calendar_region, :volunteer_name, :speaker_name, :volunteer_title,
            :volunteer_company, :speaker_region, :stage, :stage_order, :match_score, :rank,
            :travel_burden, :event_cadence, :recent_assignment_count,
            :days_since_last_assignment, :volunteer_fatigue, :recovery_status,
            :recovery_label, :coverage_status, :coverage_label, :status_color,
            :status_tone, :coverage_ratio
        )
        """,
        CALENDAR_ASSIGNMENTS,
    )
    connection.execute(
        "INSERT INTO qr_stats (payload_json) VALUES (?)",
        (json.dumps(QR_STATS, sort_keys=True),),
    )
    connection.execute(
        "INSERT INTO feedback_stats (payload_json) VALUES (?)",
        (json.dumps(FEEDBACK_STATS, sort_keys=True),),
    )


def main() -> None:
    DEMO_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DEMO_DB_PATH.exists():
        DEMO_DB_PATH.unlink()

    connection = sqlite3.connect(DEMO_DB_PATH)
    try:
        create_schema(connection)
        insert_seed_data(connection)
        connection.commit()
    finally:
        connection.close()

    print(f"Seeded demo database: {DEMO_DB_PATH}")


if __name__ == "__main__":
    main()
