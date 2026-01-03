import { assertEquals, assertStringIncludes } from "jsr:@std/assert";
import { parse } from "./parser.ts";
import { generate } from "./generator.ts";

Deno.test("generate simple struct", () => {
  const lcm = parse(`
    package test;
    struct simple_t {
      int32_t value;
      string name;
    }
  `);

  const output = generate(lcm);

  assertStringIncludes(output, "export class simple_t");
  assertStringIncludes(output, "value: number");
  assertStringIncludes(output, "name: string");
  assertStringIncludes(output, "static readonly _HASH");
  assertStringIncludes(output, "static decode(data: Uint8Array)");
  assertStringIncludes(output, "encode(): Uint8Array");
});

Deno.test("generate int64 as bigint", () => {
  const lcm = parse(`
    package test;
    struct bigint_t {
      int64_t timestamp;
    }
  `);

  const output = generate(lcm);

  assertStringIncludes(output, "timestamp: bigint");
  assertStringIncludes(output, "getBigInt64");
  assertStringIncludes(output, "setBigInt64");
});

Deno.test("generate fixed array", () => {
  const lcm = parse(`
    package test;
    struct array_t {
      double position[3];
    }
  `);

  const output = generate(lcm);

  assertStringIncludes(output, "position: number[]");
  assertStringIncludes(output, "Array.from({ length: 3 }");
  assertStringIncludes(output, "for (let i0 = 0; i0 < 3; i0++)");
});

Deno.test("generate dynamic array", () => {
  const lcm = parse(`
    package test;
    struct dynamic_t {
      int32_t count;
      int16_t values[count];
    }
  `);

  const output = generate(lcm);

  assertStringIncludes(output, "values: number[]");
  assertStringIncludes(output, "target.count");
  assertStringIncludes(output, "this.count");
});

Deno.test("generate byte array as Uint8Array", () => {
  const lcm = parse(`
    package test;
    struct bytes_t {
      int32_t len;
      byte data[len];
    }
  `);

  const output = generate(lcm);

  assertStringIncludes(output, "data: Uint8Array");
});

Deno.test("generate constants", () => {
  const lcm = parse(`
    package test;
    struct consts_t {
      const int32_t FOO = 42;
      const int64_t BAR = 123;
      const double PI = 3.14;
    }
  `);

  const output = generate(lcm);

  assertStringIncludes(output, "static readonly FOO = 42");
  assertStringIncludes(output, "static readonly BAR = 123n");
  assertStringIncludes(output, "static readonly PI = 3.14");
});

Deno.test("generate nested struct", () => {
  const lcm = parse(`
    package test;
    struct inner_t {
      int32_t x;
    }
    struct outer_t {
      inner_t nested;
    }
  `);

  const output = generate({ package: lcm.package, types: [lcm.types[1]] });

  assertStringIncludes(output, "nested: inner_t");
  assertStringIncludes(output, "new inner_t()");
  assertStringIncludes(output, "inner_t._decodeOne");
});

Deno.test("generate enum", () => {
  const lcm = parse(`
    package test;
    enum status_t {
      OK,
      ERROR = 5,
      DONE
    }
  `);

  const output = generate(lcm);

  assertStringIncludes(output, "export const status_t = {");
  assertStringIncludes(output, "OK: 0");
  assertStringIncludes(output, "ERROR: 5");
  assertStringIncludes(output, "DONE: 6");
  assertStringIncludes(output, "status_tType");
});

Deno.test("generate multidimensional array", () => {
  const lcm = parse(`
    package test;
    struct matrix_t {
      int32_t rows;
      int32_t cols;
      double data[rows][cols];
    }
  `);

  const output = generate(lcm);

  assertStringIncludes(output, "data: number[][]");
  assertStringIncludes(output, "for (let i0 = 0; i0 < target.rows; i0++)");
  assertStringIncludes(output, "for (let i1 = 0; i1 < target.cols; i1++)");
});

Deno.test("generated code is syntactically valid TypeScript", async () => {
  const lcm = parse(`
    package test;
    struct example_t {
      int64_t timestamp;
      double position[3];
      int32_t num_ranges;
      int16_t ranges[num_ranges];
      string name;
      boolean enabled;
    }
  `);

  const output = generate(lcm);

  // Write to temp file and type-check
  const tempFile = await Deno.makeTempFile({ suffix: ".ts" });
  try {
    await Deno.writeTextFile(tempFile, output);

    const command = new Deno.Command("deno", {
      args: ["check", tempFile],
      stderr: "piped",
      stdout: "piped",
    });

    const { code, stderr } = await command.output();
    if (code !== 0) {
      const errorText = new TextDecoder().decode(stderr);
      throw new Error(`Type check failed:\n${errorText}\n\nGenerated code:\n${output}`);
    }
  } finally {
    await Deno.remove(tempFile);
  }
});

Deno.test("encode/decode roundtrip for simple struct", async () => {
  const lcm = parse(`
    package test;
    struct roundtrip_t {
      int32_t x;
      int64_t y;
      double z;
      string s;
      boolean b;
    }
  `);

  const output = generate(lcm);

  // Create a test script that imports and tests the generated code
  const testScript = `
    ${output}

    const original = new roundtrip_t({
      x: 42,
      y: 123456789012345n,
      z: 3.14159,
      s: "hello world",
      b: true,
    });

    const encoded = original.encode();
    const decoded = roundtrip_t.decode(encoded);

    if (decoded.x !== original.x) throw new Error("x mismatch");
    if (decoded.y !== original.y) throw new Error("y mismatch");
    if (Math.abs(decoded.z - original.z) > 0.0001) throw new Error("z mismatch");
    if (decoded.s !== original.s) throw new Error("s mismatch");
    if (decoded.b !== original.b) throw new Error("b mismatch");

    console.log("Roundtrip test passed!");
  `;

  const tempFile = await Deno.makeTempFile({ suffix: ".ts" });
  try {
    await Deno.writeTextFile(tempFile, testScript);

    const command = new Deno.Command("deno", {
      args: ["run", tempFile],
      stderr: "piped",
      stdout: "piped",
    });

    const { code, stderr, stdout } = await command.output();
    if (code !== 0) {
      const errorText = new TextDecoder().decode(stderr);
      throw new Error(`Roundtrip test failed:\n${errorText}`);
    }

    const outputText = new TextDecoder().decode(stdout);
    assertStringIncludes(outputText, "Roundtrip test passed!");
  } finally {
    await Deno.remove(tempFile);
  }
});

Deno.test("encode/decode roundtrip for arrays", async () => {
  const lcm = parse(`
    package test;
    struct array_roundtrip_t {
      double fixed[3];
      int32_t count;
      int16_t dynamic[count];
    }
  `);

  const output = generate(lcm);

  const testScript = `
    ${output}

    const original = new array_roundtrip_t({
      fixed: [1.0, 2.0, 3.0],
      count: 4,
      dynamic: [10, 20, 30, 40],
    });

    const encoded = original.encode();
    const decoded = array_roundtrip_t.decode(encoded);

    if (decoded.fixed.length !== 3) throw new Error("fixed length mismatch");
    if (Math.abs(decoded.fixed[0] - 1.0) > 0.0001) throw new Error("fixed[0] mismatch");
    if (Math.abs(decoded.fixed[1] - 2.0) > 0.0001) throw new Error("fixed[1] mismatch");
    if (Math.abs(decoded.fixed[2] - 3.0) > 0.0001) throw new Error("fixed[2] mismatch");

    if (decoded.count !== 4) throw new Error("count mismatch");
    if (decoded.dynamic.length !== 4) throw new Error("dynamic length mismatch");
    if (decoded.dynamic[0] !== 10) throw new Error("dynamic[0] mismatch");
    if (decoded.dynamic[3] !== 40) throw new Error("dynamic[3] mismatch");

    console.log("Array roundtrip test passed!");
  `;

  const tempFile = await Deno.makeTempFile({ suffix: ".ts" });
  try {
    await Deno.writeTextFile(tempFile, testScript);

    const command = new Deno.Command("deno", {
      args: ["run", tempFile],
      stderr: "piped",
      stdout: "piped",
    });

    const { code, stderr, stdout } = await command.output();
    if (code !== 0) {
      const errorText = new TextDecoder().decode(stderr);
      throw new Error(`Array roundtrip test failed:\n${errorText}`);
    }

    const outputText = new TextDecoder().decode(stdout);
    assertStringIncludes(outputText, "Array roundtrip test passed!");
  } finally {
    await Deno.remove(tempFile);
  }
});
