# @dimos/lcm

Pure TypeScript implementation of the [LCM (Lightweight Communications and Marshalling)](https://lcm-proj.github.io/) protocol for Deno.

## Installation

```bash
deno add jsr:@dimos/lcm jsr:@dimos/msgs
```

## Features

- UDP multicast transport (default: `udpm://239.255.76.67:7667`)
- Small message support (single UDP packet, up to 64KB)
- Fragmented message support (large messages split across packets)
- Type-safe message encoding/decoding with generated types
- Wildcard channel subscriptions
- Raw packet forwarding for WebSocket bridges
- Full interop with Python/C++/Java LCM implementations

## Quick Start

```typescript
import { LCM } from "@dimos/lcm";
import { geometry_msgs } from "@dimos/msgs";

const lcm = new LCM();
await lcm.start();

// Subscribe to typed messages (type suffix added automatically)
lcm.subscribe("/vector", geometry_msgs.Vector3, (msg) => {
  console.log(`Received: x=${msg.data.x}, y=${msg.data.y}, z=${msg.data.z}`);
});

// Publish messages (type suffix added automatically)
const vec = new geometry_msgs.Vector3({ x: 1.0, y: 2.0, z: 3.0 });
await lcm.publish("/vector", vec);

// Run message loop
await lcm.run();
```

## Examples

### Simple Publisher/Subscriber

Basic examples demonstrating typed pub/sub:

```bash
cd examples/simple

# Terminal 1: Start subscriber
deno task sub

# Terminal 2: Start publisher
deno task pub
```

### WebSocket Bridge

Web-based LCM message viewer that forwards packets to browser clients:

```bash
cd examples/web

# Start server
deno task start

# Open http://localhost:8080
```

The web example demonstrates:
- `subscribePacket()` for raw packet forwarding
- Client-side decoding with `@dimos/msgs`

## API Reference

### Constructor

```typescript
// Default multicast group
const lcm = new LCM();

// Custom URL
const lcm = new LCM("udpm://239.255.76.67:7667?ttl=1");

// Options object
const lcm = new LCM({ url: "udpm://239.255.76.67:7667", ttl: 1 });
```

### Subscription Methods

#### `subscribe<T>(channel, msgClass, handler): () => void`
Typed subscription with automatic decoding. Type suffix is appended automatically.

```typescript
lcm.subscribe("/pose", geometry_msgs.PoseStamped, (msg) => {
  console.log(msg.data.pose.position.x); // Fully typed
});
// Subscribes to: /pose#geometry_msgs.PoseStamped
```

#### `subscribeRaw(pattern, handler): () => void`
Subscribe to parsed messages with raw payload bytes.

```typescript
lcm.subscribeRaw("SENSOR_*", (msg) => {
  console.log(msg.channel, msg.data); // data is Uint8Array
});
```

#### `subscribePacket(handler): () => void`
Subscribe to raw UDP packets. Useful for WebSocket forwarding.

```typescript
lcm.subscribePacket((packet) => {
  ws.send(packet); // Forward raw packet to WebSocket
});

// With channel filter
lcm.subscribePacket("/vector#*", (packet) => { ... });
```

### Publishing Methods

#### `publish<T>(channel, msg): Promise<void>`
Publish a typed message. Type suffix is appended automatically.

```typescript
await lcm.publish("/vector", new geometry_msgs.Vector3({ x: 1, y: 2, z: 3 }));
// Publishes to: /vector#geometry_msgs.Vector3
```

#### `publishRaw(channel, data): Promise<void>`
Publish raw bytes with a channel name.

#### `publishPacket(packet): Promise<void>`
Forward a pre-encoded LCM packet (e.g., from WebSocket client).

```typescript
ws.onmessage = (event) => {
  lcm.publishPacket(new Uint8Array(event.data));
};
```

### Control Methods

- `start(): Promise<void>` - Start listening for messages
- `stop(): void` - Stop and close socket
- `handle(timeoutMs?): number` - Process pending messages synchronously
- `handleAsync(timeoutMs?): Promise<number>` - Process messages async
- `run(callback?): Promise<void>` - Run message loop continuously
- `isRunning(): boolean` - Check if running

### Channel Patterns

Raw subscriptions support wildcard patterns:

```typescript
lcm.subscribeRaw("SENSOR_*", handler);  // SENSOR_IMU, SENSOR_GPS, etc.
lcm.subscribeRaw("*/status", handler);  // robot/status, arm/status, etc.
lcm.subscribeRaw("*", handler);         // All channels
```

## Companion Package: @dimos/msgs

The `@dimos/msgs` package provides message types and packet utilities:

```typescript
import { decodePacket, encodePacket, geometry_msgs } from "@dimos/msgs";

// Decode raw packet to { channel, data }
const { channel, data } = decodePacket(packet);

// Encode typed message to packet
const packet = encodePacket("/vector", new geometry_msgs.Vector3({ x: 1, y: 2, z: 3 }));
```

## Interop with Other Languages

LCM uses a common wire protocol. TypeScript can communicate with Python, C++, Java, etc.

### Channel Naming Convention

Typed channels include the message type as a suffix:
```
/my_topic#package.MessageType
```

This is handled automatically by `subscribe()` and `publish()`.

```typescript
// TypeScript - type suffix added automatically
lcm.subscribe("/robot/pose", geometry_msgs.PoseStamped, handler);
// Subscribes to: /robot/pose#geometry_msgs.PoseStamped

// Python publisher must use full channel name
lc.publish("/robot/pose#geometry_msgs.PoseStamped", pose.lcm_encode())
```

## Limitations

- Requires Deno's unstable net API (`--unstable-net` flag)
- Only UDP multicast transport (no TCP, no file logging)

## Running Tests

```bash
deno test --allow-net --allow-read --allow-write --allow-run
```
