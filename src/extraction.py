"""Ollama extraction integration with reproducible raw and parsed outputs."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any
from urllib.request import urlopen

from .config import DEFAULT_MODEL, OLLAMA_HOST


def verify_ollama(model: str = DEFAULT_MODEL, host: str = OLLAMA_HOST) -> tuple[bool, str]:
    try:
        with urlopen(f"{host.rstrip('/')}/api/tags", timeout=5) as response:
            payload = json.load(response)
        names = {item.get("name") for item in payload.get("models", [])}
        if model not in names:
            return False, f"model {model!r} is not installed; no download was attempted"
        return True, "Ollama server and configured model are available"
    except Exception as exc:
        return False, f"Ollama is unavailable: {exc}"


def extract_course(course: dict[str, str], prompt_template: str, model: str = DEFAULT_MODEL, host: str = OLLAMA_HOST) -> dict[str, Any]:
    try:
        import ollama
    except ImportError as exc:
        raise RuntimeError("The optional 'ollama' package is required for extraction. Install requirements.txt.") from exc
    description = course["description"] if isinstance(course, dict) else course.description
    prompt = prompt_template.replace("{description}", description)
    started = time.perf_counter()
    response = ollama.generate(model=model, prompt=prompt, format="json", options={"temperature": 0})
    raw = response.get("response", "")
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model returned malformed JSON: {exc}") from exc
    parsed["_metadata"] = {"model": model, "course_id": course["course_id"], "elapsed_seconds": time.perf_counter() - started}
    return {"raw_response": raw, "parsed": parsed}


def save_extraction(result: dict[str, Any], output_dir: Path, course_id: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{course_id}.raw.json").write_text(json.dumps(result["raw_response"], ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / f"{course_id}.parsed.json").write_text(json.dumps(result["parsed"], ensure_ascii=False, indent=2), encoding="utf-8")
