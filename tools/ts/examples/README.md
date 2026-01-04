# LCM TypeScript Examples

## simple/

Basic publisher and subscriber demonstrating typed message handling.

```bash
cd simple

# Terminal 1: Subscribe to Vector3 messages
deno task sub

# Terminal 2: Publish Vector3 messages at 10 Hz
deno task pub
```

## web/

WebSocket bridge that forwards LCM packets to browser clients for real-time visualization.

```bash
cd web

# Start server on http://localhost:8080
deno task start
```

Features:
- Server uses `subscribePacket()` to forward raw packets
- Browser decodes messages with `@dimos/msgs` via ESM import
- Auto-reconnect on disconnect
