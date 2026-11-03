import { assertEquals } from "https://deno.land/std@0.208.0/assert/mod.ts";
import * as standalone from "../generated/ts_lcm_msgs/mod.ts";
import * as published from "../tools/ts/msgs/mod.ts";

const fixtures = JSON.parse(
  await Deno.readTextFile(new URL("./sim_wire_fixtures.json", import.meta.url)),
);
const bytes = (hex: string) =>
  Uint8Array.from(hex.match(/../g)!.map((v) => parseInt(v, 16)));

Deno.test("Python scene observations decode and re-encode through both TS entrypoints", () => {
  const payload = bytes(fixtures.observations);
  const message = standalone.decode(
    payload,
  ) as standalone.sim_msgs.Observations;
  assertEquals(message.epoch, (1n << 60n) + 3n);
  assertEquals(message.complete, true);
  assertEquals(message.observations[0].entity_id, "g1/hand");
  const pose = standalone.geometry_msgs.Pose.decode(
    message.observations[0].data,
  );
  assertEquals(pose.position.x, 1);
  assertEquals(pose.orientation.w, 1);
  assertEquals(message.encode(), payload);
  assertEquals(
    (published.decode(payload) as published.sim_msgs.Observations).encode(),
    payload,
  );
});

Deno.test("Python action batch preserves joint command semantics in TS", () => {
  const payload = bytes(fixtures.actions);
  const message = published.decode(payload) as published.sim_msgs.Actions;
  const command = published.sim_msgs.JointCommand.decode(
    message.actions[0].data,
  );
  assertEquals(command.names, ["g1/elbow"]);
  assertEquals(Array.from(command.position), [.25]);
  assertEquals(Array.from(command.kp), [40]);
  assertEquals(Array.from(command.effort), [2]);
  assertEquals(message.encode(), payload);
});
