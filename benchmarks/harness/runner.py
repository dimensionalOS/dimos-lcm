"""Drives an echo binary through the benchmark profiles.

Architecture:
    1. Spawn the echo binary as a subprocess. It takes:
           <binary> <lcm_type> <input_channel> <output_channel>
       and is expected to subscribe to input_channel, decode each
       message, re-encode it, and publish on output_channel.
    2. Wait for the binary to print the literal sentinel "READY\n" on
       its stdout. This avoids a race between the harness publishing
       and the binary's subscription being installed.
    3. Run the latency, throughput, and (optionally) drop_stress
       profiles in sequence on the same subprocess.
    4. SIGTERM the subprocess and reap it.
"""

import os
import signal
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import dataclass

import lcm

from .generator import build_fixture
from .menu import MenuEntry
from .metrics import LatencyStats, summarize_latencies
from .profiles import DROP_STRESS, LATENCY, THROUGHPUT


@dataclass
class ProfileResult:
    profile: str
    samples: int
    sent: int
    received: int
    drops: int
    duration_s: float
    latency: LatencyStats
    msgs_per_sec: float
    bytes_per_sec: float


@dataclass
class TypeRunResult:
    type_name: str
    encoded_bytes: int
    profiles: list[ProfileResult]


class EchoProcess:
    """A spawned echo binary plus its bookkeeping."""

    def __init__(
        self,
        argv: list[str],
        type_name: str,
        in_channel: str,
        out_channel: str,
        env: dict | None = None,
    ) -> None:
        self.argv = argv + [type_name, in_channel, out_channel]
        self.proc: subprocess.Popen | None = None
        self._stderr_thread: threading.Thread | None = None
        self._env = env

    def __enter__(self) -> "EchoProcess":
        self.proc = subprocess.Popen(
            self.argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=self._env,
        )
        # Drain stderr in the background so the child never blocks on
        # a full pipe — we forward it to our own stderr with a tag.
        assert self.proc.stderr is not None
        tag = f"[echo {self.argv[-3]}]"
        stderr = self.proc.stderr

        def _pump() -> None:
            for line in stderr:
                sys.stderr.write(f"{tag} {line}")

        self._stderr_thread = threading.Thread(target=_pump, daemon=True)
        self._stderr_thread.start()
        self._wait_ready()
        return self

    def _wait_ready(self) -> None:
        assert self.proc is not None
        assert self.proc.stdout is not None
        deadline = time.monotonic() + 15.0
        while time.monotonic() < deadline:
            line = self.proc.stdout.readline()
            if not line:
                rc = self.proc.poll()
                raise RuntimeError(
                    f"echo binary exited before reporting READY (rc={rc})"
                )
            if line.strip() == "READY":
                return
        raise TimeoutError("echo binary did not print READY within 15s")

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.proc is None:
            return
        if self.proc.poll() is None:
            self.proc.send_signal(signal.SIGTERM)
            try:
                self.proc.wait(timeout=5.0)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()
        if self._stderr_thread is not None:
            self._stderr_thread.join(timeout=1.0)


class _Receiver:
    """Holds the LCM handle and a deque of completion timestamps."""

    def __init__(self) -> None:
        # Use mcast addr that is unique-ish per process to dodge stale
        # state from other dev sessions on the same machine.
        self.lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=0")
        self.recv_count = 0
        self.recv_ts: list[float] = []

    def subscribe(self, channel: str) -> None:
        sub = self.lc.subscribe(channel, self._on_message)
        # Match the C++ echo's queue capacity so neither side becomes
        # the silent bottleneck during throughput bursts.
        try:
            sub.set_queue_capacity(4096)
        except AttributeError:
            pass

    def _on_message(self, channel: str, data: bytes) -> None:  # noqa: ARG002
        self.recv_ts.append(time.monotonic_ns())
        self.recv_count += 1


def _run_latency(
    receiver: _Receiver,
    in_channel: str,
    payload: bytes,
    samples: int,
    warmup: int,
) -> ProfileResult:
    # Warmup: not measured.
    for _ in range(warmup):
        receiver.lc.publish(in_channel, payload)
        deadline = time.monotonic() + 1.0
        before = receiver.recv_count
        while receiver.recv_count == before and time.monotonic() < deadline:
            receiver.lc.handle_timeout(50)

    receiver.recv_ts.clear()
    receiver.recv_count = 0
    send_ts: list[int] = []
    sent = 0
    t0 = time.monotonic()
    for _ in range(samples):
        send_ts.append(time.monotonic_ns())
        receiver.lc.publish(in_channel, payload)
        sent += 1
        # 1 in flight: wait for echo before sending next.
        before = receiver.recv_count
        deadline_ns = time.monotonic_ns() + int(2e9)
        while receiver.recv_count == before and time.monotonic_ns() < deadline_ns:
            receiver.lc.handle_timeout(50)
    duration = time.monotonic() - t0
    received = min(receiver.recv_count, len(receiver.recv_ts))
    pairs = list(zip(send_ts[:received], receiver.recv_ts[:received]))
    latencies = [float(rcv - snd) for snd, rcv in pairs]
    return ProfileResult(
        profile="latency",
        samples=len(latencies),
        sent=sent,
        received=received,
        drops=sent - received,
        duration_s=duration,
        latency=summarize_latencies(latencies),
        msgs_per_sec=received / duration if duration > 0 else 0.0,
        bytes_per_sec=(received * len(payload)) / duration if duration > 0 else 0.0,
    )


def _run_throughput(
    receiver: _Receiver,
    in_channel: str,
    payload: bytes,
    duration_s: float,
    inflight: int,
    warmup: int,
) -> ProfileResult:
    for _ in range(warmup):
        receiver.lc.publish(in_channel, payload)
        receiver.lc.handle_timeout(20)

    receiver.recv_ts.clear()
    receiver.recv_count = 0
    sent = 0
    t0 = time.monotonic()
    deadline = t0 + duration_s
    while time.monotonic() < deadline:
        for _ in range(inflight):
            receiver.lc.publish(in_channel, payload)
            sent += 1
        # Drain whatever has come back so far without blocking long.
        for _ in range(inflight * 2):
            if receiver.lc.handle_timeout(0) <= 0:
                break
    # Allow stragglers to come back.
    drain_deadline = time.monotonic() + 1.0
    while receiver.recv_count < sent and time.monotonic() < drain_deadline:
        receiver.lc.handle_timeout(50)
    duration = time.monotonic() - t0
    received = receiver.recv_count
    return ProfileResult(
        profile="throughput",
        samples=received,
        sent=sent,
        received=received,
        drops=max(0, sent - received),
        duration_s=duration,
        latency=summarize_latencies([]),
        msgs_per_sec=received / duration if duration > 0 else 0.0,
        bytes_per_sec=(received * len(payload)) / duration if duration > 0 else 0.0,
    )


def _run_drop_stress(
    receiver: _Receiver,
    in_channel: str,
    payload: bytes,
    duration_s: float,
) -> ProfileResult:
    receiver.recv_ts.clear()
    receiver.recv_count = 0
    sent = 0
    t0 = time.monotonic()
    deadline = t0 + duration_s
    # Pure flood with no draining — measure how many survive.
    while time.monotonic() < deadline:
        receiver.lc.publish(in_channel, payload)
        sent += 1
    # Drain after the flood ends.
    drain_deadline = time.monotonic() + 2.0
    while time.monotonic() < drain_deadline:
        if receiver.lc.handle_timeout(50) <= 0:
            break
    duration = time.monotonic() - t0
    received = receiver.recv_count
    return ProfileResult(
        profile="drop_stress",
        samples=received,
        sent=sent,
        received=received,
        drops=max(0, sent - received),
        duration_s=duration,
        latency=summarize_latencies([]),
        msgs_per_sec=received / duration if duration > 0 else 0.0,
        bytes_per_sec=(received * len(payload)) / duration if duration > 0 else 0.0,
    )


def run_type(
    binary_argv: list[str],
    entry: MenuEntry,
    profiles: tuple = (LATENCY, THROUGHPUT, DROP_STRESS),
    env: dict | None = None,
) -> TypeRunResult:
    fixture = build_fixture(entry.fixture_kind, entry.fixture_arg)
    payload = fixture.lcm_encode()

    run_id = uuid.uuid4().hex[:8]
    in_channel = f"bench_{run_id}_in"
    out_channel = f"bench_{run_id}_out"

    receiver = _Receiver()
    receiver.subscribe(out_channel)
    # Drain any pending traffic on the brand-new socket before measuring.
    while receiver.lc.handle_timeout(0) > 0:
        pass
    receiver.recv_ts.clear()
    receiver.recv_count = 0

    profile_results: list[ProfileResult] = []
    with EchoProcess(binary_argv, entry.type_name, in_channel, out_channel, env=env):
        for profile in profiles:
            if profile is LATENCY:
                profile_results.append(
                    _run_latency(
                        receiver,
                        in_channel,
                        payload,
                        samples=LATENCY.samples_for(entry.category),
                        warmup=LATENCY.warmup,
                    )
                )
            elif profile is THROUGHPUT:
                profile_results.append(
                    _run_throughput(
                        receiver,
                        in_channel,
                        payload,
                        duration_s=THROUGHPUT.duration_s,
                        inflight=THROUGHPUT.inflight_for(entry.category),
                        warmup=THROUGHPUT.warmup,
                    )
                )
            elif profile is DROP_STRESS:
                if entry.category not in DROP_STRESS.enabled_categories:
                    continue
                profile_results.append(
                    _run_drop_stress(
                        receiver,
                        in_channel,
                        payload,
                        duration_s=DROP_STRESS.duration_s,
                    )
                )

    return TypeRunResult(
        type_name=entry.type_name,
        encoded_bytes=len(payload),
        profiles=profile_results,
    )


def echo_python_argv() -> list[str]:
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    echo = os.path.join(repo_root, "benchmarks", "echoes", "python", "echo.py")
    return [sys.executable, echo]


def echo_cpp_argv() -> list[str]:
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    binary = os.path.join(repo_root, "benchmarks", "echoes", "cpp", "build", "echo")
    return [binary]
