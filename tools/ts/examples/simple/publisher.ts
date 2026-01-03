#!/usr/bin/env -S deno run --allow-net --unstable-net

// Simple LCM Publisher Example
// Publishes Vector3 messages at 10 Hz

import { LCM } from "@dimos/lcm";
import { geometry_msgs } from "@dimos/msgs";

const lcm = new LCM();
await lcm.start();

console.log("Publishing Vector3 on '/vector'...");
console.log("Press Ctrl+C to stop.\n");

let t = 0;
while (lcm.isRunning()) {
  const vec = new geometry_msgs.Vector3({
    x: Math.sin(t) * 5,
    y: Math.cos(t) * 5,
    z: t,
  });

  await lcm.publish("/vector", vec);
  console.log(`Published: x=${vec.x.toFixed(2)} y=${vec.y.toFixed(2)} z=${vec.z.toFixed(2)}`);

  t += 0.1;
  await new Promise((r) => setTimeout(r, 100));
}
