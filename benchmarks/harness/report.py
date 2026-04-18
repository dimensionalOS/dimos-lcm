"""JSON output writer + console summary table."""

import datetime as dt
import json
import os
import platform
import socket
import sys

from .runner import TypeRunResult


def _now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _filename_stamp() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")


def _host_info() -> dict:
    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "system": platform.system(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python": sys.version.split()[0],
    }


def write_results(
    results_dir: str,
    binary_results: dict[str, list[TypeRunResult]],
    binary_meta: dict[str, dict],
) -> str:
    os.makedirs(results_dir, exist_ok=True)
    payload = {
        "run_id": _now_iso(),
        "host": _host_info(),
        "binaries": binary_meta,
        "results": [],
    }
    for binary, runs in binary_results.items():
        for run in runs:
            for prof in run.profiles:
                payload["results"].append(
                    {
                        "binary": binary,
                        "type": run.type_name,
                        "encoded_bytes": run.encoded_bytes,
                        "profile": prof.profile,
                        "duration_s": prof.duration_s,
                        "sent": prof.sent,
                        "received": prof.received,
                        "drops": prof.drops,
                        "msgs_per_sec": prof.msgs_per_sec,
                        "bytes_per_sec": prof.bytes_per_sec,
                        "latency": prof.latency.to_dict(),
                    }
                )
    out_path = os.path.join(results_dir, f"{_filename_stamp()}.json")
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    return out_path


def print_summary(binary_results: dict[str, list[TypeRunResult]]) -> None:
    rows: list[tuple[str, str, str, str, str, str, str]] = []
    rows.append(
        ("binary", "type", "profile", "bytes", "p50_us", "msgs/s", "drops")
    )
    for binary, runs in binary_results.items():
        for run in runs:
            for prof in run.profiles:
                p50 = prof.latency.p50_ns / 1000.0 if prof.latency.samples else 0.0
                rows.append(
                    (
                        binary,
                        run.type_name,
                        prof.profile,
                        f"{run.encoded_bytes}",
                        f"{p50:,.1f}" if p50 else "-",
                        f"{prof.msgs_per_sec:,.0f}",
                        f"{prof.drops}",
                    )
                )
    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    for i, row in enumerate(rows):
        line = "  ".join(cell.ljust(widths[j]) for j, cell in enumerate(row))
        print(line)
        if i == 0:
            print("  ".join("-" * w for w in widths))
