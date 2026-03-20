// Simple LCM Publisher Example
// Publishes Vector3 messages at 10 Hz

use dimos_lcm::Lcm;
use lcm_msgs::geometry_msgs::Vector3;
use std::thread;
use std::time::Duration;

fn main() {
    let lcm = Lcm::new().expect("Failed to create LCM transport");

    println!("Publishing Vector3 on '/vector'...");
    println!("Press Ctrl+C to stop.\n");

    let mut t: f64 = 0.0;
    loop {
        let vec = Vector3 {
            x: t.sin() * 5.0,
            y: t.cos() * 5.0,
            z: t,
        };

        let data = vec.encode();
        lcm.publish("/vector#geometry_msgs.Vector3", &data)
            .expect("publish failed");
        println!(
            "Published: x={:.2} y={:.2} z={:.2}",
            vec.x, vec.y, vec.z
        );

        t += 0.1;
        thread::sleep(Duration::from_millis(100));
    }
}
