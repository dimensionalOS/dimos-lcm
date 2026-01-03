#!/usr/bin/env -S deno run --allow-net --unstable-net

// Example: Publishing LCM messages
// Run with: deno task pub

import { LCM } from "@dimos/lcm";
import { Point } from "@dimos/msgs/geometry_msgs/mod.ts";

async function main() {
  const lcm = new LCM();
  await lcm.start();

  console.log("Publishing Point messages on 'EXAMPLE_POINT'...");
  console.log("Press Ctrl+C to stop.\n");

  let counter = 0;

  while (lcm.isRunning()) {
    const point = new Point({
      x: Math.sin(counter * 0.1) * 10,
      y: Math.cos(counter * 0.1) * 10,
      z: counter * 0.1,
    });

    await lcm.publish("EXAMPLE_POINT", point);
    console.log(`Published: x=${point.x.toFixed(2)}, y=${point.y.toFixed(2)}, z=${point.z.toFixed(2)}`);

    counter++;
    await new Promise((r) => setTimeout(r, 100)); // 10 Hz
  }
}

main().catch(console.error);
