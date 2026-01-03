#!/usr/bin/env -S deno run --allow-net --allow-read --unstable-net

// LCM to WebSocket Bridge
// Listens for LCM messages and forwards them to connected WebSocket clients

import { LCM } from "@dimos/lcm";

const PORT = 8080;
const clients = new Set<WebSocket>();

// Serve static files and WebSocket connections
Deno.serve({ port: PORT }, async (req) => {
  const url = new URL(req.url);

  // WebSocket upgrade
  if (req.headers.get("upgrade") === "websocket") {
    const { socket, response } = Deno.upgradeWebSocket(req);

    socket.onopen = () => {
      console.log("Client connected");
      clients.add(socket);
    };

    socket.onclose = () => {
      console.log("Client disconnected");
      clients.delete(socket);
    };

    socket.onerror = (e) => {
      console.error("WebSocket error:", e);
      clients.delete(socket);
    };

    return response;
  }

  // Serve static files
  if (url.pathname === "/" || url.pathname === "/index.html") {
    const html = await Deno.readTextFile(new URL("./index.html", import.meta.url));
    return new Response(html, {
      headers: { "content-type": "text/html" },
    });
  }

  // Serve the msgs bundle for browser
  if (url.pathname === "/msgs.js") {
    const js = await Deno.readTextFile(new URL("./msgs.bundle.js", import.meta.url));
    return new Response(js, {
      headers: { "content-type": "application/javascript" },
    });
  }

  return new Response("Not found", { status: 404 });
});

console.log(`HTTP server running at http://localhost:${PORT}`);
console.log("Open in browser to view LCM messages");

// Start LCM and forward messages to WebSocket clients
const lcm = new LCM();
await lcm.start();

console.log("Listening for LCM messages...");

// Subscribe to all raw messages and forward to WebSocket clients
lcm.subscribeRaw("*", (msg) => {
  // Send channel, type (from suffix), and raw binary data
  const [channel, typeName] = msg.channel.includes("#")
    ? msg.channel.split("#")
    : [msg.channel, null];

  console.log(`[${channel}]${typeName ? ` ${typeName}` : ""} ${msg.data.length} bytes`);

  // Build binary message: [channelLen:u16][channel][typeLen:u16][type][timestamp:f64][data]
  const encoder = new TextEncoder();
  const channelBytes = encoder.encode(channel);
  const typeBytes = encoder.encode(typeName || "");
  const headerSize = 2 + channelBytes.length + 2 + typeBytes.length + 8;
  const packet = new Uint8Array(headerSize + msg.data.length);
  const view = new DataView(packet.buffer);

  let offset = 0;
  view.setUint16(offset, channelBytes.length, true); offset += 2;
  packet.set(channelBytes, offset); offset += channelBytes.length;
  view.setUint16(offset, typeBytes.length, true); offset += 2;
  packet.set(typeBytes, offset); offset += typeBytes.length;
  view.setFloat64(offset, msg.timestamp, true); offset += 8;
  packet.set(msg.data, offset);

  for (const client of clients) {
    if (client.readyState === WebSocket.OPEN) {
      client.send(packet);
    }
  }
});

await lcm.run();
