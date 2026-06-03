import { assertEquals, assertNotEquals } from "https://deno.land/std@0.208.0/assert/mod.ts";
import {
  encodeSmallMessage,
  encodeFragmentedMessage,
  decodePacket,
  FragmentReassembler,
} from "./transport.ts";
import { MAGIC_SHORT, MAGIC_LONG } from "./types.ts";

Deno.test("encodeSmallMessage - basic", () => {
  const channel = "TEST";
  const data = new Uint8Array([1, 2, 3, 4]);
  const seqNum = 42;

  const encoded = encodeSmallMessage(channel, data, seqNum);
  const view = new DataView(encoded.buffer);

  // Check magic number
  assertEquals(view.getUint32(0, false), MAGIC_SHORT);

  // Check sequence number
  assertEquals(view.getUint32(4, false), seqNum);

  // Check channel name (starts at offset 8)
  const channelBytes = new TextEncoder().encode(channel);
  for (let i = 0; i < channelBytes.length; i++) {
    assertEquals(encoded[8 + i], channelBytes[i]);
  }

  // Check null terminator
  assertEquals(encoded[8 + channelBytes.length], 0);

  // Check payload
  const payloadStart = 8 + channelBytes.length + 1;
  for (let i = 0; i < data.length; i++) {
    assertEquals(encoded[payloadStart + i], data[i]);
  }
});

Deno.test("decodePacket - small message roundtrip", () => {
  const channel = "ROUNDTRIP_TEST";
  const data = new Uint8Array([10, 20, 30, 40, 50]);
  const seqNum = 123;

  const encoded = encodeSmallMessage(channel, data, seqNum);
  const decoded = decodePacket(encoded);

  assertNotEquals(decoded, null);
  if (decoded === null) throw new Error("decoded is null");
  assertEquals(decoded.type, "small");

  if (decoded.type === "small") {
    assertEquals(decoded.channel, channel);
    assertEquals(decoded.sequenceNumber, seqNum);
    assertEquals(decoded.data.length, data.length);
    for (let i = 0; i < data.length; i++) {
      assertEquals(decoded.data[i], data[i]);
    }
  }
});

Deno.test("encodeFragmentedMessage - creates multiple fragments", () => {
  const channel = "FRAG_TEST";
  const data = new Uint8Array(2000); // Large enough to fragment
  for (let i = 0; i < data.length; i++) {
    data[i] = i % 256;
  }
  const seqNum = 999;

  const fragments = encodeFragmentedMessage(channel, data, seqNum, 1000);

  // Should have multiple fragments
  assertEquals(fragments.length > 1, true);

  // First fragment should have MAGIC_LONG
  const view0 = new DataView(fragments[0].buffer);
  assertEquals(view0.getUint32(0, false), MAGIC_LONG);

  // All fragments should have same sequence number
  for (const frag of fragments) {
    const view = new DataView(frag.buffer);
    assertEquals(view.getUint32(4, false), seqNum);
  }
});

Deno.test("FragmentReassembler - reassembles complete message", () => {
  const channel = "REASSEMBLE_TEST";
  const originalData = new Uint8Array(2000);
  for (let i = 0; i < originalData.length; i++) {
    originalData[i] = i % 256;
  }
  const seqNum = 555;

  const fragments = encodeFragmentedMessage(channel, originalData, seqNum, 1000);
  const reassembler = new FragmentReassembler();

  let result: { channel: string; data: Uint8Array } | null = null;
  for (const fragBytes of fragments) {
    const decoded = decodePacket(fragBytes);
    if (decoded === null) throw new Error("decoded is null");
    assertEquals(decoded.type, "fragment");

    if (decoded.type === "fragment") {
      result = reassembler.processFragment(decoded);
    }
  }

  // Should have complete message after last fragment
  if (result === null) throw new Error("result is null");
  assertEquals(result.channel, channel);
  assertEquals(result.data.length, originalData.length);

  for (let i = 0; i < originalData.length; i++) {
    assertEquals(result.data[i], originalData[i]);
  }
});

Deno.test("decodePacket - returns null for invalid magic", () => {
  const badPacket = new Uint8Array(20);
  new DataView(badPacket.buffer).setUint32(0, 0xDEADBEEF, false);

  const result = decodePacket(badPacket);
  assertEquals(result, null);
});

Deno.test("decodePacket - returns null for too-short packet", () => {
  const shortPacket = new Uint8Array(4);
  const result = decodePacket(shortPacket);
  assertEquals(result, null);
});
