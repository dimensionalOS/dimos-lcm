use dimos_lcm::{Lcm, ReceivedMessage};
use lcm_msgs::geometry_msgs::{Twist, Vector3};
use std::time::{Duration, Instant};

fn recv_with_timeout(lcm: &Lcm, channel: &str, timeout_ms: u64) -> Option<ReceivedMessage> {
    let deadline = Instant::now() + Duration::from_millis(timeout_ms);
    while Instant::now() < deadline {
        if let Ok(Some(msg)) = lcm.try_recv() {
            if msg.channel == channel {
                return Some(msg);
            }
        }
        std::thread::sleep(Duration::from_millis(10));
    }
    None
}

#[test]
fn test_try_recv_returns_none_when_empty() {
    let lcm = Lcm::new().unwrap();
    // Drain any stale multicast messages
    while let Ok(Some(_)) = lcm.try_recv() {}
    assert!(lcm.try_recv().unwrap().is_none());
}

#[test]
fn test_publish_and_receive_vector3() {
    let sender = Lcm::new().unwrap();
    let receiver = Lcm::new().unwrap();

    // Drain stale messages
    while let Ok(Some(_)) = receiver.try_recv() {}

    let v = Vector3 {
        x: 1.5,
        y: 2.5,
        z: 3.5,
    };
    let encoded = v.encode();
    sender.publish("VECTOR3_TEST", &encoded).unwrap();

    let msg = recv_with_timeout(&receiver, "VECTOR3_TEST", 500)
        .expect("timed out waiting for VECTOR3_TEST");
    assert_eq!(msg.channel, "VECTOR3_TEST");

    let decoded = Vector3::decode(&msg.data).unwrap();
    assert_eq!(decoded.x.to_bits(), 1.5f64.to_bits());
    assert_eq!(decoded.y.to_bits(), 2.5f64.to_bits());
    assert_eq!(decoded.z.to_bits(), 3.5f64.to_bits());
}

#[test]
fn test_publish_and_receive_twist() {
    let sender = Lcm::new().unwrap();
    let receiver = Lcm::new().unwrap();

    while let Ok(Some(_)) = receiver.try_recv() {}

    let t = Twist {
        linear: Vector3 {
            x: 1.0,
            y: 0.0,
            z: 0.0,
        },
        angular: Vector3 {
            x: 0.0,
            y: 0.0,
            z: 0.5,
        },
    };
    let encoded = t.encode();
    sender.publish("/cmd_vel", &encoded).unwrap();

    let msg =
        recv_with_timeout(&receiver, "/cmd_vel", 500).expect("timed out waiting for /cmd_vel");
    assert_eq!(msg.channel, "/cmd_vel");

    let decoded = Twist::decode(&msg.data).unwrap();
    assert_eq!(decoded.linear.x.to_bits(), 1.0f64.to_bits());
    assert_eq!(decoded.linear.y.to_bits(), 0.0f64.to_bits());
    assert_eq!(decoded.linear.z.to_bits(), 0.0f64.to_bits());
    assert_eq!(decoded.angular.x.to_bits(), 0.0f64.to_bits());
    assert_eq!(decoded.angular.y.to_bits(), 0.0f64.to_bits());
    assert_eq!(decoded.angular.z.to_bits(), 0.5f64.to_bits());
}

#[test]
fn test_publish_raw_bytes_and_receive() {
    let sender = Lcm::new().unwrap();
    let receiver = Lcm::new().unwrap();

    while let Ok(Some(_)) = receiver.try_recv() {}

    let raw = vec![0xDE, 0xAD, 0xBE, 0xEF, 0x01, 0x02, 0x03];
    sender.publish("RAW_TEST", &raw).unwrap();

    let msg =
        recv_with_timeout(&receiver, "RAW_TEST", 500).expect("timed out waiting for RAW_TEST");
    assert_eq!(msg.channel, "RAW_TEST");
    assert_eq!(msg.data, raw);
}

#[test]
fn test_publish_and_receive_large_message() {
    let sender = Lcm::new().unwrap();
    let receiver = Lcm::new().unwrap();

    while let Ok(Some(_)) = receiver.try_recv() {}

    let large_message = vec![0x2Au8; 1024 * 1024];
    sender.publish("LARGE_TEST", &large_message).unwrap();

    let msg = recv_with_timeout(&receiver, "LARGE_TEST", 500).expect("timed out waiting for LARGE_TEST");
    assert_eq!(msg.channel, "LARGE_TEST");
    assert_eq!(msg.data, large_message);
}