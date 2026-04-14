use byteorder::{BigEndian, ByteOrder};
use socket2::{Domain, Protocol, Socket, Type};
use tokio::net::UdpSocket;
use std::io;
use std::net::{Ipv4Addr, SocketAddrV4};
use std::sync::atomic::{AtomicU32, Ordering};

const MAGIC_SHORT: u32 = 0x4c433032; // "LC02"
const SHORT_HEADER_SIZE: usize = 8;

/// Default LCM multicast group address.
pub const DEFAULT_MULTICAST_GROUP: Ipv4Addr = Ipv4Addr::new(239, 255, 76, 67);
/// Default LCM multicast port.
pub const DEFAULT_PORT: u16 = 7667;

static SEQ: AtomicU32 = AtomicU32::new(0);

/// Configuration for an LCM transport instance.
#[derive(Debug, Clone)]
pub struct LcmOptions {
    /// Multicast group address (default: 239.255.76.67).
    pub multicast_group: Ipv4Addr,
    /// UDP port (default: 7667).
    pub port: u16,
    /// Multicast TTL (default: 1).
    pub ttl: u32,
    /// Network interface to bind to (default: any).
    pub interface: Ipv4Addr,
}

impl Default for LcmOptions {
    fn default() -> Self {
        Self {
            multicast_group: DEFAULT_MULTICAST_GROUP,
            port: DEFAULT_PORT,
            ttl: 1,
            interface: Ipv4Addr::UNSPECIFIED,
        }
    }
}

/// A received LCM message.
#[derive(Debug, Clone)]
pub struct ReceivedMessage {
    /// Channel name (e.g., "/odom#geometry_msgs.PoseStamped").
    pub channel: String,
    /// Encoded message payload.
    pub data: Vec<u8>,
}

/// Pure Rust LCM UDP multicast transport.
///
/// Supports small-message encode/decode (no fragmentation).
/// This covers the vast majority of robotics control messages.
pub struct Lcm {
    socket: UdpSocket,
    multicast_addr: SocketAddrV4,
}

impl Lcm {
    /// Create a new LCM transport with default options.
    pub async fn new() -> io::Result<Self> {
        Self::with_options(LcmOptions::default()).await
    }

    /// Create a new LCM transport with custom options.
    pub async fn with_options(opts: LcmOptions) -> io::Result<Self> {
        let s2 = Socket::new(Domain::IPV4, Type::DGRAM, Some(Protocol::UDP))?;
        s2.set_reuse_address(true)?;
        #[cfg(not(target_os = "windows"))]
        s2.set_reuse_port(true)?;

        let bind_addr = SocketAddrV4::new(Ipv4Addr::UNSPECIFIED, opts.port);
        s2.bind(&bind_addr.into())?;

        let std_socket: std::net::UdpSocket = s2.into();
        std_socket.set_nonblocking(true)?;
        let socket = UdpSocket::from_std(std_socket)?;

        socket.join_multicast_v4(opts.multicast_group, opts.interface)?;
        socket.set_multicast_ttl_v4(opts.ttl)?;

        Ok(Self {
            socket,
            multicast_addr: SocketAddrV4::new(opts.multicast_group, opts.port),
        })
    }

    /// Publish encoded message data on the given channel.
    pub async fn publish(&self, channel: &str, data: &[u8]) -> io::Result<()> {
        let channel_bytes = channel.as_bytes();
        let total = SHORT_HEADER_SIZE + channel_bytes.len() + 1 + data.len();
        let mut buf = vec![0u8; total];

        BigEndian::write_u32(&mut buf[0..4], MAGIC_SHORT);
        BigEndian::write_u32(&mut buf[4..8], SEQ.fetch_add(1, Ordering::Relaxed));

        buf[SHORT_HEADER_SIZE..SHORT_HEADER_SIZE + channel_bytes.len()]
            .copy_from_slice(channel_bytes);
        // null terminator already 0 from vec![0u8; ..]
        let payload_start = SHORT_HEADER_SIZE + channel_bytes.len() + 1;
        buf[payload_start..].copy_from_slice(data);

        self.socket.send_to(&buf, self.multicast_addr).await?;
        Ok(())
    }


    /// Receive one LCM message asynchronously.
    ///
    /// Waits until a complete message arrives.
    pub async fn recv(&self) -> io::Result<ReceivedMessage> {
        let mut buf = vec![0u8; 65536];
        loop {
            let n = self.socket.recv(&mut buf).await?;
            if let Some(msg) = Self::decode_small(&buf[..n])? {
                return Ok(msg);
            }
            // Malformed or unknown packet — wait for the next one
        }
    }

    fn decode_small(buf: &[u8]) -> io::Result<Option<ReceivedMessage>> {
        if buf.len() < SHORT_HEADER_SIZE {
            return Ok(None);
        }
        let magic = BigEndian::read_u32(&buf[0..4]);
        if magic != MAGIC_SHORT {
            return Ok(None); // skip fragmented / unknown messages
        }
        let channel_start = SHORT_HEADER_SIZE;
        let channel_end = match buf[channel_start..].iter().position(|&b| b == 0) {
            Some(pos) => channel_start + pos,
            None => return Ok(None),
        };
        let channel = String::from_utf8_lossy(&buf[channel_start..channel_end]).into_owned();
        let data = buf[channel_end + 1..].to_vec();
        Ok(Some(ReceivedMessage { channel, data }))
    }
}
