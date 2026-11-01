import json
import tempfile
import unittest
from pathlib import Path

from src.data_loader import load_courses
from src.evidence_gate import Decision, verify_evidence
from src.evaluation import precision_recall_f1
from src.validation import load_ontology, validate_extraction


ROOT = Path(__file__).resolve().parents[1]


class CoreTests(unittest.TestCase):
    def test_loads_sample_course(self):
        courses, invalid = load_courses(ROOT / "data" / "raw" / "sample_courses.csv")
        self.assertEqual(len(courses), 1)
        self.assertFalse(invalid)

    def test_duplicate_is_invalid(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "courses.csv"
            path.write_text((ROOT / "data" / "raw" / "sample_courses.csv").read_text(encoding="utf-8") +
                            "EXAMPLE-001,Duplicate,University,Department,Description,https://example.invalid/duplicate\n", encoding="utf-8")
            courses, invalid = load_courses(path)
            self.assertEqual(len(courses), 1)
            self.assertIn("duplicate course_id", invalid[0]["reason"])

    def test_validation_rejects_unsupported_relation(self):
        ontology = load_ontology(ROOT / "schemas" / "ontology.json")
        record = {"entities": [{"label": "Course", "type": "Course"}, {"label": "Topic", "type": "Topic"}],
                  "triples": [{"subject": "Course", "relation": "INVENTS", "object": "Topic", "evidence": "text"}]}
        self.assertTrue(any("unsupported relation" in error for error in validate_extraction(record, ontology)))

    def test_evidence_decisions(self):
        result = verify_evidence("Students learn arrays and queues.", "Course", "TEACHES", "arrays", "learn arrays")
        self.assertEqual(result.decision, Decision.ACCEPT)
        missing = verify_evidence("Students learn arrays.", "Course", "TEACHES", "queues", "learn queues")
        self.assertEqual(missing.decision, Decision.REJECT)

    def test_metrics(self):
        metrics = precision_recall_f1({"a", "b"}, {"b", "c"})
        self.assertEqual(metrics.precision, 0.5)
        self.assertEqual(metrics.recall, 0.5)
        self.assertEqual(metrics.f1, 0.5)


if __name__ == "__main__":
    unittest.main()
