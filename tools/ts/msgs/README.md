# @dimos/msgs

LCM message types and packet utilities for TypeScript/Deno.

This package is transport-agnostic - use it with [`@dimos/lcm`](https://jsr.io/@dimos/lcm) for UDP multicast, or any transport (WebSocket, TCP, etc.) since it handles encoding/decoding independently.

## Installation

```bash
deno add jsr:@dimos/msgs
```

For UDP multicast transport, also install:
```bash
deno add jsr:@dimos/lcm
```

## Message Types

Import message types by package:

```typescript
import { geometry_msgs, std_msgs, sensor_msgs } from "@dimos/msgs";

const vec = new geometry_msgs.Vector3({ x: 1, y: 2, z: 3 });
const header = new std_msgs.Header({ seq: 1, frame_id: "base_link" });
```

Or import specific types:

```typescript
import { Vector3, PoseStamped } from "@dimos/msgs/geometry_msgs";
import { Header } from "@dimos/msgs/std_msgs";
```

### Available Packages

- `actionlib_msgs` - Action library messages
- `builtin_interfaces` - Time, Duration
- `diagnostic_msgs` - Diagnostic status/array
- `foxglove_msgs` - Foxglove visualization
- `geometry_msgs` - Point, Vector3, Pose, Transform, etc.
- `nav_msgs` - Odometry, Path, OccupancyGrid
- `sensor_msgs` - Image, PointCloud2, Imu, LaserScan, etc.
- `shape_msgs` - Mesh, Plane, SolidPrimitive
- `std_msgs` - Header, String, Int32, Float64, etc.
- `stereo_msgs` - DisparityImage
- `tf2_msgs` - TFMessage
- `trajectory_msgs` - JointTrajectory
- `vision_msgs` - Detection2D, BoundingBox3D
- `visualization_msgs` - Marker, MarkerArray

## Packet Encoding/Decoding

For WebSocket bridges and raw packet handling:

```typescript
import { decodePacket, decodeChannel, encodePacket, encodeChannel } from "@dimos/msgs";
```

### Decode Functions

```typescript
// Full decode: packet → { channel, data (typed) }
const { channel, data } = decodePacket(packet);
console.log(`[${channel}]`, data);

// Partial decode: packet → { channel, payload (raw bytes) }
const { channel, payload } = decodeChannel(packet);
// payload is Uint8Array, decode separately if needed
```

### Encode Functions

```typescript
import { geometry_msgs } from "@dimos/msgs";

// Full encode: channel + typed message → packet
const packet = encodePacket("/vector", new geometry_msgs.Vector3({ x: 1, y: 2, z: 3 }));

// Partial encode: channel + raw payload → packet
const packet = encodeChannel("/raw", someBytes);
```

### Auto-Decode by Hash

Decode payload bytes when you know it's a registered type:

```typescript
import { decode } from "@dimos/msgs";

// Payload must start with 8-byte hash
const msg = decode(payload);  // Returns typed message
```

### List Registered Types

```typescript
import { getTypeNames } from "@dimos/msgs";

console.log(getTypeNames());
// ["geometry_msgs.Vector3", "geometry_msgs.Point", "std_msgs.Header", ...]
```

## Message API

All message types share a common interface:

```typescript
// Construction with partial init
const pose = new geometry_msgs.Pose({
  position: new geometry_msgs.Point({ x: 1, y: 2, z: 3 }),
  orientation: new geometry_msgs.Quaternion({ w: 1 }),
});

// Encode to bytes (includes 8-byte hash prefix)
const bytes: Uint8Array = pose.encode();

// Decode from bytes
const decoded = geometry_msgs.Pose.decode(bytes);

// Static properties
geometry_msgs.Pose._NAME;  // "geometry_msgs.Pose"
geometry_msgs.Pose._HASH;  // Base hash (bigint)
geometry_msgs.Pose._getPackedFingerprint();  // Recursive hash for wire format
```

## WebSocket Bridge Example

Server (Deno):
```typescript
import { LCM } from "@dimos/lcm";

const lcm = new LCM();
await lcm.start();

lcm.subscribePacket((packet) => {
  for (const ws of clients) {
    ws.send(packet);
  }
});
```

Browser client:
```typescript
import { decodePacket } from "https://esm.sh/jsr/@dimos/msgs";

ws.onmessage = (event) => {
  const { channel, data } = decodePacket(new Uint8Array(event.data));
  console.log(`[${channel}]`, data);
};
```

## Transport Options

### UDP Multicast with @dimos/lcm

For standard LCM UDP multicast communication:

```typescript
import { LCM } from "@dimos/lcm";
import { geometry_msgs } from "@dimos/msgs";

const lcm = new LCM();
await lcm.start();

lcm.subscribe("/vector", geometry_msgs.Vector3, (msg) => {
  console.log(msg.data.x, msg.data.y, msg.data.z);
});

await lcm.publish("/vector", new geometry_msgs.Vector3({ x: 1, y: 2, z: 3 }));
```

See [`@dimos/lcm`](https://jsr.io/@dimos/lcm) for full documentation.

### Custom Transport

Use `encodePacket`/`decodePacket` with any transport:

```typescript
import { encodePacket, decodePacket, geometry_msgs } from "@dimos/msgs";

// Send over WebSocket, TCP, etc.
const packet = encodePacket("/vector", new geometry_msgs.Vector3({ x: 1, y: 2, z: 3 }));
socket.send(packet);

// Receive and decode
socket.onmessage = (data) => {
  const { channel, data: msg } = decodePacket(new Uint8Array(data));
  console.log(`[${channel}]`, msg);
};
```

## LCM Packet Format

Small messages (≤64KB):
```
[magic:4][seq:4][channel:null-terminated][payload]
```

- Magic: `0x4C433032` ("LC02")
- Seq: 32-bit sequence number
- Channel: UTF-8 string, null-terminated
- Payload: Message bytes starting with 8-byte hash
