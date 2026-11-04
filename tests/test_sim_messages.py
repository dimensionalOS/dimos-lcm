import json
from pathlib import Path
import unittest

from dimos_lcm.control_msgs import JointCommand
from dimos_lcm.sim_msgs import BodyPoses, BodyMotion

FIXTURES = json.loads(Path(__file__).with_name("sim_wire_fixtures.json").read_text())


class SimMessagesTest(unittest.TestCase):
    def test_named_pose_and_acquisition_identity(self):
        payload = bytes.fromhex(FIXTURES["body_poses"])
        message = BodyPoses.lcm_decode(payload)
        self.assertEqual(message.header.epoch, 2**60+3)
        self.assertEqual(message.header.time_ns, 2**60+7)
        self.assertEqual(message.bodies[0].body_id, "g1/hand")
        self.assertEqual(message.bodies[0].pose_world.position.x, 1)
        self.assertEqual(message.lcm_encode(), payload)

    def test_joint_command_has_explicit_control_semantics(self):
        payload = bytes.fromhex(FIXTURES["joint_command"])
        message = JointCommand.lcm_decode(payload)
        t = message.targets[0]
        self.assertEqual((t.joint_id,t.position,t.velocity,t.kp,t.kd,t.feedforward),
                         ("g1/elbow",.25,-.5,40,1.5,2))
        self.assertEqual(message.valid_until_ns-message.apply_at_ns,20_000_000)
        self.assertEqual(message.lcm_encode(), payload)

    def test_motion_keeps_kinematics_and_gravity_distinct(self):
        payload = bytes.fromhex(FIXTURES["body_motion"])
        message = BodyMotion.lcm_decode(payload)
        self.assertEqual(list(message.linear_acceleration_world),[0,0,-9.81])
        self.assertEqual(list(message.gravity_world),[0,0,-9.81])
        self.assertEqual(message.lcm_encode(),payload)

    def test_wrong_type_fingerprint_is_rejected(self):
        with self.assertRaises(ValueError):
            BodyMotion.lcm_decode(bytes.fromhex(FIXTURES["body_poses"]))
