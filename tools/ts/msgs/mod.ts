// @dimos/msgs - LCM Message Types for TypeScript
// Hand-written module that re-exports generated types and provides decode utilities

// Re-export all generated packages
export * as actionlib_msgs from "./generated/actionlib_msgs/mod.ts";
export * as builtin_interfaces from "./generated/builtin_interfaces/mod.ts";
export * as diagnostic_msgs from "./generated/diagnostic_msgs/mod.ts";
export * as foxglove_msgs from "./generated/foxglove_msgs/mod.ts";
export * as geometry_msgs from "./generated/geometry_msgs/mod.ts";
export * as nav_msgs from "./generated/nav_msgs/mod.ts";
export * as sensor_msgs from "./generated/sensor_msgs/mod.ts";
export * as shape_msgs from "./generated/shape_msgs/mod.ts";
export * as std_msgs from "./generated/std_msgs/mod.ts";
export * as stereo_msgs from "./generated/stereo_msgs/mod.ts";
export * as tf2_msgs from "./generated/tf2_msgs/mod.ts";
export * as trajectory_msgs from "./generated/trajectory_msgs/mod.ts";
export * as vision_msgs from "./generated/vision_msgs/mod.ts";
export * as visualization_msgs from "./generated/visualization_msgs/mod.ts";

// Import for registry population
import * as actionlib_msgs from "./generated/actionlib_msgs/mod.ts";
import * as builtin_interfaces from "./generated/builtin_interfaces/mod.ts";
import * as diagnostic_msgs from "./generated/diagnostic_msgs/mod.ts";
import * as foxglove_msgs from "./generated/foxglove_msgs/mod.ts";
import * as geometry_msgs from "./generated/geometry_msgs/mod.ts";
import * as nav_msgs from "./generated/nav_msgs/mod.ts";
import * as sensor_msgs from "./generated/sensor_msgs/mod.ts";
import * as shape_msgs from "./generated/shape_msgs/mod.ts";
import * as std_msgs from "./generated/std_msgs/mod.ts";
import * as stereo_msgs from "./generated/stereo_msgs/mod.ts";
import * as tf2_msgs from "./generated/tf2_msgs/mod.ts";
import * as trajectory_msgs from "./generated/trajectory_msgs/mod.ts";
import * as vision_msgs from "./generated/vision_msgs/mod.ts";
import * as visualization_msgs from "./generated/visualization_msgs/mod.ts";

// Message registry for decoding by hash
interface MessageClass<T> {
  readonly _NAME: string;
  _getPackedFingerprint(): bigint;
  decode(data: Uint8Array): T;
}

const _byHash = new Map<bigint, MessageClass<unknown>>();
const _byName = new Map<string, MessageClass<unknown>>();

function _registerPackage(pkg: Record<string, unknown>): void {
  for (const value of Object.values(pkg)) {
    if (value && typeof value === "function" && "_NAME" in value && "_getPackedFingerprint" in value && "decode" in value) {
      const cls = value as MessageClass<unknown>;
      _byHash.set(cls._getPackedFingerprint(), cls);
      _byName.set(cls._NAME, cls);
    }
  }
}

// Register all packages
_registerPackage(actionlib_msgs);
_registerPackage(builtin_interfaces);
_registerPackage(diagnostic_msgs);
_registerPackage(foxglove_msgs);
_registerPackage(geometry_msgs);
_registerPackage(nav_msgs);
_registerPackage(sensor_msgs);
_registerPackage(shape_msgs);
_registerPackage(std_msgs);
_registerPackage(stereo_msgs);
_registerPackage(tf2_msgs);
_registerPackage(trajectory_msgs);
_registerPackage(vision_msgs);
_registerPackage(visualization_msgs);

function _readHash(data: Uint8Array): bigint {
  const view = new DataView(data.buffer, data.byteOffset, 8);
  return view.getBigUint64(0, false); // big-endian, unsigned
}

/**
 * Decode an LCM message from binary data.
 * Type is auto-detected from the hash in the first 8 bytes.
 * @param data - Binary LCM message payload (not full packet)
 */
export function decode(data: Uint8Array): unknown {
  const hash = _readHash(data);
  const cls = _byHash.get(hash);
  if (!cls) throw new Error(`Unknown message hash: ${hash}`);
  return cls.decode(data);
}

/** Get all registered type names */
export function getTypeNames(): string[] {
  return [..._byName.keys()];
}

// LCM packet encoding/decoding for raw packet handling
const _MAGIC_SHORT = 0x4c433032; // "LC02"
const _SHORT_HEADER_SIZE = 8;
let _seqNum = Math.floor(Math.random() * 0xFFFFFFFF);

/**
 * Decode channel and raw payload from LCM packet (no type decoding).
 * @param packet - Raw LCM UDP packet bytes
 * @returns Object with channel string and raw payload bytes
 */
export function decodeChannel(packet: Uint8Array): { channel: string; payload: Uint8Array } {
  if (packet.length < _SHORT_HEADER_SIZE) throw new Error("Packet too short");
  const view = new DataView(packet.buffer, packet.byteOffset, packet.byteLength);
  const magic = view.getUint32(0, false);
  if (magic !== _MAGIC_SHORT) throw new Error("Invalid magic (only small messages supported)");

  let channelEnd = _SHORT_HEADER_SIZE;
  while (channelEnd < packet.length && packet[channelEnd] !== 0) channelEnd++;
  if (channelEnd >= packet.length) throw new Error("No null terminator for channel");

  const channel = new TextDecoder().decode(packet.subarray(_SHORT_HEADER_SIZE, channelEnd));
  const payload = packet.subarray(channelEnd + 1);
  return { channel, payload };
}

/**
 * Decode a raw LCM packet into channel and typed message.
 * @param packet - Raw LCM UDP packet bytes
 * @returns Object with channel string and decoded message data
 */
export function decodePacket(packet: Uint8Array): { channel: string; data: unknown } {
  const { channel, payload } = decodeChannel(packet);
  return { channel, data: decode(payload) };
}

/**
 * Encode channel and raw payload into LCM packet (no type encoding).
 * @param channel - Channel name
 * @param payload - Raw payload bytes
 * @returns Raw LCM packet bytes
 */
export function encodeChannel(channel: string, payload: Uint8Array): Uint8Array {
  const channelBytes = new TextEncoder().encode(channel);
  const packet = new Uint8Array(_SHORT_HEADER_SIZE + channelBytes.length + 1 + payload.length);
  const view = new DataView(packet.buffer);

  view.setUint32(0, _MAGIC_SHORT, false);
  view.setUint32(4, _seqNum++, false);
  packet.set(channelBytes, _SHORT_HEADER_SIZE);
  packet[_SHORT_HEADER_SIZE + channelBytes.length] = 0;
  packet.set(payload, _SHORT_HEADER_SIZE + channelBytes.length + 1);

  return packet;
}

/**
 * Encode a typed message into a raw LCM packet.
 * @param channel - Channel name to publish on
 * @param msg - Message instance with encode() method
 * @returns Raw LCM packet bytes ready to send
 */
export function encodePacket(channel: string, msg: { encode(): Uint8Array }): Uint8Array {
  return encodeChannel(channel, msg.encode());
}
