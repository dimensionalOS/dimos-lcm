#!/usr/bin/env -S deno run --allow-net --allow-read --unstable-net

// LCM to WebSocket Bridge
// Forwards raw LCM packets to browser clients for decoding

import { LCM } from "@dimos/lcm";
import { decodePacket, geometry_msgs } from "@dimos/msgs";

const PORT = 8080;
const clients = new Set<WebSocket>();

Deno.serve({ port: PORT }, async (req) => {
  const url = new URL(req.url);

  if (req.headers.get("upgrade") === "websocket") {
    const { socket, response } = Deno.upgradeWebSocket(req);
    socket.onopen = () => { console.log("Client connected"); clients.add(socket); };
    socket.onclose = () => { console.log("Client disconnected"); clients.delete(socket); };
    socket.onerror = () => clients.delete(socket);
    return response;
  }

  if (url.pathname === "/" || url.pathname === "/index.html") {
    const html = await Deno.readTextFile(new URL("./index.html", import.meta.url));
    return new Response(html, { headers: { "content-type": "text/html" } });
  }

  return new Response("Not found", { status: 404 });
});

console.log(`Server: http://localhost:${PORT}`);

const lcm = new LCM();
await lcm.start();

// Typed subscription - auto-decodes to geometry_msgs.Vector3
// Subscribes to "/vector#geometry_msgs.Vector3"
lcm.subscribe("/vector", geometry_msgs.Vector3, (msg) => {
  console.log(`[typed] x=${msg.data.x.toFixed(2)} y=${msg.data.y.toFixed(2)} z=${msg.data.z.toFixed(2)}`);
});

// Raw packet subscription - forwards all packets to WebSocket clients
lcm.subscribePacket((packet) => {
  // Log decoded message on server
  try {
    const { channel, data } = decodePacket(packet);
    console.log(`[${channel}]`, data);
  } catch (e) {
    console.error("Decode error:", e);
  }

  // Forward raw packet to all WebSocket clients
  for (const client of clients) {
    if (client.readyState === WebSocket.OPEN) {
      client.send(packet);
    }
  }
});

await lcm.run();
