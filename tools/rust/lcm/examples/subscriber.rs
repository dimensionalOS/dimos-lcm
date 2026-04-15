// Simple LCM Subscriber Example
// Receives Vector3 messages with typed decoding

use dimos_lcm::LcmModule;
use lcm_msgs::geometry_msgs::Vector3;
use std::time::Instant;

#[tokio::main]
async fn main() {
    let mut subscriber = LcmModule::new().await.expect("Failed to create LcmModule (subscriber)");
    
    // in a Native Module, this will be handled by parsing the args
    subscriber.map_topic("vector", "/vector#geometry_msgs.Vector3");

    let mut vector = subscriber.input("vector", Vector3::decode);
    let _handle = subscriber.spawn();

    println!("Listening for Vector3 on {}", vector.topic);
    println!("Press Ctrl+C to stop\n");

    let mut last = Instant::now();

    loop {
        // run the processing on whichever topic receives a message first
        tokio::select! {
            Some(vec) = vector.recv() => {
                // processing for message goes here
                // can either do here, or move to a separate thread if cpu heavy
                let interval = last.elapsed();
                println!("Received: x={:.2} y={:.2} z={:.2} (interval {:.1}ms)",
                    vec.x, vec.y, vec.z, interval.as_secs_f64() * 1000.0
                );
                last = Instant::now();
            }
            // other subscribed topics are added here with the same pattern...
        }
    }
}
