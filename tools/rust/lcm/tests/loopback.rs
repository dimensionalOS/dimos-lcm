use dimos_lcm::Lcm;
use lcm_msgs::geometry_msgs::{Twist, Vector3};
use tokio::time::Duration;

#[tokio::test]
async fn test_publish_and_receive_vector3() {
    let sender = Lcm::new().await.unwrap();
    let receiver = Lcm::new().await.unwrap();

    let encoded = Vector3 { x: 1.5, y: 2.5, z: 3.5 }.encode();

    tokio::spawn(async move {
        // give the subscriber time to start before publishing
        tokio::time::sleep(Duration::from_millis(10)).await;
        sender.publish("VECTOR3_TEST", &encoded).await.unwrap();
    });

    loop {
        let msg = receiver.recv().await.unwrap();
        if msg.channel == "VECTOR3_TEST" {
            let decoded = Vector3::decode(&msg.data).unwrap();
            assert_eq!(decoded.x.to_bits(), 1.5f64.to_bits());
            assert_eq!(decoded.y.to_bits(), 2.5f64.to_bits());
            assert_eq!(decoded.z.to_bits(), 3.5f64.to_bits());
            break;
        }
    }
}

#[tokio::test]
async fn test_publish_and_receive_twist() {
    let sender = Lcm::new().await.unwrap();
    let receiver = Lcm::new().await.unwrap();

    let encoded = Twist {
        linear: Vector3 { x: 1.0, y: 0.0, z: 0.0 },
        angular: Vector3 { x: 0.0, y: 0.0, z: 0.5 },
    }.encode();

    tokio::spawn(async move {
        tokio::time::sleep(Duration::from_millis(10)).await;
        sender.publish("/cmd_vel", &encoded).await.unwrap();
    });

    loop {
        let msg = receiver.recv().await.unwrap();
        if msg.channel == "/cmd_vel" {
            let decoded = Twist::decode(&msg.data).unwrap();
            assert_eq!(decoded.linear.x.to_bits(), 1.0f64.to_bits());
            assert_eq!(decoded.linear.y.to_bits(), 0.0f64.to_bits());
            assert_eq!(decoded.linear.z.to_bits(), 0.0f64.to_bits());
            assert_eq!(decoded.angular.x.to_bits(), 0.0f64.to_bits());
            assert_eq!(decoded.angular.y.to_bits(), 0.0f64.to_bits());
            assert_eq!(decoded.angular.z.to_bits(), 0.5f64.to_bits());
            break;
        }
    }
}

#[tokio::test]
async fn test_publish_raw_bytes_and_receive() {
    let sender = Lcm::new().await.unwrap();
    let receiver = Lcm::new().await.unwrap();

    let raw = vec![0xDE, 0xAD, 0xBE, 0xEF, 0x01, 0x02, 0x03];

    tokio::spawn(async move {
        tokio::time::sleep(Duration::from_millis(10)).await;
        sender.publish("RAW_TEST", &raw).await.unwrap();
    });

    loop {
        let msg = receiver.recv().await.unwrap();
        if msg.channel == "RAW_TEST" {
            assert_eq!(msg.data, vec![0xDE, 0xAD, 0xBE, 0xEF, 0x01, 0x02, 0x03]);
            break;
        }
    }
}

#[tokio::test]
async fn test_publish_and_receive_large_message() {
    let sender = Lcm::new().await.unwrap();
    let receiver = Lcm::new().await.unwrap();

    let large_message = vec![0x2Au8; 1024 * 1024];

    let handle = tokio::spawn(async move {
        tokio::time::sleep(Duration::from_millis(10)).await;
        sender.publish("LARGE_TEST", &large_message).await.unwrap();
    });

    tokio::time::timeout(Duration::from_secs(2), async {
        loop {
            let msg = receiver.recv().await.unwrap();
            if msg.channel == "LARGE_TEST" {
                assert_eq!(msg.data, vec![0x2Au8; 1024 * 1024]);
                break;
            }
        }
    })
    .await
    .expect("timed out waiting for LARGE_TEST");

    handle.await.unwrap();
}
