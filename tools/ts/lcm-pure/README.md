# LCM Pure TypeScript

Pure TypeScript implementation of the [LCM (Lightweight Communications and Marshalling)](https://lcm-proj.github.io/) protocol for Deno.

## Features

- UDP multicast transport (default: `udpm://239.255.76.67:7667`)
- Small message support (single UDP packet, up to 64KB)
- Fragmented message support (large messages split across packets)
- Type-safe message encoding/decoding with generated types
- Wildcard channel subscriptions
- Full interop with Python/C++/Java LCM implementations

## Quick Start

```typescript
import { LCM } from "./mod.ts";
import { Vector3 } from "../../generated/ts_lcm_msgs/geometry_msgs/Vector3.ts";

const lcm = new LCM();
await lcm.start();

// Subscribe to typed messages
lcm.subscribeTyped("MY_CHANNEL", Vector3, (msg) => {
  console.log(`Received: x=${msg.data.x}, y=${msg.data.y}, z=${msg.data.z}`);
});

// Publish messages
const vec = new Vector3({ x: 1.0, y: 2.0, z: 3.0 });
await lcm.publish("MY_CHANNEL", vec);

// Run message loop
await lcm.run();
```

## Running Examples

```bash
# Terminal 1: Start subscriber
deno task sub

# Terminal 2: Start publisher
deno task pub

# Or test interop with Python/C++ publishers
deno task interop
```

## API Reference

### Constructor

```typescript
// Default multicast group
const lcm = new LCM();

// Custom URL
const lcm = new LCM("udpm://239.255.76.67:7667?ttl=1");

// Options object
const lcm = new LCM({
  url: "udpm://239.255.76.67:7667",
  ttl: 1,
});
```

### Methods

#### `start(): Promise<void>`
Start the LCM instance and begin listening for messages.

#### `stop(): void`
Stop the LCM instance and close the socket.

#### `subscribe(channel: string, handler): () => void`
Subscribe to raw messages on a channel. Returns an unsubscribe function.

```typescript
const unsub = lcm.subscribe("CHANNEL", (msg) => {
  console.log(msg.channel, msg.data); // data is Uint8Array
});
unsub(); // Stop receiving
```

#### `subscribeTyped<T>(channel: string, msgClass, handler): () => void`
Subscribe to typed messages with automatic decoding.

```typescript
lcm.subscribeTyped("POSE", PoseStamped, (msg) => {
  console.log(msg.data.pose.position.x); // Fully typed
});
```

#### `publish<T>(channel: string, msg: T): Promise<void>`
Publish a typed message.

```typescript
await lcm.publish("CHANNEL", new Vector3({ x: 1, y: 2, z: 3 }));
```

#### `publishRaw(channel: string, data: Uint8Array): Promise<void>`
Publish raw bytes.

#### `handle(timeoutMs?: number): number`
Process pending messages synchronously. Returns number of messages handled.

#### `handleAsync(timeoutMs?: number): Promise<number>`
Process messages asynchronously, waiting for at least one or timeout.

#### `run(callback?: () => void): Promise<void>`
Run the message loop continuously until `stop()` is called.

### Channel Patterns

Subscriptions support wildcard patterns:

```typescript
lcm.subscribe("SENSOR_*", handler);     // Matches SENSOR_IMU, SENSOR_GPS, etc.
lcm.subscribe("*/status", handler);     // Matches robot/status, arm/status, etc.
lcm.subscribe("*", handler);            // Matches all channels
```

## Interop with Other Languages

LCM uses a common wire protocol, so TypeScript can communicate with Python, C++, Java, etc.

### Channel Naming Convention

When using typed channels (recommended for interop), include the type in the channel name:

```
/my_topic#package.MessageType
```

Example:
```typescript
// TypeScript subscriber
lcm.subscribeTyped("/robot/pose#geometry_msgs.PoseStamped", PoseStamped, handler);

// Python publisher
lc.publish("/robot/pose#geometry_msgs.PoseStamped", pose.lcm_encode())
```

## Protocol Details

This implementation follows the [LCM UDP multicast protocol](https://lcm-proj.github.io/group__LcmC__lcm__t.html):

- **Small messages** (≤64KB): 8-byte header + channel name + payload
- **Fragmented messages** (>64KB): 20-byte header per fragment

The message fingerprint (hash) is computed using the same algorithm as the C implementation, ensuring binary compatibility across all LCM language bindings.

## Limitations

- Requires Deno's unstable net API (`--unstable-net` flag)
- Only UDP multicast transport is supported (no TCP, no file logging)
- Multicast group membership relies on OS-level configuration

## Files

```
lcm-pure/
├── mod.ts          # Main exports
├── lcm.ts          # LCM class implementation
├── transport.ts    # UDP multicast, packet encoding/decoding
├── types.ts        # TypeScript type definitions
├── url.ts          # LCM URL parser
├── examples/
│   ├── publisher.ts   # Publish example
│   ├── subscriber.ts  # Subscribe example
│   └── interop.ts     # Cross-language interop example
└── README.md
```
