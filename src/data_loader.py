"""CSV loading and deterministic dataset validation."""

from __future__ import annotations

import csv
import logging
from dataclasses import dataclass
from pathlib import Path

REQUIRED_FIELDS = (
    "course_id",
    "course_name",
    "university",
    "department",
    "description",
    "source_url",
)


@dataclass(frozen=True)
class Course:
    course_id: str
    course_name: str
    university: str
    department: str
    description: str
    source_url: str

    def as_dict(self) -> dict[str, str]:
        return {field: getattr(self, field) for field in REQUIRED_FIELDS}


def load_courses(path: Path, logger: logging.Logger | None = None) -> tuple[list[Course], list[dict[str, str]]]:
    """Load valid rows and return invalid rows with explicit reasons."""
    logger = logger or logging.getLogger(__name__)
    valid: list[Course] = []
    invalid: list[dict[str, str]] = []
    seen: set[str] = set()
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [field for field in REQUIRED_FIELDS if field not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")
        for line_number, row in enumerate(reader, start=2):
            values = {field: (row.get(field) or "").strip() for field in REQUIRED_FIELDS}
            reasons: list[str] = []
            if any(not values[field] for field in REQUIRED_FIELDS):
                reasons.append("missing required field")
            if values["course_id"] in seen:
                reasons.append("duplicate course_id")
            if reasons:
                invalid.append({"line": str(line_number), "reason": "; ".join(reasons), **values})
                logger.warning("Skipping invalid course row %s: %s", line_number, "; ".join(reasons))
                continue
            seen.add(values["course_id"])
            valid.append(Course(**values))
    return valid, invalid


def write_courses(path: Path, courses: list[Course]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_FIELDS)
        writer.writeheader()
        writer.writerows(course.as_dict() for course in courses)
