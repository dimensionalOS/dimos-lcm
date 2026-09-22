import struct
import sys
from pathlib import Path
import unittest


sys.path.insert(
    0,
    str(Path(__file__).parents[1] / "generated" / "python_lcm_msgs" / "lcm_msgs"),
)

from control_msgs import ControlValues  # noqa: E402


class ControlValuesTest(unittest.TestCase):
    def test_shared_wire_fixture(self) -> None:
        # Same golden bytes as the standalone Rust and TypeScript tests.
        payload = bytes.fromhex(
            "31b3ec9631ab499f00000003636300405ee000000000001000000000000003"
            "100000000000000400000001000000010000000e626173652f6c696e6561725f78003fe0000000000000"
        )

        decoded = ControlValues.lcm_decode(payload)

        self.assertEqual(decoded.source, "cc")
        self.assertEqual(decoded.source_ts, 123.5)
        self.assertEqual(decoded.epoch, 2**60 + 3)
        self.assertEqual(decoded.sequence, 2**60 + 4)
        self.assertEqual(decoded.interface_names, ["base/linear_x"])
        self.assertEqual(list(decoded.values), [0.5])
        self.assertEqual(decoded.lcm_encode(), payload)

    def test_control_families_round_trip(self) -> None:
        cases = {
            "arm": (["left/j1/position", "left/j1/velocity"], [1.25, -2.5]),
            "whole_body": (
                [
                    f"body/j1/{field}"
                    for field in ("position", "velocity", "effort", "kp", "kd")
                ],
                [0.25, -0.5, 2.0, 40.0, 1.5],
            ),
            "base": (
                ["base/linear_x", "base/linear_y", "base/angular_z"],
                [0.5, 0.0, -0.25],
            ),
            "pose": (
                [
                    f"arm/tool/{field}"
                    for field in ("x", "y", "z", "qx", "qy", "qz", "qw")
                ],
                [0.1, 0.2, 0.3, 0.0, 0.0, 0.0, 1.0],
            ),
            "empty": ([], []),
        }
        for family, (names, values) in cases.items():
            with self.subTest(family=family):
                message = ControlValues(
                    source="contrôle",
                    source_ts=123.5,
                    epoch=2**60 + 3,
                    sequence=2**60 + 4,
                    interface_names_length=len(names),
                    values_length=len(values),
                    interface_names=names,
                    values=values,
                )

                encoded = message.lcm_encode()
                decoded = ControlValues.lcm_decode(encoded)

                self.assertEqual(decoded.source, "contrôle")
                self.assertEqual(decoded.source_ts, 123.5)
                self.assertEqual(decoded.epoch, 2**60 + 3)
                self.assertEqual(decoded.sequence, 2**60 + 4)
                self.assertEqual(decoded.interface_names_length, len(names))
                self.assertEqual(decoded.values_length, len(values))
                self.assertEqual(decoded.interface_names, names)
                self.assertEqual(list(decoded.values), values)
                self.assertEqual(decoded.lcm_encode(), encoded)

    def test_bad_fingerprint_is_rejected(self) -> None:
        encoded = bytearray(ControlValues().lcm_encode())
        encoded[0] ^= 0xFF

        with self.assertRaises(ValueError):
            ControlValues.lcm_decode(bytes(encoded))

    def test_truncated_values_are_rejected(self) -> None:
        message = ControlValues(
            interface_names_length=1,
            values_length=1,
            interface_names=["base/linear_x"],
            values=[0.5],
        )

        with self.assertRaises(struct.error):
            ControlValues.lcm_decode(message.lcm_encode()[:-1])


if __name__ == "__main__":
    unittest.main()
