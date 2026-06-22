use dimos_lcm::Lcm;
use tokio::time::Duration;

const TIMEOUT: Duration = Duration::from_secs(2);

async fn recv_channel(receiver: &mut Lcm, channel: &str) -> Vec<u8> {
    loop {
        let msg = receiver.recv().await.unwrap();
        if msg.channel == channel {
            return msg.data;
        }
    }
}

#[tokio::test]
async fn test_small_message_round_trip() {
    let sender = Lcm::new().await.unwrap();
    let mut receiver = Lcm::new().await.unwrap();
    let payload = b"hello lcm transport".to_vec();
    let expected = payload.clone();

    tokio::spawn(async move {
        tokio::time::sleep(Duration::from_millis(10)).await;
        sender.publish("SMALL_TRIP", &payload).await.unwrap();
    });

    tokio::time::timeout(TIMEOUT, async {
        assert_eq!(recv_channel(&mut receiver, "SMALL_TRIP").await, expected);
    })
    .await
    .expect("timed out waiting for SMALL_TRIP");
}

#[tokio::test]
async fn test_binary_payload_round_trip() {
    let sender = Lcm::new().await.unwrap();
    let mut receiver = Lcm::new().await.unwrap();
    let payload: Vec<u8> = (0u8..=255).collect();
    let expected = payload.clone();

    tokio::spawn(async move {
        tokio::time::sleep(Duration::from_millis(10)).await;
        sender.publish("BIN_TRIP", &payload).await.unwrap();
    });

    tokio::time::timeout(TIMEOUT, async {
        assert_eq!(recv_channel(&mut receiver, "BIN_TRIP").await, expected);
    })
    .await
    .expect("timed out waiting for BIN_TRIP");
}

#[tokio::test]
async fn test_publish_raw_bytes_and_receive() {
    let sender = Lcm::new().await.unwrap();
    let mut receiver = Lcm::new().await.unwrap();

    let raw = vec![0xDE, 0xAD, 0xBE, 0xEF, 0x01, 0x02, 0x03];
    let expected = raw.clone();

    tokio::spawn(async move {
        tokio::time::sleep(Duration::from_millis(10)).await;
        sender.publish("RAW_TEST", &raw).await.unwrap();
    });

    tokio::time::timeout(TIMEOUT, async {
        assert_eq!(recv_channel(&mut receiver, "RAW_TEST").await, expected);
    })
    .await
    .expect("timed out waiting for RAW_TEST");
}

#[tokio::test]
async fn test_empty_payload_round_trip() {
    let sender = Lcm::new().await.unwrap();
    let mut receiver = Lcm::new().await.unwrap();

    tokio::spawn(async move {
        tokio::time::sleep(Duration::from_millis(10)).await;
        sender.publish("EMPTY_TEST", &[]).await.unwrap();
    });

    tokio::time::timeout(TIMEOUT, async {
        assert!(recv_channel(&mut receiver, "EMPTY_TEST").await.is_empty());
    })
    .await
    .expect("timed out waiting for EMPTY_TEST");
}

#[tokio::test]
async fn test_multiple_sequential_messages() {
    let sender = Lcm::new().await.unwrap();
    let mut receiver = Lcm::new().await.unwrap();

    tokio::spawn(async move {
        tokio::time::sleep(Duration::from_millis(10)).await;
        for i in 0u8..5 {
            sender.publish("MULTI_TEST", &[i]).await.unwrap();
        }
    });

    tokio::time::timeout(TIMEOUT, async {
        let mut received = Vec::new();
        while received.len() < 5 {
            let msg = receiver.recv().await.unwrap();
            if msg.channel == "MULTI_TEST" {
                received.push(msg.data[0]);
            }
        }
        assert_eq!(received, vec![0, 1, 2, 3, 4]);
    })
    .await
    .expect("timed out waiting for MULTI_TEST");
}

#[tokio::test]
async fn test_publish_and_receive_large_message() {
    let sender = Lcm::new().await.unwrap();
    let mut receiver = Lcm::new().await.unwrap();

    let large_message = vec![0x2Au8; 1024 * 1024];
    let expected = large_message.clone();

    let handle = tokio::spawn(async move {
        tokio::time::sleep(Duration::from_millis(10)).await;
        sender.publish("LARGE_TEST", &large_message).await.unwrap();
    });

    tokio::time::timeout(TIMEOUT, async {
        assert_eq!(recv_channel(&mut receiver, "LARGE_TEST").await, expected);
    })
    .await
    .expect("timed out waiting for LARGE_TEST");

    handle.await.unwrap();
}
