"""Top-level CLI entry point for the dimos-lcm benchmark harness."""

import argparse
import os
import sys
import time

from .menu import MENU, by_name
from .runner import TypeRunResult, echo_cpp_argv, echo_python_argv, run_type
from .report import print_summary, write_results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="dimos-lcm echo benchmark harness")
    parser.add_argument(
        "--binary",
        action="append",
        default=None,
        help='Binary spec like "name:command [args...]" — repeat for several. '
        'Defaults to running both the python and cpp echoes shipped in this repo.',
    )
    parser.add_argument(
        "--type",
        action="append",
        default=None,
        help="Restrict to a subset of menu type names.",
    )
    parser.add_argument(
        "--results-dir",
        default=os.path.join(os.path.dirname(__file__), "..", "results"),
    )
    args = parser.parse_args(argv)

    binaries: dict[str, list[str]] = {}
    if args.binary:
        for spec in args.binary:
            name, _, cmd = spec.partition(":")
            if not cmd:
                parser.error(f"--binary expects 'name:command', got {spec!r}")
            binaries[name] = cmd.split()
    else:
        binaries["python"] = echo_python_argv()
        binaries["cpp"] = echo_cpp_argv()

    if args.type:
        menu_entries = [by_name(t) for t in args.type]
    else:
        menu_entries = list(MENU)

    # Skip binaries that don't exist on disk yet — common while iterating.
    available: dict[str, list[str]] = {}
    for name, argv_ in binaries.items():
        head = argv_[0]
        if head.endswith(".py") and not os.path.exists(head):
            print(f"[skip] {name}: {head} not found", file=sys.stderr)
            continue
        if not head.endswith(".py") and not os.path.exists(head):
            print(
                f"[skip] {name}: {head} not built (run benchmarks/echoes/cpp/build.sh)",
                file=sys.stderr,
            )
            continue
        available[name] = argv_

    if not available:
        print("no echo binaries available — nothing to do", file=sys.stderr)
        return 1

    results: dict[str, list[TypeRunResult]] = {n: [] for n in available}
    binary_meta: dict[str, dict] = {}
    for name, argv_ in available.items():
        binary_meta[name] = {"argv": argv_}
        print(f"\n=== {name} ===", file=sys.stderr)
        for entry in menu_entries:
            print(f"  -> {entry.type_name} ({entry.category})", file=sys.stderr)
            t0 = time.monotonic()
            try:
                results[name].append(run_type(argv_, entry))
            except Exception as exc:
                print(f"     FAILED: {exc!r}", file=sys.stderr)
                continue
            print(f"     done in {time.monotonic() - t0:.1f}s", file=sys.stderr)

    out_path = write_results(args.results_dir, results, binary_meta)
    print(f"\nwrote results to {out_path}\n", file=sys.stderr)
    print_summary(results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
