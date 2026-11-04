import { assertEquals } from "https://deno.land/std@0.208.0/assert/mod.ts";
import * as standalone from "../generated/ts_lcm_msgs/mod.ts";
import * as published from "../tools/ts/msgs/mod.ts";
const fixtures = JSON.parse(await Deno.readTextFile(new URL("./sim_wire_fixtures.json", import.meta.url)));
const bytes = (hex: string) => Uint8Array.from(hex.match(/../g)!.map(v => parseInt(v, 16)));
Deno.test("complete world state preserves acquisition and typed physical values", () => {
  const payload = bytes(fixtures.world_state);
  const m = standalone.decode(payload) as standalone.sim_msgs.WorldState;
  assertEquals(m.header.epoch, (1n << 60n) + 3n);
  assertEquals(m.header.time_ns, (1n << 60n) + 7n);
  assertEquals(m.body_poses[0].body_id, "g1/hand");
  assertEquals(m.body_poses[0].pose_world.position.x, 1);
  assertEquals(m.body_motion[0].frame_id, "g1/hand");
  assertEquals(Array.from(m.body_motion[0].linear_acceleration_world), [0, 0, -9.81]);
  assertEquals(Array.from(m.joint_truth.position), [.25]);
  assertEquals(Array.from(m.joint_truth.effort), []);
  assertEquals(m.extensions[0].schema, "example.thermal.v1");
  assertEquals(m.encode(), payload);
  assertEquals((published.decode(payload) as published.sim_msgs.WorldState).encode(), payload);
});
Deno.test("unrecognized extension bytes survive alongside typed fields", () => {
  const m = published.decode(bytes(fixtures.world_state)) as published.sim_msgs.WorldState;
  m.extensions[0].schema = "vendor.unrecognized.v2";
  const restored = published.decode(m.encode()) as published.sim_msgs.WorldState;
  assertEquals(restored.extensions[0].schema, "vendor.unrecognized.v2");
  assertEquals(restored.extensions[0].value, m.extensions[0].value);
  assertEquals(restored.body_poses[0].body_id, "g1/hand");
});
Deno.test("direct joint commands preserve PD, feedforward and validity", () => {
  const payload = bytes(fixtures.joint_command);
  const m = published.decode(payload) as published.control_msgs.JointCommand;
  assertEquals(m.targets[0].joint_id, "g1/elbow");
  assertEquals(m.targets[0].kp, 40);
  assertEquals(m.targets[0].feedforward, 2);
  assertEquals(m.valid_until_ns - m.apply_at_ns, 20000000n);
  assertEquals(m.encode(), payload);
});
