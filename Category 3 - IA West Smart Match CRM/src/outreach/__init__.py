"""Outreach tools for IA SmartMatch CRM."""

from src.outreach.email_gen import generate_outreach_email
from src.outreach.ics_generator import generate_ics

__all__ = ["generate_outreach_email", "generate_ics"]
