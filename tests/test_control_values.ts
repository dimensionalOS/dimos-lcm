import { assertEquals } from "https://deno.land/std@0.208.0/assert/mod.ts";
import * as standalone from "../generated/ts_lcm_msgs/mod.ts";
import * as published from "../tools/ts/msgs/mod.ts";

Deno.test("both TypeScript entrypoints decode ControlValues", () => {
  const original = new published.dimos_control_msgs.ControlValues({
    source: "cc",
    epoch: (1n << 60n) + 3n,
    sequence: (1n << 60n) + 4n,
    interface_names_length: 1,
    values_length: 1,
    interface_names: ["base/linear_x"],
    values: [0.5],
  });

  const decoded = standalone.decode(original.encode()) as standalone.dimos_control_msgs.ControlValues;

  assertEquals(decoded.epoch, original.epoch);
  assertEquals(decoded.sequence, original.sequence);
  assertEquals(decoded.interface_names, original.interface_names);
  assertEquals(decoded.values, original.values);
  assertEquals(published.decode(decoded.encode()), original);
});
