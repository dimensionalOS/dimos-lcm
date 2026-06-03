import { assertEquals } from "https://deno.land/std@0.208.0/assert/mod.ts";
import { Point, Vector3, PoseStamped, Pose, Quaternion } from "@dimos/msgs/geometry_msgs/mod.ts";
import { Header } from "@dimos/msgs/std_msgs/mod.ts";

Deno.test("Point - encode/decode roundtrip", () => {
  const original = new Point({ x: 1.5, y: 2.5, z: 3.5 });
  const encoded = original.encode();
  const decoded = Point.decode(encoded);

  assertEquals(decoded.x, original.x);
  assertEquals(decoded.y, original.y);
  assertEquals(decoded.z, original.z);
});

Deno.test("Vector3 - encode/decode roundtrip", () => {
  const original = new Vector3({ x: -10.0, y: 0.0, z: 100.5 });
  const encoded = original.encode();
  const decoded = Vector3.decode(encoded);

  assertEquals(decoded.x, original.x);
  assertEquals(decoded.y, original.y);
  assertEquals(decoded.z, original.z);
});

Deno.test("Header - encode/decode roundtrip", () => {
  const original = new Header({
    seq: 42,
    frame_id: "base_link",
  });
  const encoded = original.encode();
  const decoded = Header.decode(encoded);

  assertEquals(decoded.seq, original.seq);
  assertEquals(decoded.frame_id, original.frame_id);
});

Deno.test("PoseStamped - encode/decode roundtrip (nested types)", () => {
  const original = new PoseStamped({
    header: new Header({ seq: 100, frame_id: "world" }),
    pose: new Pose({
      position: new Point({ x: 1.0, y: 2.0, z: 3.0 }),
      orientation: new Quaternion({ x: 0.0, y: 0.0, z: 0.0, w: 1.0 }),
    }),
  });

  const encoded = original.encode();
  const decoded = PoseStamped.decode(encoded);

  assertEquals(decoded.header.seq, 100);
  assertEquals(decoded.header.frame_id, "world");
  assertEquals(decoded.pose.position.x, 1.0);
  assertEquals(decoded.pose.position.y, 2.0);
  assertEquals(decoded.pose.position.z, 3.0);
  assertEquals(decoded.pose.orientation.w, 1.0);
});

Deno.test("Point - hash is consistent", () => {
  const hash1 = Point._getPackedFingerprint();
  const hash2 = Point._getPackedFingerprint();
  assertEquals(hash1, hash2);
});

Deno.test("PoseStamped - recursive hash includes nested types", () => {
  // The recursive hash should be different from the base hash
  const baseHash = PoseStamped._HASH;
  const recursiveHash = PoseStamped._getPackedFingerprint();

  // They should be different because PoseStamped has nested types
  assertEquals(baseHash !== recursiveHash, true);
});

Deno.test("Vector3 - default values", () => {
  const v = new Vector3();
  assertEquals(v.x, 0);
  assertEquals(v.y, 0);
  assertEquals(v.z, 0);
});

Deno.test("Point - partial initialization", () => {
  const p = new Point({ x: 5.0 });
  assertEquals(p.x, 5.0);
  assertEquals(p.y, 0);
  assertEquals(p.z, 0);
});
