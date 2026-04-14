// Simple LCM Subscriber Example
// Receives Vector3 messages with typed decoding

use dimos_lcm::Lcm;
use lcm_msgs::geometry_msgs::Vector3;
use std::time::Instant;

const CHANNEL: &str = "/vector#geometry_msgs.Vector3";

#[tokio::main]
async fn main() {
    let mut lcm = Lcm::new().await.expect("Failed to create LCM transport");

    println!("Listening for Vector3 on '/vector'...");
    println!("Press Ctrl+C to stop.\n");

    let mut last = Instant::now();

    loop {
        match lcm.recv().await {
            Ok(msg) if msg.channel == CHANNEL => {
                let interval = last.elapsed();
                last = Instant::now();
                match Vector3::decode(&msg.data) {
                    Ok(vec) => {
                        println!(
                            "Received: x={:.2} y={:.2} z={:.2} (interval {:.1}ms)",
                            vec.x, vec.y, vec.z, interval.as_secs_f64() * 1000.0
                        );
                    }
                    Err(e) => eprintln!("decode error: {e}"),
                }
            }
            Ok(_) => {}
            Err(e) => eprintln!("recv error: {e}"),
        }
    }
}
