import { assertEquals, assertThrows } from "https://deno.land/std@0.208.0/assert/mod.ts";
import {
  decode,
  decodeChannel,
  decodePacket,
  encodeChannel,
  encodePacket,
  getTypeNames,
} from "./mod.ts";
import { Vector3 } from "./generated/geometry_msgs/mod.ts";

Deno.test("getTypeNames - returns registered types", () => {
  const names = getTypeNames();
  assertEquals(names.includes("geometry_msgs.Vector3"), true);
  assertEquals(names.includes("std_msgs.Header"), true);
  assertEquals(names.length > 10, true); // Should have many types
});

Deno.test("decode - decodes payload by hash", () => {
  const original = new Vector3({ x: 1.5, y: 2.5, z: 3.5 });
  const payload = original.encode();

  const decoded = decode(payload) as Vector3;
  assertEquals(decoded.x, 1.5);
  assertEquals(decoded.y, 2.5);
  assertEquals(decoded.z, 3.5);
});

Deno.test("decode - throws for unknown hash", () => {
  const badPayload = new Uint8Array(16);
  new DataView(badPayload.buffer).setBigUint64(0, 0xDEADBEEFn, false);

  assertThrows(() => decode(badPayload), Error, "Unknown message hash");
});

Deno.test("encodeChannel/decodeChannel - roundtrip", () => {
  const channel = "/test/channel";
  const payload = new Uint8Array([1, 2, 3, 4, 5]);

  const packet = encodeChannel(channel, payload);
  const decoded = decodeChannel(packet);

  assertEquals(decoded.channel, channel);
  assertEquals(decoded.payload.length, payload.length);
  for (let i = 0; i < payload.length; i++) {
    assertEquals(decoded.payload[i], payload[i]);
  }
});

Deno.test("encodePacket/decodePacket - roundtrip with typed message", () => {
  const channel = "/vector";
  const original = new Vector3({ x: 10.0, y: 20.0, z: 30.0 });

  const packet = encodePacket(channel, original);
  const { channel: decodedChannel, data } = decodePacket(packet);

  assertEquals(decodedChannel, channel);
  const decoded = data as Vector3;
  assertEquals(decoded.x, 10.0);
  assertEquals(decoded.y, 20.0);
  assertEquals(decoded.z, 30.0);
});

Deno.test("decodeChannel - throws for invalid packet", () => {
  const badPacket = new Uint8Array(4); // too short
  assertThrows(() => decodeChannel(badPacket), Error);
});

Deno.test("decodeChannel - throws for bad magic", () => {
  const badPacket = new Uint8Array(20);
  new DataView(badPacket.buffer).setUint32(0, 0xDEADBEEF, false);

  assertThrows(() => decodeChannel(badPacket), Error, "Invalid magic");
});

Deno.test("encodeChannel - sequence number increments", () => {
  const channel = "test";
  const payload = new Uint8Array([1]);

  const packet1 = encodeChannel(channel, payload);
  const packet2 = encodeChannel(channel, payload);

  const view1 = new DataView(packet1.buffer, packet1.byteOffset);
  const view2 = new DataView(packet2.buffer, packet2.byteOffset);

  const seq1 = view1.getUint32(4, false);
  const seq2 = view2.getUint32(4, false);

  assertEquals(seq2, seq1 + 1);
});
