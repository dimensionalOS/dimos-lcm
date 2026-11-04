import { assertEquals } from "https://deno.land/std@0.208.0/assert/mod.ts";
import * as standalone from "../generated/ts_lcm_msgs/mod.ts";
import * as published from "../tools/ts/msgs/mod.ts";
const fixtures=JSON.parse(await Deno.readTextFile(new URL("./sim_wire_fixtures.json",import.meta.url)));
const bytes=(hex:string)=>Uint8Array.from(hex.match(/../g)!.map(v=>parseInt(v,16)));
Deno.test("named body poses preserve 64-bit clock fields across languages",()=>{
 const payload=bytes(fixtures.body_poses);
 const m=standalone.decode(payload) as standalone.sim_msgs.BodyPoses;
 assertEquals(m.header.epoch,(1n<<60n)+3n);
 assertEquals(m.header.time_ns,(1n<<60n)+7n);
 assertEquals(m.bodies[0].body_id,"g1/hand");
 assertEquals(m.bodies[0].pose_world.position.x,1);
 assertEquals(m.encode(),payload);
 assertEquals((published.decode(payload) as published.sim_msgs.BodyPoses).encode(),payload);
});
Deno.test("direct joint commands preserve PD, feedforward and validity",()=>{
 const payload=bytes(fixtures.joint_command);
 const m=published.decode(payload) as published.control_msgs.JointCommand;
 assertEquals(m.targets[0].joint_id,"g1/elbow");
 assertEquals(m.targets[0].kp,40);
 assertEquals(m.targets[0].feedforward,2);
 assertEquals(m.valid_until_ns-m.apply_at_ns,20000000n);
 assertEquals(m.encode(),payload);
});
Deno.test("body motion remains physical truth",()=>{
 const payload=bytes(fixtures.body_motion);
 const m=standalone.decode(payload) as standalone.sim_msgs.BodyMotion;
 assertEquals(Array.from(m.linear_acceleration_world),[0,0,-9.81]);
 assertEquals(Array.from(m.gravity_world),[0,0,-9.81]);
 assertEquals(m.encode(),payload);
});
