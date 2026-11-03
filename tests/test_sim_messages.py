import json
from pathlib import Path
import unittest

from dimos_lcm.geometry_msgs import Pose
from dimos_lcm.sim_msgs import Actions, JointCommand, Observations


class SimMessagesTest(unittest.TestCase):
    def test_shared_pose_fixture(self):
        fixtures = json.loads(
            Path(__file__).with_name("sim_wire_fixtures.json").read_text()
        )
        payload = bytes.fromhex(fixtures["observations"])
        message = Observations.lcm_decode(payload)
        self.assertEqual(message.epoch, 2**60 + 3)
        self.assertTrue(message.complete)
        self.assertEqual(message.observations[0].entity_id, "g1/hand")
        pose = Pose.lcm_decode(message.observations[0].data)
        self.assertEqual((pose.position.x, pose.position.y, pose.position.z), (1, 2, 3))
        self.assertEqual(pose.orientation.w, 1)
        self.assertEqual(message.lcm_encode(), payload)

    def test_shared_action_fixture_preserves_pd_and_feedforward(self):
        fixtures = json.loads(
            Path(__file__).with_name("sim_wire_fixtures.json").read_text()
        )
        payload = bytes.fromhex(fixtures["actions"])
        message = Actions.lcm_decode(payload)
        command = JointCommand.lcm_decode(message.actions[0].data)
        self.assertEqual(command.names, ["g1/elbow"])
        self.assertEqual(
            [
                list(getattr(command, k))
                for k in ("position", "velocity", "kp", "kd", "effort")
            ],
            [[0.25], [-0.5], [40.0], [1.5], [2.0]],
        )
        self.assertEqual(message.lcm_encode(), payload)

    def test_wrong_fingerprint_is_rejected(self):
        fixtures = json.loads(
            Path(__file__).with_name("sim_wire_fixtures.json").read_text()
        )
        payload = bytes.fromhex(fixtures["observations"])
        with self.assertRaises(ValueError):
            Observations.lcm_decode(bytes(8) + payload[8:])
