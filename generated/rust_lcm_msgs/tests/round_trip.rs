//! Round-trip encode/decode tests for generated LCM types.

use lcm_msgs::geometry_msgs::{Point, Vector3, Pose, Quaternion, PoseWithCovariance};
use lcm_msgs::std_msgs::Header;
use lcm_msgs::sensor_msgs::Imu;

#[test]
fn vector3_round_trip() {
    let original = Vector3 { x: 1.5, y: -2.0, z: 3.14 };
    let encoded = original.encode();
    let decoded = Vector3::decode(&encoded).unwrap();
    assert_eq!(original, decoded);
}

#[test]
fn pose_round_trip() {
    let original = Pose {
        position: Point { x: 1.0, y: 2.0, z: 3.0 },
        orientation: Quaternion { x: 0.0, y: 0.0, z: 0.0, w: 1.0 },
    };
    let encoded = original.encode();
    let decoded = Pose::decode(&encoded).unwrap();
    assert_eq!(original, decoded);
}

#[test]
fn header_with_string_round_trip() {
    let original = Header {
        seq: 42,
        stamp: lcm_msgs::std_msgs::Time { sec: 1234, nsec: 5678 },
        frame_id: "base_link".to_string(),
    };
    let encoded = original.encode();
    let decoded = Header::decode(&encoded).unwrap();
    assert_eq!(original, decoded);
}

#[test]
fn imu_with_fixed_arrays_round_trip() {
    let mut original = Imu::default();
    original.linear_acceleration = Vector3 { x: 0.0, y: 0.0, z: 9.81 };
    original.orientation = Quaternion { x: 0.0, y: 0.0, z: 0.0, w: 1.0 };
    // Set some covariance values
    original.orientation_covariance[0] = 0.01;
    original.orientation_covariance[4] = 0.01;
    original.orientation_covariance[8] = 0.01;
    let encoded = original.encode();
    let decoded = Imu::decode(&encoded).unwrap();
    assert_eq!(original, decoded);
}

#[test]
fn pose_with_covariance_manual_default_round_trip() {
    let mut original = PoseWithCovariance::default();
    original.pose = Pose {
        position: Point { x: 10.0, y: 20.0, z: 30.0 },
        orientation: Quaternion { x: 0.0, y: 0.0, z: 0.707, w: 0.707 },
    };
    original.covariance[0] = 1.0;
    original.covariance[35] = 1.0;
    let encoded = original.encode();
    let decoded = PoseWithCovariance::decode(&encoded).unwrap();
    assert_eq!(original, decoded);
}

#[test]
fn default_values_round_trip() {
    // Ensure default-constructed types survive round-trip
    let original = Vector3::default();
    let decoded = Vector3::decode(&original.encode()).unwrap();
    assert_eq!(original, decoded);
}

#[test]
fn hash_mismatch_returns_error() {
    let encoded = Vector3 { x: 1.0, y: 2.0, z: 3.0 }.encode();
    // Try to decode as Pose (different hash) — should fail
    let result = Pose::decode(&encoded);
    assert!(result.is_err());
}
