"""Lightweight process resource measurements; GPU measurement is not inferred."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceMeasurement:
    elapsed_seconds: float
    peak_rss_bytes: int | None
    cpu_percent: float | None = None
    gpu_percent: float | None = None


def measure_elapsed(start: float, peak_rss_bytes: int | None = None) -> ResourceMeasurement:
    return ResourceMeasurement(time.perf_counter() - start, peak_rss_bytes)


def current_rss_bytes() -> int | None:
    try:
        import psutil
    except ImportError:
        return None
    return int(psutil.Process(os.getpid()).memory_info().rss)
