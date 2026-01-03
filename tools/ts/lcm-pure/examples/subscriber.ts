#!/usr/bin/env -S deno run --allow-net --unstable-net

// Example: Subscribing to LCM messages
// Run with: deno task sub

import { LCM } from "../mod.ts";
import { Point } from "../../../../generated/ts_lcm_msgs/geometry_msgs/Point.ts";

async function main() {
  const lcm = new LCM();
  await lcm.start();

  console.log("Listening for messages...");
  console.log("Press Ctrl+C to stop.\n");

  // Subscribe to typed Point messages
  lcm.subscribeTyped("EXAMPLE_POINT", Point, (msg) => {
    console.log(
      `[${msg.channel}] Point: x=${msg.data.x.toFixed(2)}, y=${msg.data.y.toFixed(2)}, z=${msg.data.z.toFixed(2)}`
    );
  });

  // Subscribe to raw messages on any channel starting with "RAW_"
  lcm.subscribe("RAW_*", (msg) => {
    console.log(`[${msg.channel}] Raw: ${msg.data.length} bytes`);
  });

  await lcm.run();
}

main().catch(console.error);
