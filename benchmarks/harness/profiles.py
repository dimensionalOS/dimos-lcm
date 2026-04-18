"""Per-(category, profile) tunables for the benchmark.

The harness sweeps every menu entry through every applicable profile.
A profile says: how many warmup messages, how many measurement
messages, and (for throughput) how long to flood for.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LatencyProfile:
    name: str = "latency"
    warmup: int = 200
    samples_by_category: tuple[tuple[str, int], ...] = (
        ("tiny", 20_000),
        ("small", 10_000),
        ("medium", 5_000),
        ("variable", 2_000),
        ("large", 500),
        ("large_fragmented", 200),
        ("huge_fragmented", 50),
    )

    def samples_for(self, category: str) -> int:
        for name, count in self.samples_by_category:
            if name == category:
                return count
        return 100


@dataclass(frozen=True)
class ThroughputProfile:
    name: str = "throughput"
    warmup: int = 200
    duration_s: float = 5.0
    inflight_by_category: tuple[tuple[str, int], ...] = (
        ("tiny", 256),
        ("small", 256),
        ("medium", 128),
        ("variable", 64),
        ("large", 32),
        ("large_fragmented", 8),
        ("huge_fragmented", 2),
    )

    def inflight_for(self, category: str) -> int:
        for name, count in self.inflight_by_category:
            if name == category:
                return count
        return 16


@dataclass(frozen=True)
class DropStressProfile:
    """Flood as fast as possible, see how many come back."""
    name: str = "drop_stress"
    warmup: int = 0
    duration_s: float = 2.0
    # Only run for these categories — small messages don't drop on
    # a localhost multicast loop in any meaningful way.
    enabled_categories: tuple[str, ...] = ("large_fragmented", "huge_fragmented")


LATENCY = LatencyProfile()
THROUGHPUT = ThroughputProfile()
DROP_STRESS = DropStressProfile()

ALL_PROFILES = (LATENCY, THROUGHPUT, DROP_STRESS)
