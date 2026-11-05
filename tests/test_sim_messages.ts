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
  assertEquals(m.bodies[0].body_id, "g1/hand");
  assertEquals(m.bodies[0].pose.position.x, 1);
  const b = m.bodies[0], a = b.acceleration.linear;
  assertEquals([a.x, a.y, a.z], [0, 0, -9.81]);
  const alpha = b.acceleration.angular;
  assertEquals([alpha.x, alpha.y, alpha.z], [4, 5, 6]);
  assertEquals([b.twist.linear.x, b.twist.linear.y, b.twist.linear.z], [.1, .2, .3]);
  assertEquals([b.twist.angular.x, b.twist.angular.y, b.twist.angular.z], [1, 2, 3]);
  assertEquals(BigInt(m.joint_truth.header.stamp.sec) * 1000000000n +
    BigInt(m.joint_truth.header.stamp.nsec), m.header.time_ns);
  assertEquals(Array.from(m.joint_truth.position), [.25]);
  assertEquals(Array.from(m.joint_truth.effort), []);
  assertEquals(m.cbor_observations[0].key, "thermal");
  assertEquals(m.encode(), payload);
  assertEquals((published.decode(payload) as published.sim_msgs.WorldState).encode(), payload);
});
Deno.test("unrecognized observation bytes survive alongside typed fields", () => {
  const m = published.decode(bytes(fixtures.world_state)) as published.sim_msgs.WorldState;
  m.cbor_observations[0].key = "vendor.unrecognized.v2";
  const restored = published.decode(m.encode()) as published.sim_msgs.WorldState;
  assertEquals(restored.cbor_observations[0].key, "vendor.unrecognized.v2");
  assertEquals(restored.cbor_observations[0].value, m.cbor_observations[0].value);
  assertEquals(restored.bodies[0].body_id, "g1/hand");
});
Deno.test("unified actions preserve joint targets, CBOR and validity", () => {
  const payload = bytes(fixtures.action_command);
  const m = published.decode(payload) as published.control_msgs.ActionCommand;
  assertEquals(m.header.time_ns, (1n << 60n) + 7n);
  assertEquals(m.cbor_commands[0].entity_id, "world");
  assertEquals(m.cbor_commands[0].key, "increment");
  assertEquals(Array.from(m.cbor_commands[0].value), [1]);
  assertEquals((standalone.decode(payload) as standalone.control_msgs.ActionCommand).encode(), payload);
  assertEquals(m.joint_commands[0].joint_id, "g1/elbow");
  assertEquals(m.joint_commands[0].kp, 40);
  assertEquals(m.joint_commands[0].feedforward, 2);
  assertEquals(m.valid_until_ns - m.apply_at_ns, 20000000n);
  assertEquals(m.encode(), payload);
});
