"""Command-line entry point for the prototype."""

from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path

from .config import ONTOLOGY_PATH, project_path
from .data_loader import load_courses, write_courses
from .evidence_gate import verify_evidence
from .preprocessing import clean_text
from .validation import load_ontology, validate_extraction
from .experiment_runner import CONDITIONS, run_condition
from .evaluation import precision_recall_f1, triple_key


def validate_dataset(path: Path) -> int:
    courses, invalid = load_courses(path)
    print(json.dumps({"valid_courses": len(courses), "invalid_rows": len(invalid)}, indent=2))
    return 0 if not invalid else 1


def run_smoke(input_path: Path, output_path: Path) -> int:
    courses, invalid = load_courses(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("course_id", "status", "reason"))
        writer.writeheader()
        for course in courses:
            writer.writerow({"course_id": course.course_id, "status": "LOADED", "reason": clean_text(course.description)})
        for row in invalid:
            writer.writerow({"course_id": row["course_id"], "status": "INVALID", "reason": row["reason"]})
    print(f"Smoke test wrote {len(courses)} valid and {len(invalid)} invalid records to {output_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="course-ontology", description="Evidence-gated course ontology prototype")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate-dataset")
    validate.add_argument("input", type=Path)
    smoke = subparsers.add_parser("smoke-test")
    smoke.add_argument("--input", type=Path, default=project_path("data", "raw", "sample_courses.csv"))
    smoke.add_argument("--output", type=Path, default=project_path("results", "smoke_test.csv"))
    experiment = subparsers.add_parser("run-experiment")
    experiment.add_argument("condition", choices=sorted(CONDITIONS))
    experiment.add_argument("--input", type=Path, default=project_path("data", "raw", "sample_courses.csv"))
    experiment.add_argument("--extractions", type=Path, required=True, help="Directory containing COURSE_ID.json files")
    experiment.add_argument("--output", type=Path, default=project_path("results"))
    experiment.add_argument("--review-queue", type=Path, default=project_path("results", "escalation_queue.csv"))
    experiment.add_argument("--overwrite", action="store_true")
    evaluate = subparsers.add_parser("evaluate")
    evaluate.add_argument("--predicted", type=Path, required=True)
    evaluate.add_argument("--annotated", type=Path, required=True)
    return parser


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = build_parser().parse_args()
    if args.command == "validate-dataset":
        return validate_dataset(args.input)
    if args.command == "smoke-test":
        return run_smoke(args.input, args.output)
    if args.command == "run-experiment":
        courses, invalid = load_courses(args.input)
        extracted = {}
        for course in courses:
            candidate = args.extractions / f"{course.course_id}.json"
            if candidate.exists():
                extracted[course.course_id] = json.loads(candidate.read_text(encoding="utf-8"))
        summary = run_condition(args.condition, courses, extracted, args.output / args.condition, args.review_queue, args.overwrite)
        print(json.dumps({"invalid_dataset_rows": len(invalid), **summary}, indent=2))
        return 0
    if args.command == "evaluate":
        predicted = {triple_key(row) for row in csv.DictReader(args.predicted.open(encoding="utf-8", newline=""))}
        annotated = {triple_key(row) for row in csv.DictReader(args.annotated.open(encoding="utf-8", newline="")) if row.get("supported", "").casefold() == "true"}
        print(json.dumps(precision_recall_f1(predicted, annotated).__dict__, indent=2))
        return 0
    return 2
