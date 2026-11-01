"""Human review queue for uncertain relationships."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ("course_id", "subject", "relation", "object", "evidence", "reason", "source_url", "review_decision", "reviewer", "reviewed_at")


def append_review_item(path: Path, item: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow({field: item.get(field, "") for field in FIELDS})


def review_item(path: Path, course_id: str, decision: str, reviewer: str) -> int:
    if decision not in {"ACCEPT", "REJECT", "UNRESOLVED"}:
        raise ValueError("decision must be ACCEPT, REJECT, or UNRESOLVED")
    rows = list(csv.DictReader(path.open("r", encoding="utf-8", newline="")))
    changed = 0
    for row in rows:
        if row["course_id"] == course_id and not row["review_decision"]:
            row["review_decision"] = decision
            row["reviewer"] = reviewer
            row["reviewed_at"] = datetime.now(timezone.utc).isoformat()
            changed += 1
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return changed
