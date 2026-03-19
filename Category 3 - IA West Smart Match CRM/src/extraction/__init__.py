"""Extraction subpackage — LLM-based structured data extraction from HTML."""

from src.extraction.llm_extractor import (
    EXTRACTED_EVENT_SCHEMA,
    extract_events,
    preprocess_html,
)

__all__ = ["extract_events", "preprocess_html", "EXTRACTED_EVENT_SCHEMA"]
