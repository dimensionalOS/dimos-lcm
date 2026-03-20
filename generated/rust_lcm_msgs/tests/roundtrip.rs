use lcm_msgs::geometry_msgs::{Point, Pose, PoseStamped, Quaternion, Twist, Vector3};
use lcm_msgs::std_msgs::{Header, Time};

#[test]
fn test_vector3_encode_decode_roundtrip() {
    let v = Vector3 {
        x: 1.5,
        y: 2.5,
        z: 3.5,
    };
    let encoded = v.encode();
    let decoded = Vector3::decode(&encoded).unwrap();
    assert_eq!(decoded.x.to_bits(), v.x.to_bits());
    assert_eq!(decoded.y.to_bits(), v.y.to_bits());
    assert_eq!(decoded.z.to_bits(), v.z.to_bits());
}

#[test]
fn test_twist_encode_decode_roundtrip() {
    let t = Twist {
        linear: Vector3 {
            x: 1.0,
            y: 2.0,
            z: 3.0,
        },
        angular: Vector3 {
            x: 0.1,
            y: 0.2,
            z: 0.3,
        },
    };
    let encoded = t.encode();
    let decoded = Twist::decode(&encoded).unwrap();
    assert_eq!(decoded.linear.x.to_bits(), t.linear.x.to_bits());
    assert_eq!(decoded.linear.y.to_bits(), t.linear.y.to_bits());
    assert_eq!(decoded.linear.z.to_bits(), t.linear.z.to_bits());
    assert_eq!(decoded.angular.x.to_bits(), t.angular.x.to_bits());
    assert_eq!(decoded.angular.y.to_bits(), t.angular.y.to_bits());
    assert_eq!(decoded.angular.z.to_bits(), t.angular.z.to_bits());
}

#[test]
fn test_pose_stamped_roundtrip() {
    let ps = PoseStamped {
        header: Header {
            seq: 42,
            stamp: Time { sec: 100, nsec: 500 },
            frame_id: "map".into(),
        },
        pose: Pose {
            position: Point {
                x: 1.0,
                y: 2.0,
                z: 3.0,
            },
            orientation: Quaternion {
                x: 0.0,
                y: 0.0,
                z: 0.0,
                w: 1.0,
            },
        },
    };
    let encoded = ps.encode();
    let decoded = PoseStamped::decode(&encoded).unwrap();
    assert_eq!(decoded.header.seq, 42);
    assert_eq!(decoded.header.stamp.sec, 100);
    assert_eq!(decoded.header.stamp.nsec, 500);
    assert_eq!(decoded.header.frame_id, "map");
    assert_eq!(decoded.pose.position.x.to_bits(), 1.0f64.to_bits());
    assert_eq!(decoded.pose.position.y.to_bits(), 2.0f64.to_bits());
    assert_eq!(decoded.pose.position.z.to_bits(), 3.0f64.to_bits());
    assert_eq!(decoded.pose.orientation.x.to_bits(), 0.0f64.to_bits());
    assert_eq!(decoded.pose.orientation.y.to_bits(), 0.0f64.to_bits());
    assert_eq!(decoded.pose.orientation.z.to_bits(), 0.0f64.to_bits());
    assert_eq!(decoded.pose.orientation.w.to_bits(), 1.0f64.to_bits());
}

#[test]
fn test_vector3_hash_consistent() {
    let v = Vector3 {
        x: 1.5,
        y: 2.5,
        z: 3.5,
    };
    let enc1 = v.encode();
    let enc2 = v.encode();
    assert_eq!(&enc1[..8], &enc2[..8]);
}

#[test]
fn test_decode_corrupted_hash_fails() {
    let v = Vector3 {
        x: 1.5,
        y: 2.5,
        z: 3.5,
    };
    let mut encoded = v.encode();
    encoded[0] ^= 0xFF; // flip first byte of fingerprint
    assert!(Vector3::decode(&encoded).is_err());
}

#[test]
fn test_vector3_known_binary_layout() {
    let v = Vector3 {
        x: 1.5,
        y: 2.5,
        z: 3.5,
    };
    let encoded = v.encode();

    // Total: 8-byte fingerprint + 3x8-byte f64 = 32 bytes
    assert_eq!(encoded.len(), 32);

    // Fingerprint: 0xAE7E5FBA5EECA11E in big-endian
    assert_eq!(&encoded[..8], &0xAE7E5FBA5EECA11Eu64.to_be_bytes());

    // x=1.5 as f64 BE = 0x3FF8000000000000
    assert_eq!(&encoded[8..16], &0x3FF8000000000000u64.to_be_bytes());

    // y=2.5 as f64 BE = 0x4004000000000000
    assert_eq!(&encoded[16..24], &0x4004000000000000u64.to_be_bytes());

    // z=3.5 as f64 BE = 0x400C000000000000
    assert_eq!(&encoded[24..32], &0x400C000000000000u64.to_be_bytes());
}

#[test]
fn test_twist_known_fingerprint() {
    let t = Twist {
        linear: Vector3 {
            x: 0.0,
            y: 0.0,
            z: 0.0,
        },
        angular: Vector3 {
            x: 0.0,
            y: 0.0,
            z: 0.0,
        },
    };
    let encoded = t.encode();
    // Twist fingerprint: 0x2E7C07D7CDF7E027 in big-endian
    assert_eq!(&encoded[..8], &0x2E7C07D7CDF7E027u64.to_be_bytes());
}
