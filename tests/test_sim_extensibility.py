"""Compiled-reader compatibility: optional payloads do not change the core codec."""

from importlib.metadata import distribution
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from dimos_lcm.sim_msgs import CborObservation, WorldState

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = json.loads((ROOT / "tests/sim_wire_fixtures.json").read_text())

READER = r'''
#include <fstream>
#include <iterator>
#include <vector>
#include "sim_msgs/WorldState.hpp"
int main(int argc, char** argv) {
    if (argc != 2) return 2;
    // Freeze the core contract, including every recursively nested field.
    if (uint64_t(sim_msgs::WorldState::getHash()) != 0xbd2d6c56249d6c45ULL) return 3;
    std::ifstream file(argv[1], std::ios::binary);
    std::vector<char> bytes((std::istreambuf_iterator<char>(file)), {});
    sim_msgs::WorldState state;
    int n = state.decode(bytes.data(), 0, bytes.size());
    if (n < 0) return 10;
    // This reader understands no extension keys and has no CBOR codec.
    if (n != bytes.size() || state.bodies.size() != 1 ||
        state.bodies[0].body_id != "g1/hand" ||
        state.bodies[0].pose.position.x != 1.0 ||
        state.joint_truth.position != std::vector<double>{0.25}) return 4;
    return 0;
}
'''


class SimExtensibilityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resources = tempfile.TemporaryDirectory(prefix="sim2-wire-test-")
        cls.addClassCleanup(cls.resources.cleanup)
        cls.directory = Path(cls.resources.name)
        cls.include = str(distribution("lcm").locate_file("include"))
        cls.headers = ROOT / "generated/cpp_lcm_msgs"
        # Build once, before the new payload type exists.
        cls.reader = cls.compile("old_reader", READER)

    @classmethod
    def compile(cls, name, source, extra_headers=None):
        path = cls.directory / (name + ".cpp")
        path.write_text(source)
        executable = cls.directory / name
        includes = ["-I", str(extra_headers)] if extra_headers else []
        subprocess.run(["c++", "-std=c++17", *includes, "-I", cls.include,
                        "-I", str(cls.headers), str(path), "-o", str(executable)],
                       check=True, capture_output=True)
        return executable

    def read(self, name, payload):
        path = self.directory / (name + ".bin")
        path.write_bytes(payload)
        return subprocess.run([str(self.reader), str(path)], capture_output=True).returncode

    def test_new_payload_types_leave_core_and_unused_wire_size_unchanged(self):
        state = WorldState.lcm_decode(bytes.fromhex(FIXTURES["world_state"]))
        state.cbor_observations_length = 0
        state.cbor_observations = []
        baseline = state.lcm_encode()
        self.assertEqual(len(baseline), 343)
        self.assertEqual(self.read("baseline", baseline), 0)

        # A new, separately compiled message type; the old executable stays untouched.
        schema = self.directory / "TemperatureV1.lcm"
        schema.write_text("package compat; struct TemperatureV1 { double kelvin; }\n")
        generated = self.directory / "new_headers"
        generated.mkdir()
        subprocess.run([shutil.which("lcm-gen"), "--cpp", "--cpp-hpath", str(generated),
                        str(schema)], check=True, capture_output=True)
        writer = self.compile("new_payload", r'''
#include <fstream>
#include <vector>
#include "compat/TemperatureV1.hpp"
int main(int argc, char** argv) {
    if (argc != 2) return 2;
    compat::TemperatureV1 temperature{};
    temperature.kelvin = 305.0;
    std::vector<char> bytes(temperature.getEncodedSize());
    temperature.encode(bytes.data(), 0, bytes.size());
    std::ofstream(argv[1], std::ios::binary).write(bytes.data(), bytes.size());
}
''', generated)
        payload_file = self.directory / "temperature.bin"
        subprocess.run([str(writer), str(payload_file)], check=True)
        self.assertEqual(state.lcm_encode(), baseline)  # Defining a type adds zero bytes.
        inner = payload_file.read_bytes()
        self.assertEqual(len(inner), 16)  # fingerprint + float64
        # CBOR byte string of length 16; no new core field or per-type array count.
        value = b"\x50" + inner
        state.cbor_observations = [CborObservation(
            entity_id="g1/hand", key="example.temperature.lcm.v1",
            value_length=len(value), value=value)]
        state.cbor_observations_length = 1
        extended = state.lcm_encode()
        self.assertEqual(extended[:8], baseline[:8])
        self.assertEqual(len(extended), 407)
        self.assertEqual(self.read("new_extension", extended), 0)
        decoded = WorldState.lcm_decode(extended)
        self.assertEqual(bytes(decoded.cbor_observations[0].value), value)

        # Counterexample: adding even an empty typed array changes the outer hash.
        original = (ROOT / "lcm_types/sim_msgs_WorldState.lcm").read_text()
        before, end = original.rsplit("}", 1)
        changed = self.directory / "WorldState.lcm"
        changed.write_text(before + "int32_t temperatures_length;\n"
                           "compat.TemperatureV1 temperatures[temperatures_length];\n}" + end)
        subprocess.run([shutil.which("lcm-gen"), "--cpp", "--cpp-hpath", str(generated),
                        str(changed)], check=True, capture_output=True)
        changed_writer = self.compile("incompatible_writer", r'''
#include <fstream>
#include <vector>
#include "sim_msgs/WorldState.hpp"
int main(int argc, char** argv) {
    if (argc != 2) return 2;
    sim_msgs::WorldState state{};
    std::vector<char> bytes(state.getEncodedSize());
    state.encode(bytes.data(), 0, bytes.size());
    std::ofstream(argv[1], std::ios::binary).write(bytes.data(), bytes.size());
}
''', generated)
        incompatible = self.directory / "incompatible.bin"
        subprocess.run([str(changed_writer), str(incompatible)], check=True)
        self.assertEqual(self.read("new_typed_field", incompatible.read_bytes()), 10)
