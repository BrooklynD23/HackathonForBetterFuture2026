"""Gemini-powered intent parser for coordinator commands.

Pure Python — no Streamlit imports. Fully testable in isolation.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any

from src.config import GEMINI_API_KEY, GEMINI_TEXT_MODEL
from src.gemini_client import GeminiAPIError, generate_text

logger = logging.getLogger(__name__)

SUPPORTED_INTENTS: frozenset[str] = frozenset({
    "discover_events",
    "rank_speakers",
    "generate_outreach",
    "check_contacts",
    "unknown",
})

ACTION_REGISTRY: list[dict[str, str]] = [
    {"intent": "discover_events",   "agent": "Discovery Agent",  "description": "Scrape universities for new events"},
    {"intent": "rank_speakers",     "agent": "Matching Agent",   "description": "Rank speakers for a target event"},
    {"intent": "generate_outreach", "agent": "Outreach Agent",   "description": "Draft outreach emails for a match"},
    {"intent": "check_contacts",    "agent": "Contacts Agent",   "description": "Review POC contact status"},
]

_SYSTEM_PROMPT = """\
You are Jarvis, an AI coordinator assistant. Given a coordinator command and a list
of available agent actions, identify the best matching intent and return ONLY valid JSON.

Available actions:
{actions}

Response format (JSON only, no markdown):
{{
  "intent": "<one of the intent keys above, or 'unknown'>",
  "agent": "<agent display name>",
  "params": {{}},
  "reasoning": "<one sentence explaining why>"
}}
"""


@dataclass(frozen=True)
class ParsedIntent:
    """Immutable result of intent parsing.

    Carries all fields needed to construct an ActionProposal.
    """

    intent: str
    agent: str
    params: dict[str, Any]
    reasoning: str
    raw_text: str


def _strip_markdown_fence(text: str) -> str:
    """Remove triple-backtick fences that Gemini occasionally adds."""
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        inner = lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
        return "\n".join(inner).strip()
    return stripped


def parse_intent(text: str) -> ParsedIntent:
    """Parse coordinator text into a structured intent. Never raises.

    On any exception (GeminiAPIError, JSONDecodeError, KeyError, TypeError),
    returns ParsedIntent with intent="unknown".
    """
    actions_str = json.dumps(ACTION_REGISTRY, indent=2)
    system = _SYSTEM_PROMPT.format(actions=actions_str)
    try:
        raw = generate_text(
            messages=[{"role": "user", "content": text}],
            api_key=GEMINI_API_KEY,
            model=GEMINI_TEXT_MODEL,
            system_instruction=system,
            temperature=0.1,
            max_output_tokens=300,
            timeout=10.0,
        )
        cleaned = _strip_markdown_fence(raw)
        data = json.loads(cleaned)
        intent = data.get("intent", "unknown")
        if intent not in SUPPORTED_INTENTS:
            intent = "unknown"
        return ParsedIntent(
            intent=intent,
            agent=data.get("agent", "Jarvis"),
            params=data.get("params", {}),
            reasoning=data.get("reasoning", ""),
            raw_text=text,
        )
    except (GeminiAPIError, json.JSONDecodeError, KeyError, TypeError) as exc:
        logger.warning("Intent parsing failed: %s", exc)
        return ParsedIntent(
            intent="unknown",
            agent="Jarvis",
            params={},
            reasoning="",
            raw_text=text,
        )
