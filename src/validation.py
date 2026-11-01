"""Deterministic ontology and extracted-record validation."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


def load_ontology(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_extraction(record: dict[str, Any], ontology: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["record must be an object"]
    entities = record.get("entities")
    triples = record.get("triples")
    if not isinstance(entities, list):
        errors.append("entities must be a list")
    if not isinstance(triples, list):
        errors.append("triples must be a list")
    if errors:
        return errors
    entity_types = set(ontology["entity_types"])
    relation_defs = ontology["relationships"]
    labels: dict[str, str] = {}
    for index, entity in enumerate(entities):
        if not isinstance(entity, dict):
            errors.append(f"entities[{index}] must be an object")
            continue
        label, entity_type = entity.get("label"), entity.get("type")
        if not label or entity_type not in entity_types:
            errors.append(f"entities[{index}] requires label and valid type")
        elif label in labels and labels[label] != entity_type:
            errors.append(f"entity label has conflicting types: {label}")
        else:
            labels[label] = entity_type
    seen: set[tuple[str, str, str]] = set()
    for index, triple in enumerate(triples):
        if not isinstance(triple, dict):
            errors.append(f"triples[{index}] must be an object")
            continue
        subject, relation, object_ = triple.get("subject"), triple.get("relation"), triple.get("object")
        evidence = triple.get("evidence")
        if not all(isinstance(value, str) and value.strip() for value in (subject, relation, object_, evidence)):
            errors.append(f"triples[{index}] requires subject, relation, object, and evidence")
            continue
        if relation not in relation_defs:
            errors.append(f"unsupported relation: {relation}")
            continue
        if subject not in labels or object_ not in labels:
            errors.append(f"triple references unknown entity: {subject} -> {object_}")
            continue
        definition = relation_defs[relation]
        if labels[subject] != definition["subject"] or labels[object_] != definition["object"]:
            errors.append(f"incompatible types for relation: {relation}")
        key = (subject, relation, object_)
        if key in seen:
            errors.append(f"duplicate triple: {subject} | {relation} | {object_}")
        seen.add(key)
    return errors


def validation_summary(records: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(record.get("validation_status", "INVALID") for record in records)
    return dict(counts)
