"""Meaning-preserving text preprocessing."""

from __future__ import annotations

import re


def clean_text(text: str) -> str:
    """Normalize whitespace without removing words or punctuation."""
    return re.sub(r"\s+", " ", text).strip()
