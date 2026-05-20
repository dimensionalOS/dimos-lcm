//! LCM burst test — characterizes how many large messages LCM can
//! reliably deliver under various burst conditions on loopback.
//!
//! Run with two processes:
//!   $ cargo run --release --example burst_test -- receiver
//!   $ cargo run --release --example burst_test -- sender <MSG_SIZE_BYTES> <COUNT> <INTERVAL_MS>
//!
//! Or single-process mode (sender + receiver in the same tokio runtime):
//!   $ cargo run --release --example burst_test -- both <MSG_SIZE_BYTES> <COUNT> <INTERVAL_MS>
//!
//! Reports: messages received vs sent, drop rate, per-message latency stats.

use dimos_lcm::{Lcm, LcmOptions};
use std::env;
use std::sync::atomic::{AtomicU32, Ordering};
use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::time::sleep;

const TOPIC: &str = "burst";

fn make_payload(seq: u32, total_size: usize) -> Vec<u8> {
    let mut buf = vec![0u8; total_size];
    buf[0..4].copy_from_slice(&seq.to_le_bytes());
    buf
}

fn parse_seq(buf: &[u8]) -> Option<u32> {
    if buf.len() < 4 {
        return None;
    }
    Some(u32::from_le_bytes([buf[0], buf[1], buf[2], buf[3]]))
}

async fn run_slow_receiver(expected: u32, duration: Duration, handler_ms: u64) -> (u32, Vec<u32>) {
    // Same as run_receiver but the recv task sleeps `handler_ms` after each
    // message to simulate a slow application handler. Used to test whether
    // sender-fast / receiver-slow scenarios cause LCM-level drops.
    let mut opts = LcmOptions::default();
    opts.recv_buf_size = Some(64 * 1024 * 1024);
    let lcm = Lcm::with_options(opts).await.expect("create lcm");
    eprintln!("[receiver] subscribed (handler_ms={}), waiting for messages...", handler_ms);
    let received = Arc::new(AtomicU32::new(0));
    let received_clone = received.clone();
    let recv_task = tokio::spawn(async move {
        let mut seqs = Vec::with_capacity(expected as usize);
        loop {
            match tokio::time::timeout(Duration::from_secs(5), lcm.recv()).await {
                Ok(Ok(msg)) => {
                    if msg.channel != TOPIC {
                        continue;
                    }
                    if let Some(seq) = parse_seq(&msg.data) {
                        seqs.push(seq);
                        let n = received_clone.fetch_add(1, Ordering::Relaxed) + 1;
                        if n % 25 == 0 || n <= 3 {
                            eprintln!("[receiver] got seq={} (total={})", seq, n);
                        }
                        if handler_ms > 0 {
                            tokio::time::sleep(Duration::from_millis(handler_ms)).await;
                        }
                    }
                }
                Ok(Err(e)) => {
                    eprintln!("[receiver] recv error: {e}");
                    break;
                }
                Err(_) => {
                    eprintln!("[receiver] 5s idle timeout, ending");
                    break;
                }
            }
        }
        seqs
    });

    let start = Instant::now();
    while start.elapsed() < duration && received.load(Ordering::Relaxed) < expected {
        sleep(Duration::from_millis(50)).await;
    }
    let seqs = recv_task.await.unwrap();
    let count = received.load(Ordering::Relaxed);
    (count, seqs)
}

async fn run_receiver(expected: u32, duration: Duration) -> (u32, Vec<u32>) {
    // Bump SO_RCVBUF to match what production dimos uses
    let mut opts = LcmOptions::default();
    opts.recv_buf_size = Some(64 * 1024 * 1024);
    let lcm = Lcm::with_options(opts).await.expect("create lcm");
    eprintln!("[receiver] subscribed, waiting for messages...");
    let received = Arc::new(AtomicU32::new(0));
    let received_clone = received.clone();
    let recv_task = tokio::spawn(async move {
        let mut seqs = Vec::with_capacity(expected as usize);
        loop {
            match tokio::time::timeout(Duration::from_secs(2), lcm.recv()).await {
                Ok(Ok(msg)) => {
                    if msg.channel != TOPIC {
                        eprintln!("[receiver] skipping channel '{}'", msg.channel);
                        continue;
                    }
                    if let Some(seq) = parse_seq(&msg.data) {
                        seqs.push(seq);
                        let n = received_clone.fetch_add(1, Ordering::Relaxed) + 1;
                        if n % 25 == 0 || n <= 3 {
                            eprintln!("[receiver] got seq={} (total={})", seq, n);
                        }
                    }
                }
                Ok(Err(e)) => {
                    eprintln!("[receiver] recv error: {e}");
                    break;
                }
                Err(_) => {
                    eprintln!("[receiver] 2s idle timeout, ending");
                    break;
                }
            }
        }
        seqs
    });

    // Wait for either expected count or duration
    let start = Instant::now();
    while start.elapsed() < duration && received.load(Ordering::Relaxed) < expected {
        sleep(Duration::from_millis(50)).await;
    }
    // Give the recv_task its 2s timeout to wind down
    let seqs = recv_task.await.unwrap();
    let count = received.load(Ordering::Relaxed);
    (count, seqs)
}

async fn run_sender(msg_size: usize, count: u32, interval_ms: u64) {
    let lcm = Lcm::new().await.expect("create lcm");
    // Brief warmup pause so any pre-existing subscriber is in its receive loop
    sleep(Duration::from_millis(200)).await;
    let start = Instant::now();
    for seq in 0..count {
        let payload = make_payload(seq, msg_size);
        lcm.publish(TOPIC, &payload).await.expect("publish");
        if interval_ms > 0 {
            sleep(Duration::from_millis(interval_ms)).await;
        }
    }
    let elapsed = start.elapsed();
    eprintln!(
        "[sender] sent {} messages of {} bytes in {:.3} s ({:.1} msg/s, {:.2} MB/s)",
        count,
        msg_size,
        elapsed.as_secs_f64(),
        count as f64 / elapsed.as_secs_f64(),
        (count as f64 * msg_size as f64) / 1024.0 / 1024.0 / elapsed.as_secs_f64(),
    );
}

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("usage: burst_test <sender|receiver|both> [msg_size] [count] [interval_ms]");
        std::process::exit(1);
    }
    let mode = &args[1];
    let msg_size: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(500_000);
    let count: u32 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(1000);
    let interval_ms: u64 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(100);

    match mode.as_str() {
        "sender" => run_sender(msg_size, count, interval_ms).await,
        "slow_receiver" => {
            // args: slow_receiver <count> <handler_ms>
            let recv_count: u32 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(100);
            let handler_ms: u64 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(100);
            let max_duration = Duration::from_secs(120);
            let (received, seqs) = run_slow_receiver(recv_count, max_duration, handler_ms).await;
            let unique: std::collections::HashSet<_> = seqs.iter().copied().collect();
            println!(
                "received={} unique={} expected={} drop_rate={:.1}%",
                received,
                unique.len(),
                recv_count,
                100.0 * (recv_count as f64 - unique.len() as f64) / recv_count as f64,
            );
        }
        "receiver" => {
            let max_duration = Duration::from_secs(120);
            let (received, seqs) = run_receiver(count, max_duration).await;
            let unique: std::collections::HashSet<_> = seqs.iter().copied().collect();
            println!(
                "received={} unique={} expected={} drop_rate={:.1}%",
                received,
                unique.len(),
                count,
                100.0 * (count as f64 - unique.len() as f64) / count as f64,
            );
            // Print gaps in sequence for diagnostic
            let mut sorted: Vec<u32> = unique.into_iter().collect();
            sorted.sort();
            let mut gaps = Vec::new();
            let mut prev = -1i64;
            for s in &sorted {
                let curr = *s as i64;
                if curr > prev + 1 && prev != -1 {
                    gaps.push((prev + 1, curr - 1));
                }
                prev = curr;
            }
            if !gaps.is_empty() {
                let total_missing: i64 = gaps.iter().map(|(a, b)| b - a + 1).sum();
                println!(
                    "missing-seq gaps: {} ranges, {} total missing seqs",
                    gaps.len(),
                    total_missing,
                );
                for (a, b) in gaps.iter().take(10) {
                    if a == b {
                        println!("  seq {} missing", a);
                    } else {
                        println!("  seqs [{}, {}] missing ({} seqs)", a, b, b - a + 1);
                    }
                }
            }
        }
        "both" => {
            // Spawn receiver first, give it 100ms to subscribe, then start sender
            let recv_count = count;
            let recv_task = tokio::spawn(async move {
                run_receiver(recv_count, Duration::from_secs(120)).await
            });
            sleep(Duration::from_millis(300)).await;
            run_sender(msg_size, count, interval_ms).await;
            let (received, seqs) = recv_task.await.unwrap();
            let unique: std::collections::HashSet<_> = seqs.iter().copied().collect();
            println!(
                "received={} unique={} expected={} drop_rate={:.1}%",
                received,
                unique.len(),
                count,
                100.0 * (count as f64 - unique.len() as f64) / count as f64,
            );
        }
        _ => {
            eprintln!("unknown mode: {}", mode);
            std::process::exit(1);
        }
    }
}
