"""Conservative, reviewable entity canonicalization."""

from __future__ import annotations

import re


def canonical_key(label: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", " ".join(label.casefold().split()))


def canonicalize(labels: list[str]) -> tuple[dict[str, str], list[dict[str, str]]]:
    canonical: dict[str, str] = {}
    decisions: list[dict[str, str]] = []
    by_key: dict[str, str] = {}
    for label in labels:
        key = canonical_key(label)
        existing = by_key.get(key)
        if existing and existing != label:
            canonical[label] = existing
            decisions.append({"label": label, "canonical": existing, "decision": "MERGE_SAFE", "reason": "case/whitespace/punctuation normalization"})
        else:
            by_key[key] = label
            canonical[label] = label
            decisions.append({"label": label, "canonical": label, "decision": "KEEP", "reason": "no safe duplicate detected"})
    return canonical, decisions
