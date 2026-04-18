#!/usr/bin/env python3
"""Python echo binary for the dimos-lcm benchmark harness.

CLI:  echo.py <lcm_type> <input_channel> <output_channel>

Subscribes to input_channel, decodes each message as the requested
LCM type, re-encodes it, and republishes on output_channel. Prints
the literal "READY\\n" to stdout once the subscription is in place
so the harness knows it can start measuring.
"""

import os
import signal
import sys

# Make the harness's loader available — it knows how to import
# generated message classes from the dimos-lcm tree.
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO_ROOT, "benchmarks"))
sys.path.insert(0, os.path.join(_REPO_ROOT, "generated", "python_lcm_msgs"))

import lcm  # noqa: E402

from harness.loader import load_class  # noqa: E402


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "usage: echo.py <lcm_type> <input_channel> <output_channel>",
            file=sys.stderr,
        )
        return 64

    type_name, in_channel, out_channel = sys.argv[1:]
    try:
        msg_cls = load_class(type_name)
    except Exception as exc:
        print(f"echo.py: cannot load {type_name!r}: {exc}", file=sys.stderr)
        return 2

    lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=0")

    def on_message(_channel: str, data: bytes) -> None:
        msg = msg_cls.lcm_decode(data)
        lc.publish(out_channel, msg.lcm_encode())

    sub = lc.subscribe(in_channel, on_message)
    try:
        sub.set_queue_capacity(4096)
    except AttributeError:
        pass

    # Drain any stragglers from a previous run on the same channel
    # before signaling readiness.
    while lc.handle_timeout(0) > 0:
        pass

    print("READY", flush=True)

    stop = {"requested": False}

    def _on_signal(_signo, _frame) -> None:
        stop["requested"] = True

    signal.signal(signal.SIGTERM, _on_signal)
    signal.signal(signal.SIGINT, _on_signal)
    # Tell libc to NOT automatically restart syscalls when our handlers
    # fire — we want handle_timeout to return so we can check the flag.
    # The cost is that the lcm call surfaces EINTR as OSError, which we
    # then treat as "loop again" rather than fatal.
    try:
        signal.siginterrupt(signal.SIGTERM, True)
        signal.siginterrupt(signal.SIGINT, True)
    except (AttributeError, OSError):
        pass

    while not stop["requested"]:
        try:
            lc.handle_timeout(100)
        except OSError:
            # EINTR from our own signal — fall through to the loop
            # check. Any *other* OSError will raise on the next call.
            continue
    return 0


if __name__ == "__main__":
    sys.exit(main())
