"""Deterministic evidence-location gate with explicit heuristic limitations."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import re


class Decision(StrEnum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    ABSTAIN = "ABSTAIN"
    ESCALATE = "ESCALATE"


@dataclass(frozen=True)
class EvidenceResult:
    decision: Decision
    reason: str
    evidence: str


def verify_evidence(
    description: str,
    subject: str,
    relation: str,
    object_: str,
    evidence: str,
) -> EvidenceResult:
    if not evidence.strip():
        return EvidenceResult(Decision.REJECT, "evidence is missing", evidence)
    if evidence.casefold() not in description.casefold():
        return EvidenceResult(Decision.REJECT, "evidence was not found in source description", evidence)
    evidence_words = set(re.findall(r"[a-z0-9]+", evidence.casefold()))
    object_words = set(re.findall(r"[a-z0-9]+", object_.casefold()))
    overlap = evidence_words & object_words
    if not overlap:
        return EvidenceResult(Decision.ABSTAIN, "located evidence has no lexical overlap with object; semantic support is unverified", evidence)
    if len(overlap) == 1 and len(object_words) > 2:
        return EvidenceResult(Decision.ESCALATE, "evidence is located but support is ambiguous and needs review", evidence)
    return EvidenceResult(Decision.ACCEPT, "evidence is located and has lexical overlap; semantic verification remains heuristic", evidence)
