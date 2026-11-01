"""Portable project configuration."""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = os.getenv("ONTOLOGY_MODEL", "qwen3:4b")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
ONTOLOGY_PATH = PROJECT_ROOT / "schemas" / "ontology.json"


def project_path(*parts: str) -> Path:
    return PROJECT_ROOT.joinpath(*parts)
