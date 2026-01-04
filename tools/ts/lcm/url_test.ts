import { assertEquals, assertThrows } from "https://deno.land/std@0.208.0/assert/mod.ts";
import { parseUrl } from "./url.ts";

const DEFAULT_URL = "udpm://239.255.76.67:7667";

Deno.test("parseUrl - default URL", () => {
  const result = parseUrl();
  assertEquals(result.host, "239.255.76.67");
  assertEquals(result.port, 7667);
  assertEquals(result.ttl, 0);
});

Deno.test("parseUrl - explicit default", () => {
  const result = parseUrl(DEFAULT_URL);
  assertEquals(result.host, "239.255.76.67");
  assertEquals(result.port, 7667);
});

Deno.test("parseUrl - custom host and port", () => {
  const result = parseUrl("udpm://224.0.0.1:9999");
  assertEquals(result.host, "224.0.0.1");
  assertEquals(result.port, 9999);
});

Deno.test("parseUrl - with TTL", () => {
  const result = parseUrl("udpm://239.255.76.67:7667?ttl=1");
  assertEquals(result.host, "239.255.76.67");
  assertEquals(result.port, 7667);
  assertEquals(result.ttl, 1);
});

Deno.test("parseUrl - invalid scheme", () => {
  assertThrows(
    () => parseUrl("tcp://localhost:1234"),
    Error,
    "scheme"
  );
});

Deno.test("parseUrl - invalid format", () => {
  assertThrows(
    () => parseUrl("not-a-url"),
    Error
  );
});

Deno.test("parseUrl - empty URL uses defaults", () => {
  const result = parseUrl("udpm://");
  assertEquals(result.host, "239.255.76.67");
  assertEquals(result.port, 7667);
});
