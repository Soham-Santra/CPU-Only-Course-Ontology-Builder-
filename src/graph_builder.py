"""Optional Neo4j loader using parameterized Cypher."""

from __future__ import annotations

import os
from typing import Any

from .canonicalization import canonical_key

RELATION_QUERY = """
MERGE (s:Entity {key: $subject_key})
  ON CREATE SET s.label = $subject
MERGE (o:Entity {key: $object_key})
  ON CREATE SET o.label = $object
MERGE (s)-[r:RELATION {course_id: $course_id, relation: $relation}]->(o)
SET r.evidence = $evidence, r.source_url = $source_url,
    r.model = $model, r.validation_status = $validation_status
"""


def load_records(records: list[dict[str, Any]]) -> int:
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise RuntimeError("The optional 'neo4j' package is required for graph loading.") from exc
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    if not all((uri, user, password)):
        raise RuntimeError("NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD must be configured.")
    driver = GraphDatabase.driver(uri, auth=(user, password))
    count = 0
    with driver:
        with driver.session() as session:
            for record in records:
                for triple in record.get("triples", []):
                    session.run(
                        RELATION_QUERY,
                        subject_key=canonical_key(triple["subject"]),
                        object_key=canonical_key(triple["object"]),
                        subject=triple["subject"],
                        object=triple["object"],
                        relation=triple["relation"],
                        course_id=record.get("course_id", ""),
                        evidence=triple.get("evidence", ""),
                        source_url=record.get("source_url", ""),
                        model=record.get("_metadata", {}).get("model", ""),
                        validation_status=record.get("validation_status", ""),
                    ).consume()
                    count += 1
    return count
