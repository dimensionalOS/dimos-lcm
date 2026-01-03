#!/usr/bin/env -S deno run --allow-net --unstable-net

// Example: Interop with Python/C++ LCM publishers
// This demonstrates receiving messages from other LCM implementations
//
// Run a Python publisher like:
//   lc = lcm.LCM()
//   lc.publish("/vector#geometry_msgs.Vector3", Vector3(x=1, y=2, z=3).lcm_encode())

import { LCM } from "@dimos/lcm";
import { Vector3, PoseStamped } from "@dimos/msgs/geometry_msgs/mod.ts";

async function main() {
  const lcm = new LCM();
  await lcm.start();

  console.log("Listening for LCM messages from other processes...");
  console.log("Subscribed channels:");
  console.log("  - /vector (geometry_msgs.Vector3)");
  console.log("  - /pose (geometry_msgs.PoseStamped)");
  console.log("\nPress Ctrl+C to stop.\n");

  // Subscribe to Vector3 messages (type suffix added automatically)
  lcm.subscribe("/vector", Vector3, (msg) => {
    const v = msg.data;
    console.log(`[Vector3] x=${v.x.toFixed(2)}, y=${v.y.toFixed(2)}, z=${v.z.toFixed(2)}`);
  });

  // Subscribe to PoseStamped messages (type suffix added automatically)
  lcm.subscribe("/pose", PoseStamped, (msg) => {
    const p = msg.data.pose.position;
    const o = msg.data.pose.orientation;
    console.log(
      `[PoseStamped] pos=(${p.x.toFixed(2)}, ${p.y.toFixed(2)}, ${p.z.toFixed(2)}) ` +
      `quat=(${o.x.toFixed(2)}, ${o.y.toFixed(2)}, ${o.z.toFixed(2)}, ${o.w.toFixed(2)})`
    );
  });

  // Also log any unhandled channels
  lcm.subscribeRaw("*", (msg) => {
    if (!msg.channel.includes("vector") && !msg.channel.includes("pose")) {
      console.log(`[${msg.channel}] ${msg.data.length} bytes`);
    }
  });

  await lcm.run();
}

main().catch(console.error);
