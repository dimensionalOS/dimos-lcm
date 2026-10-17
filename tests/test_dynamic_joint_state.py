import importlib
import sys
from pathlib import Path
import unittest


sys.path.insert(
    0,
    str(Path(__file__).parents[1] / "generated" / "python_lcm_msgs"),
)

from lcm_msgs.control_msgs import DynamicJointState, InterfaceValue  # noqa: E402

ROS_MSG_DIR = (
    Path(__file__).parents[1] / "sources" / "ros_msgs" / "control_msgs" / "msg"
)


class DynamicJointStateTest(unittest.TestCase):
    def test_round_trip(self) -> None:
        interfaces = ["position", "velocity", "effort", "stiffness", "damping"]
        msg = DynamicJointState()
        msg.header.frame_id = "base"
        msg.header.stamp.sec = 12
        msg.header.stamp.nsec = 345
        msg.joint_names = ["FR_hip_joint", "FR_thigh_joint"]
        msg.joint_names_length = 2
        for q in (0.1, -0.8):
            iv = InterfaceValue()
            iv.interface_names = list(interfaces)
            iv.interface_names_length = len(interfaces)
            iv.values = [q, 0.0, 1.5, 20.0, 0.5]
            iv.values_length = len(iv.values)
            msg.interface_values.append(iv)
        msg.interface_values_length = 2

        out = DynamicJointState.lcm_decode(msg.lcm_encode())

        self.assertEqual(out.header.frame_id, "base")
        self.assertEqual((out.header.stamp.sec, out.header.stamp.nsec), (12, 345))
        self.assertEqual(out.joint_names, msg.joint_names)
        self.assertEqual(len(out.interface_values), 2)
        for a, b in zip(out.interface_values, msg.interface_values):
            self.assertEqual(a.interface_names, interfaces)
            self.assertEqual(list(a.values), b.values)
        self.assertEqual(out.lcm_encode(), msg.lcm_encode())

    def test_every_upstream_type_encodes(self) -> None:
        names = sorted(p.stem for p in ROS_MSG_DIR.glob("*.msg"))
        self.assertGreater(len(names), 30)
        for name in names:
            with self.subTest(name):
                cls = getattr(
                    importlib.import_module(f"lcm_msgs.control_msgs.{name}"), name
                )
                self.assertEqual(
                    cls.lcm_decode(cls().lcm_encode()).lcm_encode(), cls().lcm_encode()
                )


if __name__ == "__main__":
    unittest.main()
