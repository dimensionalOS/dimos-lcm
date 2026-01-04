// LCM File Parser

import {
  type LcmConstant,
  type LcmDimension,
  type LcmEnum,
  type LcmEnumValue,
  type LcmFile,
  type LcmMember,
  type LcmStruct,
  type LcmType,
  isPrimitive,
} from "./types.ts";

class Tokenizer {
  private pos = 0;
  private tokens: string[] = [];

  constructor(private source: string) {
    this.tokenize();
  }

  private tokenize(): void {
    const pattern =
      /\/\/[^\n]*|\/\*[\s\S]*?\*\/|"[^"]*"|'[^']*'|[a-zA-Z_][a-zA-Z0-9_]*|0x[0-9a-fA-F]+|[0-9]+\.?[0-9]*(?:[eE][+-]?[0-9]+)?|[{}\[\];,=.]/g;
    let match;
    while ((match = pattern.exec(this.source)) !== null) {
      const token = match[0];
      // Skip comments
      if (token.startsWith("//") || token.startsWith("/*")) continue;
      this.tokens.push(token);
    }
  }

  peek(offset = 0): string | undefined {
    return this.tokens[this.pos + offset];
  }

  next(): string {
    const token = this.tokens[this.pos];
    if (token === undefined) throw new Error("Unexpected end of input");
    this.pos++;
    return token;
  }

  expect(expected: string): void {
    const token = this.next();
    if (token !== expected) {
      throw new Error(`Expected '${expected}', got '${token}'`);
    }
  }

  hasMore(): boolean {
    return this.pos < this.tokens.length;
  }
}

// LCM hash algorithm - matches the C implementation in lcmgen.c
// hash_update: v = ((v << 8) ^ (v >> 55)) + c
// IMPORTANT: C uses int64_t which means arithmetic (signed) right shift
function hashUpdate(v: bigint, c: number): bigint {
  const leftShift = (v << 8n) & 0xffffffffffffffffn;
  // Arithmetic right shift: if MSB is set, fill with 1s
  let rightShift: bigint;
  if (v >= 0x8000000000000000n) {
    // Negative in signed representation - arithmetic shift fills with 1s
    const signed = v - 0x10000000000000000n;
    rightShift = (signed >> 55n) & 0xffffffffffffffffn;
  } else {
    rightShift = v >> 55n;
  }
  return ((leftShift ^ rightShift) + BigInt(c)) & 0xffffffffffffffffn;
}

// hash_string_update: hash the length first, then each character
function hashStringUpdate(v: bigint, s: string): bigint {
  v = hashUpdate(v, s.length);
  for (const char of s) {
    v = hashUpdate(v, char.charCodeAt(0));
  }
  return v;
}

function computeStructHash(struct: LcmStruct, typeMap: Map<string, LcmType>): bigint {
  // Base hash - start with 0x12345678
  let v = 0x12345678n;

  // NOTE: We do NOT include the struct name in the hash
  // This allows renaming types without breaking compatibility

  // Hash each member
  for (const member of struct.members) {
    // Hash the member name
    v = hashStringUpdate(v, member.name);

    // If primitive type, hash the type name
    if (isPrimitive(member.type)) {
      v = hashStringUpdate(v, member.type);
    }
    // For non-primitive types, don't hash the type name here
    // (it will be included in the recursive hash at runtime)

    // Hash dimensionality information
    const ndim = member.dimensions.length;
    v = hashUpdate(v, ndim);

    for (const dim of member.dimensions) {
      // LCM_CONST = 0, LCM_VAR = 1
      const mode = dim.isConstant ? 0 : 1;
      v = hashUpdate(v, mode);
      v = hashStringUpdate(v, dim.size);
    }
  }

  return v;
}

// Note: The recursive hash is computed at RUNTIME in the generated code,
// not at generation time. This is because nested types may be in different
// files that aren't available during parsing. The generator emits a
// _getHashRecursive() method that computes the full hash at runtime.

function computeEnumHash(enumType: LcmEnum): bigint {
  // Enum hash only includes the short name
  let v = 0x87654321n;
  v = hashStringUpdate(v, enumType.name);
  return v;
}

export function parse(source: string): LcmFile {
  const tokenizer = new Tokenizer(source);
  let packageName = "";
  const types: LcmType[] = [];

  while (tokenizer.hasMore()) {
    const token = tokenizer.next();

    if (token === "package") {
      packageName = tokenizer.next();
      tokenizer.expect(";");
    } else if (token === "struct") {
      types.push(parseStruct(tokenizer, packageName));
    } else if (token === "enum") {
      types.push(parseEnum(tokenizer, packageName));
    } else {
      throw new Error(`Unexpected token: ${token}`);
    }
  }

  // Compute hashes
  const typeMap = new Map<string, LcmType>();
  for (const type of types) {
    typeMap.set(type.fullName, type);
  }

  for (const type of types) {
    if (type.kind === "struct") {
      // Store the BASE hash - recursive hash is computed at runtime
      type.hash = computeStructHash(type, typeMap);
    } else {
      type.hash = computeEnumHash(type);
    }
  }

  return { package: packageName, types };
}

function parseStruct(tokenizer: Tokenizer, packageName: string): LcmStruct {
  const name = tokenizer.next();
  const fullName = packageName ? `${packageName}.${name}` : name;
  tokenizer.expect("{");

  const members: LcmMember[] = [];
  const constants: LcmConstant[] = [];

  while (tokenizer.peek() !== "}") {
    if (tokenizer.peek() === "const") {
      tokenizer.next(); // consume 'const'
      parseConstants(tokenizer, constants);
    } else {
      members.push(parseMember(tokenizer));
    }
  }

  tokenizer.expect("}");

  return {
    kind: "struct",
    package: packageName,
    name,
    fullName,
    members,
    constants,
    hash: 0n, // computed later
  };
}

function parseConstants(tokenizer: Tokenizer, constants: LcmConstant[]): void {
  const type = tokenizer.next();

  do {
    const name = tokenizer.next();
    tokenizer.expect("=");

    let value = tokenizer.next();
    // Handle negative numbers
    if (value === "-") {
      value = "-" + tokenizer.next();
    }

    constants.push({ type, name, value });
  } while (tokenizer.peek() === "," && tokenizer.next());

  tokenizer.expect(";");
}

function parseQualifiedName(tokenizer: Tokenizer): string {
  let name = tokenizer.next();
  while (tokenizer.peek() === ".") {
    tokenizer.next(); // consume '.'
    name += "." + tokenizer.next();
  }
  return name;
}

function parseMember(tokenizer: Tokenizer): LcmMember {
  const type = parseQualifiedName(tokenizer);
  const name = tokenizer.next();
  const dimensions: LcmDimension[] = [];

  while (tokenizer.peek() === "[") {
    tokenizer.next(); // consume '['
    const size = tokenizer.next();
    tokenizer.expect("]");

    dimensions.push({
      size,
      isConstant: /^\d+$/.test(size),
    });
  }

  tokenizer.expect(";");

  return { type, name, dimensions };
}

function parseEnum(tokenizer: Tokenizer, packageName: string): LcmEnum {
  const name = tokenizer.next();
  const fullName = packageName ? `${packageName}.${name}` : name;
  tokenizer.expect("{");

  const values: LcmEnumValue[] = [];
  let nextValue = 0;

  while (tokenizer.peek() !== "}") {
    const valueName = tokenizer.next();

    if (tokenizer.peek() === "=") {
      tokenizer.next(); // consume '='
      const valueStr = tokenizer.next();
      nextValue = parseInt(valueStr);
    }

    values.push({ name: valueName, value: nextValue });
    nextValue++;

    if (tokenizer.peek() === ",") {
      tokenizer.next();
    }
  }

  tokenizer.expect("}");

  return {
    kind: "enum",
    package: packageName,
    name,
    fullName,
    values,
    hash: 0n, // computed later
  };
}

export function parseFile(path: string): LcmFile {
  const source = Deno.readTextFileSync(path);
  return parse(source);
}
