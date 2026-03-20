// Simple LCM Subscriber Example
// Receives Vector3 messages with typed decoding

use dimos_lcm::Lcm;
use lcm_msgs::geometry_msgs::Vector3;
use std::thread;
use std::time::Duration;

const CHANNEL: &str = "/vector#geometry_msgs.Vector3";

fn main() {
    let lcm = Lcm::new().expect("Failed to create LCM transport");

    println!("Listening for Vector3 on '/vector'...");
    println!("Press Ctrl+C to stop.\n");

    loop {
        match lcm.try_recv() {
            Ok(Some(msg)) if msg.channel == CHANNEL => {
                match Vector3::decode(&msg.data) {
                    Ok(vec) => {
                        println!(
                            "[{}] x={:.2} y={:.2} z={:.2}",
                            msg.channel, vec.x, vec.y, vec.z
                        );
                    }
                    Err(e) => eprintln!("decode error: {e}"),
                }
            }
            Ok(_) => {}
            Err(e) => eprintln!("recv error: {e}"),
        }
        thread::sleep(Duration::from_millis(1));
    }
}
