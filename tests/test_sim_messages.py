import json
from pathlib import Path
import unittest

from dimos_lcm.control_msgs import ActionCommand
from dimos_lcm.sim_msgs import WorldState

FIXTURES = json.loads(Path(__file__).with_name("sim_wire_fixtures.json").read_text())


class SimMessagesTest(unittest.TestCase):
    def test_complete_state_preserves_acquisition_and_physical_values(self):
        payload = bytes.fromhex(FIXTURES["world_state"])
        message = WorldState.lcm_decode(payload)
        self.assertEqual(message.header.epoch, 2**60 + 3)
        self.assertEqual(message.header.time_ns, 2**60 + 7)
        self.assertEqual(message.bodies[0].body_id, "g1/hand")
        self.assertEqual(message.bodies[0].pose.position.x, 1)
        body = message.bodies[0]
        a, v, w = body.acceleration.linear, body.twist.linear, body.twist.angular
        self.assertEqual([a.x, a.y, a.z], [0, 0, -9.81])
        alpha = body.acceleration.angular
        self.assertEqual([alpha.x, alpha.y, alpha.z], [4, 5, 6])
        self.assertEqual([v.x, v.y, v.z], [.1, .2, .3])
        self.assertEqual([w.x, w.y, w.z], [1, 2, 3])
        self.assertEqual(message.joint_truth.header.stamp.sec * 10**9 +
                         message.joint_truth.header.stamp.nsec, message.header.time_ns)
        self.assertEqual(list(message.joint_truth.position), [.25])
        self.assertEqual(list(message.joint_truth.effort), [])
        self.assertEqual(message.cbor_observations[0].key, "thermal")
        self.assertEqual(message.lcm_encode(), payload)

    def test_unknown_optional_observation_is_preserved_as_bytes(self):
        message = WorldState.lcm_decode(bytes.fromhex(FIXTURES["world_state"]))
        message.cbor_observations[0].key = "vendor.unrecognized.v2"
        restored = WorldState.lcm_decode(message.lcm_encode())
        self.assertEqual(restored.cbor_observations[0].key, "vendor.unrecognized.v2")
        self.assertEqual(bytes(restored.cbor_observations[0].value), bytes(message.cbor_observations[0].value))
        self.assertEqual(restored.bodies[0].body_id, "g1/hand")

    def test_action_command_preserves_joint_commands_cbor_and_timing(self):
        payload = bytes.fromhex(FIXTURES["action_command"])
        message = ActionCommand.lcm_decode(payload)
        self.assertEqual(message.header.time_ns, 2**60 + 7)
        self.assertEqual(message.cbor_commands[0].entity_id, "world")
        self.assertEqual(message.cbor_commands[0].key, "increment")
        self.assertEqual(bytes(message.cbor_commands[0].value), b"\x01")
        t = message.joint_commands[0]
        self.assertEqual((t.joint_id, t.position, t.velocity, t.kp, t.kd, t.feedforward),
                         ("g1/elbow", .25, -.5, 40, 1.5, 2))
        self.assertEqual(message.valid_until_ns - message.apply_at_ns, 20_000_000)
        self.assertEqual(message.lcm_encode(), payload)

    def test_wrong_type_fingerprint_is_rejected(self):
        with self.assertRaises(ValueError):
            WorldState.lcm_decode(bytes.fromhex(FIXTURES["action_command"]))
