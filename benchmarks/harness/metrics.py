"""Latency / throughput statistics."""

import math
from dataclasses import dataclass


@dataclass
class LatencyStats:
    samples: int
    min_ns: float
    max_ns: float
    mean_ns: float
    stddev_ns: float
    p50_ns: float
    p90_ns: float
    p99_ns: float

    def to_dict(self) -> dict:
        return {
            "samples": self.samples,
            "min_ns": self.min_ns,
            "max_ns": self.max_ns,
            "mean_ns": self.mean_ns,
            "stddev_ns": self.stddev_ns,
            "p50_ns": self.p50_ns,
            "p90_ns": self.p90_ns,
            "p99_ns": self.p99_ns,
        }


def _percentile(sorted_values: list[float], pct: float) -> float:
    if not sorted_values:
        return float("nan")
    if len(sorted_values) == 1:
        return sorted_values[0]
    rank = (pct / 100.0) * (len(sorted_values) - 1)
    lo = int(math.floor(rank))
    hi = int(math.ceil(rank))
    if lo == hi:
        return sorted_values[lo]
    frac = rank - lo
    return sorted_values[lo] * (1 - frac) + sorted_values[hi] * frac


def summarize_latencies(latencies_ns: list[float]) -> LatencyStats:
    if not latencies_ns:
        return LatencyStats(0, 0, 0, 0, 0, 0, 0, 0)
    s = sorted(latencies_ns)
    n = len(s)
    mean = sum(s) / n
    var = sum((x - mean) ** 2 for x in s) / n
    return LatencyStats(
        samples=n,
        min_ns=s[0],
        max_ns=s[-1],
        mean_ns=mean,
        stddev_ns=math.sqrt(var),
        p50_ns=_percentile(s, 50),
        p90_ns=_percentile(s, 90),
        p99_ns=_percentile(s, 99),
    )
