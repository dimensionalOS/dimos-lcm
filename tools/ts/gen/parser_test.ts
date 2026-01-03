import { assertEquals, assertThrows } from "jsr:@std/assert";
import { parse } from "./parser.ts";

Deno.test("parse empty struct", () => {
  const result = parse(`
    package test;
    struct empty_t {}
  `);

  assertEquals(result.package, "test");
  assertEquals(result.types.length, 1);
  assertEquals(result.types[0].kind, "struct");
  assertEquals(result.types[0].name, "empty_t");
  assertEquals(result.types[0].fullName, "test.empty_t");
});

Deno.test("parse primitives", () => {
  const result = parse(`
    package test;
    struct primitives_t {
      int8_t a;
      int16_t b;
      int32_t c;
      int64_t d;
      float e;
      double f;
      string g;
      boolean h;
      byte i;
    }
  `);

  const struct = result.types[0];
  if (struct.kind !== "struct") throw new Error("Expected struct");

  assertEquals(struct.members.length, 9);
  assertEquals(struct.members[0].type, "int8_t");
  assertEquals(struct.members[0].name, "a");
  assertEquals(struct.members[8].type, "byte");
  assertEquals(struct.members[8].name, "i");
});

Deno.test("parse fixed array", () => {
  const result = parse(`
    package test;
    struct arrays_t {
      double position[3];
      int32_t matrix[4][4];
    }
  `);

  const struct = result.types[0];
  if (struct.kind !== "struct") throw new Error("Expected struct");

  assertEquals(struct.members[0].name, "position");
  assertEquals(struct.members[0].dimensions.length, 1);
  assertEquals(struct.members[0].dimensions[0].size, "3");
  assertEquals(struct.members[0].dimensions[0].isConstant, true);

  assertEquals(struct.members[1].name, "matrix");
  assertEquals(struct.members[1].dimensions.length, 2);
  assertEquals(struct.members[1].dimensions[0].size, "4");
  assertEquals(struct.members[1].dimensions[1].size, "4");
});

Deno.test("parse dynamic array", () => {
  const result = parse(`
    package test;
    struct dynamic_t {
      int32_t num_items;
      double items[num_items];
    }
  `);

  const struct = result.types[0];
  if (struct.kind !== "struct") throw new Error("Expected struct");

  assertEquals(struct.members[1].name, "items");
  assertEquals(struct.members[1].dimensions[0].size, "num_items");
  assertEquals(struct.members[1].dimensions[0].isConstant, false);
});

Deno.test("parse constants", () => {
  const result = parse(`
    package test;
    struct consts_t {
      const int32_t FOO = 42;
      const double PI = 3.14159;
      const int64_t BIG = 0xdeadbeef;
    }
  `);

  const struct = result.types[0];
  if (struct.kind !== "struct") throw new Error("Expected struct");

  assertEquals(struct.constants.length, 3);
  assertEquals(struct.constants[0].name, "FOO");
  assertEquals(struct.constants[0].value, "42");
  assertEquals(struct.constants[1].name, "PI");
  assertEquals(struct.constants[1].value, "3.14159");
  assertEquals(struct.constants[2].name, "BIG");
  assertEquals(struct.constants[2].value, "0xdeadbeef");
});

Deno.test("parse multiple constants on one line", () => {
  const result = parse(`
    package test;
    struct multi_const_t {
      const int32_t A = 1, B = 2, C = 3;
    }
  `);

  const struct = result.types[0];
  if (struct.kind !== "struct") throw new Error("Expected struct");

  assertEquals(struct.constants.length, 3);
  assertEquals(struct.constants[0].name, "A");
  assertEquals(struct.constants[1].name, "B");
  assertEquals(struct.constants[2].name, "C");
});

Deno.test("parse qualified type name", () => {
  const result = parse(`
    package exlcm;
    struct node_t {
      int32_t num_children;
      exlcm.node_t children[num_children];
    }
  `);

  const struct = result.types[0];
  if (struct.kind !== "struct") throw new Error("Expected struct");

  assertEquals(struct.members[1].type, "exlcm.node_t");
});

Deno.test("parse enum", () => {
  const result = parse(`
    package test;
    enum status_t {
      OK,
      ERROR,
      PENDING = 10,
      DONE
    }
  `);

  assertEquals(result.types[0].kind, "enum");
  const enumType = result.types[0];
  if (enumType.kind !== "enum") throw new Error("Expected enum");

  assertEquals(enumType.values.length, 4);
  assertEquals(enumType.values[0].name, "OK");
  assertEquals(enumType.values[0].value, 0);
  assertEquals(enumType.values[1].name, "ERROR");
  assertEquals(enumType.values[1].value, 1);
  assertEquals(enumType.values[2].name, "PENDING");
  assertEquals(enumType.values[2].value, 10);
  assertEquals(enumType.values[3].name, "DONE");
  assertEquals(enumType.values[3].value, 11);
});

Deno.test("parse comments are ignored", () => {
  const result = parse(`
    // This is a comment
    package test;
    /* Multi-line
       comment */
    struct foo_t {
      int32_t x; // inline comment
    }
  `);

  assertEquals(result.package, "test");
  const struct = result.types[0];
  if (struct.kind !== "struct") throw new Error("Expected struct");
  assertEquals(struct.members.length, 1);
});

Deno.test("parse no package", () => {
  const result = parse(`
    struct bare_t {
      int32_t value;
    }
  `);

  assertEquals(result.package, "");
  assertEquals(result.types[0].name, "bare_t");
  assertEquals(result.types[0].fullName, "bare_t");
});

Deno.test("hash is computed", () => {
  const result = parse(`
    package test;
    struct hashed_t {
      int32_t value;
    }
  `);

  const struct = result.types[0];
  // Hash should be non-zero
  assertEquals(struct.hash !== 0n, true);
});

Deno.test("different structs have different hashes", () => {
  const result1 = parse(`package a; struct foo_t { int32_t x; }`);
  const result2 = parse(`package a; struct foo_t { int64_t x; }`);

  assertEquals(result1.types[0].hash !== result2.types[0].hash, true);
});
