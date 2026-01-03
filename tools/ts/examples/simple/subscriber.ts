#!/usr/bin/env -S deno run --allow-net --unstable-net

// Simple LCM Subscriber Example
// Receives Vector3 messages with typed decoding

import { LCM } from "@dimos/lcm";
import { geometry_msgs } from "@dimos/msgs";

const lcm = new LCM();
await lcm.start();

console.log("Listening for Vector3 on '/vector'...");
console.log("Press Ctrl+C to stop.\n");

// Typed subscription - auto-appends type suffix, auto-decodes
lcm.subscribe("/vector", geometry_msgs.Vector3, (msg) => {
  const { x, y, z } = msg.data;
  console.log(`[${msg.channel}] x=${x.toFixed(2)} y=${y.toFixed(2)} z=${z.toFixed(2)}`);
});

await lcm.run();
