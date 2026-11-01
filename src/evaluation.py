"""Evaluation metrics against manual annotations; no model output is ground truth."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Metrics:
    precision: float
    recall: float
    f1: float


def precision_recall_f1(predicted: set[str], expected: set[str]) -> Metrics:
    true_positive = len(predicted & expected)
    precision = true_positive / len(predicted) if predicted else 0.0
    recall = true_positive / len(expected) if expected else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return Metrics(precision, recall, f1)


def triple_key(triple: dict[str, str]) -> str:
    return " | ".join(triple[field].strip().casefold() for field in ("subject", "relation", "object"))
