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

function computeStructHash(struct: LcmStruct, typeMap: Map<string, LcmType>): bigint {
  // Base hash from type name and members
  let hash = 0x12345678n;

  // Hash the struct name
  for (const char of struct.fullName) {
    hash = ((hash << 8n) ^ BigInt(char.charCodeAt(0))) & 0xffffffffffffffffn;
  }

  // Hash each member
  for (const member of struct.members) {
    // Hash type name
    for (const char of member.type) {
      hash = ((hash << 8n) ^ BigInt(char.charCodeAt(0))) & 0xffffffffffffffffn;
    }
    // Hash member name
    for (const char of member.name) {
      hash = ((hash << 8n) ^ BigInt(char.charCodeAt(0))) & 0xffffffffffffffffn;
    }
    // Hash dimensions
    for (const dim of member.dimensions) {
      hash = ((hash << 8n) ^ BigInt(dim.isConstant ? 1 : 0)) & 0xffffffffffffffffn;
      if (dim.isConstant) {
        hash = ((hash << 8n) ^ BigInt(parseInt(dim.size))) & 0xffffffffffffffffn;
      }
    }
  }

  // Rotate
  hash = (((hash << 1n) & 0xffffffffffffffffn) + (hash >> 63n)) & 0xffffffffffffffffn;

  return hash;
}

function computeEnumHash(enumType: LcmEnum): bigint {
  let hash = 0x87654321n;

  for (const char of enumType.fullName) {
    hash = ((hash << 8n) ^ BigInt(char.charCodeAt(0))) & 0xffffffffffffffffn;
  }

  for (const value of enumType.values) {
    for (const char of value.name) {
      hash = ((hash << 8n) ^ BigInt(char.charCodeAt(0))) & 0xffffffffffffffffn;
    }
    hash = ((hash << 8n) ^ BigInt(value.value)) & 0xffffffffffffffffn;
  }

  hash = (((hash << 1n) & 0xffffffffffffffffn) + (hash >> 63n)) & 0xffffffffffffffffn;

  return hash;
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
