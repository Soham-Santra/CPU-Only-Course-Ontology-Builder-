"""Repeatable experiment-condition runner for already extracted records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import ONTOLOGY_PATH
from .data_loader import Course
from .evidence_gate import verify_evidence
from .escalation import append_review_item
from .validation import load_ontology, validate_extraction

CONDITIONS = {"baseline", "schema_validation", "evidence_gate", "escalation"}


def run_condition(
    condition: str,
    courses: list[Course],
    extracted: dict[str, dict[str, Any]],
    output_dir: Path,
    review_queue: Path | None = None,
    overwrite: bool = False,
) -> dict[str, int]:
    if condition not in CONDITIONS:
        raise ValueError(f"condition must be one of {sorted(CONDITIONS)}")
    if output_dir.exists() and any(output_dir.iterdir()) and not overwrite:
        raise FileExistsError(f"Output directory is not empty: {output_dir}; pass overwrite=True to replace files")
    ontology = load_ontology(ONTOLOGY_PATH)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = {"courses": 0, "valid": 0, "invalid": 0, "accepted": 0, "rejected": 0, "abstained": 0, "escalated": 0}
    for course in courses:
        record = extracted.get(course.course_id, {})
        errors = validate_extraction(record, ontology) if condition != "baseline" else []
        record = dict(record)
        record["validation_status"] = "VALID" if not errors else "INVALID"
        record["validation_errors"] = errors
        summary["courses"] += 1
        summary["valid" if not errors else "invalid"] += 1
        if condition in {"evidence_gate", "escalation"} and not errors:
            for triple in record.get("triples", []):
                result = verify_evidence(course.description, triple["subject"], triple["relation"], triple["object"], triple["evidence"])
                triple["evidence_decision"] = result.decision.value
                triple["evidence_reason"] = result.reason
                summary[result.decision.value.lower() + "ed" if result.decision.value != "ACCEPT" else "accepted"] += 1
                if result.decision.value == "ESCALATE" and review_queue:
                    append_review_item(review_queue, {"course_id": course.course_id, **triple, "reason": result.reason, "source_url": course.source_url})
        (output_dir / f"{course.course_id}.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
