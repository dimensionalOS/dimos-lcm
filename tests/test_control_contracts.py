import sys
from pathlib import Path
import unittest


sys.path.insert(
    0,
    str(Path(__file__).parents[1] / "generated" / "python_lcm_msgs" / "lcm_msgs"),
)

from dimos_control_msgs import (  # noqa: E402
    CommandProfile,
    ConnectionControl,
    ConnectionDescription,
    ConnectionStatus,
    ControlValues,
    InterfaceDescription,
    ResourceDescription,
)
from dimos_core_msgs import ModuleReadiness  # noqa: E402


class ControlContractTest(unittest.TestCase):
    def assert_round_trip(self, message: object) -> object:
        encoded = message.lcm_encode()
        decoded = type(message).lcm_decode(encoded)
        self.assertEqual(decoded.lcm_encode(), encoded)
        return decoded

    def test_module_readiness_round_trip(self) -> None:
        message = ModuleReadiness(
            source="left",
            generation=7,
            sequence=11,
            source_ts=123.5,
            ready=True,
            reason="prêt ✓",
        )

        decoded = self.assert_round_trip(message)

        self.assertEqual(decoded.source, "left")
        self.assertEqual(decoded.reason, "prêt ✓")

    def test_control_values_round_trip(self) -> None:
        message = ControlValues(
            source="coordinator",
            source_ts=123.5,
            epoch=3,
            sequence=4,
            interface_names_length=2,
            values_length=2,
            interface_names=["left/j1/position", "left/j1/velocity"],
            values=[1.25, -2.5],
        )

        decoded = self.assert_round_trip(message)

        self.assertEqual(decoded.interface_names, message.interface_names)
        self.assertEqual(list(decoded.values), message.values)

    def test_description_and_nested_records_round_trip(self) -> None:
        resource = ResourceDescription(
            name="left/j1",
            resource_type=ResourceDescription.JOINT,
            group_name="left_arm",
        )
        interface = InterfaceDescription(
            name="left/j1/position",
            resource="left/j1",
            field="position",
            unit="rad",
            state=True,
            command=True,
            has_hard_min=True,
            hard_min=-2.0,
            has_hard_max=True,
            hard_max=2.0,
            has_soft_min=True,
            soft_min=-1.5,
            has_soft_max=True,
            soft_max=1.5,
            omission_policy=InterfaceDescription.HOLD_LAST,
        )
        profile = CommandProfile(
            name="position",
            required_fields_length=1,
            optional_fields_length=1,
            required_fields=["position"],
            optional_fields=["velocity"],
            uniform_across_resources=True,
        )
        for nested in (resource, interface, profile):
            self.assert_round_trip(nested)
        message = ConnectionDescription(
            source="left",
            description_epoch=1,
            resources_length=1,
            interfaces_length=1,
            command_profiles_length=1,
            resources=[resource],
            interfaces=[interface],
            command_profiles=[profile],
            expected_state_rate_hz=100.0,
            state_stale_timeout_s=0.1,
            command_watchdog_timeout_s=0.05,
            activation_policy=ConnectionDescription.DIRECT,
            armed_idle_policy=ConnectionDescription.APPLY_OMISSION,
            safe_stop_behavior="hold position",
            process_loss_classification=ConnectionDescription.NATIVE_WATCHDOG,
            process_loss_evidence="controller watchdog verified",
        )

        decoded = self.assert_round_trip(message)

        self.assertEqual(decoded.resources[0].name, "left/j1")
        self.assertEqual(decoded.interfaces[0].unit, "rad")
        self.assertEqual(decoded.command_profiles[0].required_fields, ["position"])

    def test_lifecycle_messages_round_trip(self) -> None:
        control = ConnectionControl(
            target_sources_length=2,
            target_sources=["left", "right"],
            operation_id=72,
            operation=ConnectionControl.PREPARE_ARM,
            proposed_control_epoch=9,
            reason="operator request",
        )
        status = ConnectionStatus(
            source="left",
            source_ts=123.5,
            lifecycle_state=ConnectionStatus.PREPARED,
            description_epoch=1,
            control_epoch=0,
            last_operation_id=72,
            last_operation=ConnectionControl.PREPARE_ARM,
            acknowledgement=ConnectionStatus.SUCCEEDED,
            fault="",
        )

        decoded_control = self.assert_round_trip(control)
        decoded_status = self.assert_round_trip(status)

        self.assertEqual(decoded_control.target_sources, ["left", "right"])
        self.assertEqual(decoded_status.last_operation_id, 72)

    def test_bad_fingerprint_is_rejected(self) -> None:
        encoded = bytearray(ControlValues().lcm_encode())
        encoded[0] ^= 0xFF

        with self.assertRaises(ValueError):
            ControlValues.lcm_decode(bytes(encoded))


if __name__ == "__main__":
    unittest.main()
