# LCM WebSocket Bridge

A web-based LCM message viewer. Listens for LCM messages and displays them in a browser via WebSocket.

## Usage

```bash
# Start the server
deno task start

# Or with watch mode for development
deno task dev
```

Then open http://localhost:8080 in your browser.

## How it works

1. **Server** (`server.ts`):
   - Subscribes to all LCM messages using `subscribeRaw("*", ...)`
   - Serves the web client at `/`
   - Forwards messages to connected WebSocket clients as JSON with base64-encoded binary data

2. **Client** (`index.html`):
   - Connects via WebSocket
   - Decodes common message types (Point, Vector3, Quaternion, Pose, String, etc.)
   - Displays messages in real-time with auto-reconnect

## Supported Message Types

The client includes inline decoders for:
- `geometry_msgs.Point`
- `geometry_msgs.Vector3`
- `geometry_msgs.Quaternion`
- `geometry_msgs.Pose`
- `std_msgs.String`
- `std_msgs.Int32`
- `std_msgs.Float64`

Unknown types are displayed as raw byte counts.

## Testing

Run the publisher example from `@dimos/lcm` to generate test messages:

```bash
cd ../lcm
deno task pub
```
