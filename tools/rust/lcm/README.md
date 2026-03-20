# dimos-lcm (Rust)

Pure Rust LCM (Lightweight Communications and Marshalling) transport. No system LCM library required.

## Usage

```toml
[dependencies]
dimos-lcm = { git = "https://github.com/dimensionalOS/dimos-lcm.git", branch = "rust-codegen" }
lcm-msgs = { git = "https://github.com/dimensionalOS/dimos-lcm.git", branch = "rust-codegen" }
```

```rust
use dimos_lcm::Lcm;
use lcm_msgs::geometry_msgs::Vector3;

let lcm = Lcm::new()?;

// Publish
let vec = Vector3 { x: 1.0, y: 2.0, z: 3.0 };
lcm.publish("/vector#geometry_msgs.Vector3", &vec.encode())?;

// Subscribe (non-blocking poll)
if let Ok(Some(msg)) = lcm.try_recv() {
    let vec = Vector3::decode(&msg.data)?;
    println!("{}: x={} y={} z={}", msg.channel, vec.x, vec.y, vec.z);
}
```

## Examples

```bash
# In two terminals:
cargo run --example publisher
cargo run --example subscriber
```
