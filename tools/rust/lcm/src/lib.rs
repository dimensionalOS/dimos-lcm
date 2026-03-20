//! Pure Rust LCM (Lightweight Communications and Marshalling) transport.
//!
//! Provides UDP multicast publish/subscribe for LCM messages.
//! No system LCM library required.
//!
//! # Example
//!
//! ```no_run
//! use dimos_lcm::Lcm;
//!
//! let lcm = Lcm::new().unwrap();
//!
//! // Publish
//! let data = vec![1, 2, 3];
//! lcm.publish("EXAMPLE", &data).unwrap();
//!
//! // Receive (non-blocking)
//! if let Ok(Some(msg)) = lcm.try_recv() {
//!     println!("{}: {} bytes", msg.channel, msg.data.len());
//! }
//! ```

mod transport;

pub use transport::{Lcm, LcmOptions, ReceivedMessage};
