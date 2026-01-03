// TypeScript Code Generator for LCM types

import {
  type LcmEnum,
  type LcmFile,
  type LcmMember,
  type LcmStruct,
  type LcmType,
  isPrimitive,
} from "./types.ts";

function indent(level: number): string {
  return "  ".repeat(level);
}

function tsType(lcmType: string, forDeclaration = false): string {
  switch (lcmType) {
    case "int8_t":
    case "int16_t":
    case "int32_t":
    case "float":
    case "double":
    case "byte":
      return "number";
    case "int64_t":
      return "bigint";
    case "boolean":
      return "boolean";
    case "string":
      return "string";
    default:
      // Non-primitive type - use the short name
      return lcmType.split(".").pop()!;
  }
}

function memberTsType(member: LcmMember): string {
  let type = tsType(member.type);

  // Handle byte arrays specially - they become Uint8Array
  if (member.type === "byte" && member.dimensions.length > 0) {
    // Only the innermost dimension becomes Uint8Array
    let result = "Uint8Array";
    for (let i = 0; i < member.dimensions.length - 1; i++) {
      result += "[]";
    }
    return result;
  }

  for (const _ of member.dimensions) {
    type += "[]";
  }
  return type;
}

function defaultValue(lcmType: string): string {
  switch (lcmType) {
    case "int8_t":
    case "int16_t":
    case "int32_t":
    case "float":
    case "double":
    case "byte":
      return "0";
    case "int64_t":
      return "0n";
    case "boolean":
      return "false";
    case "string":
      return '""';
    default:
      return `new ${tsType(lcmType)}()`;
  }
}

function primitiveSize(lcmType: string): number {
  switch (lcmType) {
    case "int8_t":
    case "byte":
    case "boolean":
      return 1;
    case "int16_t":
      return 2;
    case "int32_t":
    case "float":
      return 4;
    case "int64_t":
    case "double":
      return 8;
    default:
      return 0;
  }
}

interface TypeDependency {
  shortName: string;
  package: string;
  fullType: string;
}

function collectDependencies(struct: LcmStruct): TypeDependency[] {
  const seen = new Set<string>();
  const deps: TypeDependency[] = [];

  for (const member of struct.members) {
    if (!isPrimitive(member.type) && !seen.has(member.type)) {
      seen.add(member.type);
      const parts = member.type.split(".");
      const shortName = parts.pop()!;
      const pkg = parts.join(".");

      // Don't import self
      if (shortName !== struct.name || pkg !== struct.package) {
        deps.push({ shortName, package: pkg, fullType: member.type });
      }
    }
  }
  return deps;
}

function generateStruct(struct: LcmStruct, allTypes: Map<string, LcmType>): string {
  const lines: string[] = [];
  const className = struct.name;

  // Generate imports for dependencies
  const deps = collectDependencies(struct);
  for (const dep of deps) {
    let importPath: string;
    if (dep.package === struct.package || dep.package === "") {
      // Same package - relative import
      importPath = `./${dep.shortName}.ts`;
    } else {
      // Different package - go up and into the other package
      importPath = `../${dep.package.replace(/\./g, "/")}/${dep.shortName}.ts`;
    }
    lines.push(`import { ${dep.shortName} } from "${importPath}";`);
  }
  if (deps.length > 0) {
    lines.push("");
  }

  // Class declaration
  lines.push(`export class ${className} {`);

  // Static fingerprint (base hash, not including nested types)
  lines.push(`${indent(1)}static readonly _HASH = 0x${struct.hash.toString(16)}n;`);
  lines.push(`${indent(1)}static readonly _NAME = "${struct.fullName}";`);
  lines.push(`${indent(1)}private static _packedFingerprint: bigint | null = null;`);
  lines.push("");

  // Constants
  for (const constant of struct.constants) {
    const value =
      constant.type === "int64_t"
        ? `${constant.value}n`
        : constant.type === "double" || constant.type === "float"
          ? constant.value.includes(".")
            ? constant.value
            : `${constant.value}.0`
          : constant.value;
    lines.push(`${indent(1)}static readonly ${constant.name} = ${value};`);
  }
  if (struct.constants.length > 0) lines.push("");

  // Member declarations
  for (const member of struct.members) {
    lines.push(`${indent(1)}${member.name}: ${memberTsType(member)};`);
  }
  lines.push("");

  // Constructor
  lines.push(`${indent(1)}constructor(init?: Partial<${className}>) {`);
  for (const member of struct.members) {
    const defaultVal = generateDefaultValue(member);
    lines.push(`${indent(2)}this.${member.name} = init?.${member.name} ?? ${defaultVal};`);
  }
  lines.push(`${indent(1)}}`);
  lines.push("");

  // Static decode method
  lines.push(`${indent(1)}static decode(data: Uint8Array): ${className} {`);
  lines.push(`${indent(2)}const view = new DataView(data.buffer, data.byteOffset, data.byteLength);`);
  lines.push(`${indent(2)}let offset = 0;`);
  lines.push("");
  lines.push(`${indent(2)}// Verify fingerprint (recursive hash including nested types)`);
  lines.push(`${indent(2)}const hash = view.getBigUint64(offset, false);`);
  lines.push(`${indent(2)}offset += 8;`);
  lines.push(`${indent(2)}const expectedHash = ${className}._getPackedFingerprint();`);
  lines.push(`${indent(2)}if (hash !== expectedHash) {`);
  lines.push(`${indent(3)}throw new Error(\`Hash mismatch: expected \${expectedHash.toString(16)}, got \${hash.toString(16)}\`);`);
  lines.push(`${indent(2)}}`);
  lines.push("");
  lines.push(`${indent(2)}const result = new ${className}();`);
  lines.push(`${indent(2)}({ offset } = ${className}._decodeOne(view, offset, result));`);
  lines.push(`${indent(2)}return result;`);
  lines.push(`${indent(1)}}`);
  lines.push("");

  // Static _decodeOne method (without fingerprint check, for nested types)
  lines.push(
    `${indent(1)}static _decodeOne(view: DataView, offset: number, target: ${className}): { offset: number } {`
  );
  for (const member of struct.members) {
    generateDecodeOne(lines, member, allTypes, 2);
  }
  lines.push(`${indent(2)}return { offset };`);
  lines.push(`${indent(1)}}`);
  lines.push("");

  // Instance encode method
  lines.push(`${indent(1)}encode(): Uint8Array {`);
  lines.push(`${indent(2)}const size = 8 + this._encodedSize();`);
  lines.push(`${indent(2)}const data = new Uint8Array(size);`);
  lines.push(`${indent(2)}const view = new DataView(data.buffer);`);
  lines.push(`${indent(2)}let offset = 0;`);
  lines.push("");
  lines.push(`${indent(2)}// Write fingerprint (recursive hash including nested types)`);
  lines.push(`${indent(2)}view.setBigUint64(offset, ${className}._getPackedFingerprint(), false);`);
  lines.push(`${indent(2)}offset += 8;`);
  lines.push("");
  lines.push(`${indent(2)}offset = this._encodeOne(view, offset);`);
  lines.push(`${indent(2)}return data;`);
  lines.push(`${indent(1)}}`);
  lines.push("");

  // Instance _encodeOne method (without fingerprint, for nested types)
  lines.push(`${indent(1)}_encodeOne(view: DataView, offset: number): number {`);
  for (const member of struct.members) {
    generateEncodeOne(lines, member, allTypes, 2);
  }
  lines.push(`${indent(2)}return offset;`);
  lines.push(`${indent(1)}}`);
  lines.push("");

  // _encodedSize method
  lines.push(`${indent(1)}_encodedSize(): number {`);
  lines.push(`${indent(2)}let size = 0;`);
  for (const member of struct.members) {
    generateEncodedSize(lines, member, allTypes, 2);
  }
  lines.push(`${indent(2)}return size;`);
  lines.push(`${indent(1)}}`);
  lines.push("");

  // _getHashRecursive method - computes full hash including nested types at runtime
  lines.push(`${indent(1)}// deno-lint-ignore no-explicit-any`);
  lines.push(`${indent(1)}static _getHashRecursive(parents: any[]): bigint {`);
  lines.push(`${indent(2)}if (parents.includes(${className})) return 0n;`);
  lines.push(`${indent(2)}const newparents = [...parents, ${className}];`);

  // Collect non-primitive member types
  const nestedTypes = struct.members
    .filter((m) => !isPrimitive(m.type))
    .map((m) => tsType(m.type));

  if (nestedTypes.length === 0) {
    // No nested types - just return base hash with rotation
    lines.push(`${indent(2)}let tmphash = ${className}._HASH;`);
  } else {
    // Add nested type hashes
    lines.push(`${indent(2)}let tmphash = ${className}._HASH;`);
    for (const nestedType of nestedTypes) {
      lines.push(`${indent(2)}tmphash = (tmphash + ${nestedType}._getHashRecursive(newparents)) & 0xffffffffffffffffn;`);
    }
  }

  // Apply rotation: (hash << 1) + (hash >> 63)
  lines.push(`${indent(2)}tmphash = (((tmphash << 1n) & 0xffffffffffffffffn) + (tmphash >> 63n)) & 0xffffffffffffffffn;`);
  lines.push(`${indent(2)}return tmphash;`);
  lines.push(`${indent(1)}}`);
  lines.push("");

  // _getPackedFingerprint - cached recursive hash
  lines.push(`${indent(1)}static _getPackedFingerprint(): bigint {`);
  lines.push(`${indent(2)}if (${className}._packedFingerprint === null) {`);
  lines.push(`${indent(3)}${className}._packedFingerprint = ${className}._getHashRecursive([]);`);
  lines.push(`${indent(2)}}`);
  lines.push(`${indent(2)}return ${className}._packedFingerprint;`);
  lines.push(`${indent(1)}}`);

  lines.push("}");

  return lines.join("\n");
}

function generateDefaultValue(member: LcmMember): string {
  if (member.dimensions.length === 0) {
    return defaultValue(member.type);
  }

  // For byte arrays, use Uint8Array
  if (member.type === "byte") {
    if (member.dimensions.length === 1) {
      if (member.dimensions[0].isConstant) {
        return `new Uint8Array(${member.dimensions[0].size})`;
      }
      return `new Uint8Array(0)`;
    }
  }

  // For fixed-size arrays, generate nested arrays
  if (member.dimensions[0].isConstant) {
    return generateNestedArray(member, 0);
  }

  return "[]";
}

function generateNestedArray(member: LcmMember, dimIndex: number): string {
  if (dimIndex >= member.dimensions.length) {
    return defaultValue(member.type);
  }

  const dim = member.dimensions[dimIndex];
  if (!dim.isConstant) {
    return "[]";
  }

  // Handle byte arrays specially
  if (member.type === "byte" && dimIndex === member.dimensions.length - 1) {
    return `new Uint8Array(${dim.size})`;
  }

  const inner = generateNestedArray(member, dimIndex + 1);
  return `Array.from({ length: ${dim.size} }, () => ${inner})`;
}

function generateDecodeOne(
  lines: string[],
  member: LcmMember,
  allTypes: Map<string, LcmType>,
  baseIndent: number
): void {
  const ind = (n: number) => indent(baseIndent + n);

  if (member.dimensions.length === 0) {
    // Scalar
    generateDecodePrimitive(lines, member.type, `target.${member.name}`, baseIndent, allTypes);
  } else {
    // Array
    generateDecodeArray(lines, member, allTypes, baseIndent, 0, `target.${member.name}`);
  }
}

function generateDecodePrimitive(
  lines: string[],
  type: string,
  target: string,
  baseIndent: number,
  allTypes: Map<string, LcmType>
): void {
  const ind = (n: number) => indent(baseIndent + n);

  if (isPrimitive(type)) {
    switch (type) {
      case "int8_t":
        lines.push(`${ind(0)}${target} = view.getInt8(offset);`);
        lines.push(`${ind(0)}offset += 1;`);
        break;
      case "byte":
        lines.push(`${ind(0)}${target} = view.getUint8(offset);`);
        lines.push(`${ind(0)}offset += 1;`);
        break;
      case "boolean":
        lines.push(`${ind(0)}${target} = view.getInt8(offset) !== 0;`);
        lines.push(`${ind(0)}offset += 1;`);
        break;
      case "int16_t":
        lines.push(`${ind(0)}${target} = view.getInt16(offset, false);`);
        lines.push(`${ind(0)}offset += 2;`);
        break;
      case "int32_t":
        lines.push(`${ind(0)}${target} = view.getInt32(offset, false);`);
        lines.push(`${ind(0)}offset += 4;`);
        break;
      case "int64_t":
        lines.push(`${ind(0)}${target} = view.getBigInt64(offset, false);`);
        lines.push(`${ind(0)}offset += 8;`);
        break;
      case "float":
        lines.push(`${ind(0)}${target} = view.getFloat32(offset, false);`);
        lines.push(`${ind(0)}offset += 4;`);
        break;
      case "double":
        lines.push(`${ind(0)}${target} = view.getFloat64(offset, false);`);
        lines.push(`${ind(0)}offset += 8;`);
        break;
      case "string":
        lines.push(`${ind(0)}{`);
        lines.push(`${ind(1)}const len = view.getUint32(offset, false);`);
        lines.push(`${ind(1)}offset += 4;`);
        lines.push(
          `${ind(1)}${target} = new TextDecoder().decode(new Uint8Array(view.buffer, view.byteOffset + offset, len - 1));`
        );
        lines.push(`${ind(1)}offset += len;`);
        lines.push(`${ind(0)}}`);
        break;
    }
  } else {
    // Nested struct
    const typeName = tsType(type);
    lines.push(`${ind(0)}${target} = new ${typeName}();`);
    lines.push(`${ind(0)}({ offset } = ${typeName}._decodeOne(view, offset, ${target}));`);
  }
}

function generateDecodeArray(
  lines: string[],
  member: LcmMember,
  allTypes: Map<string, LcmType>,
  baseIndent: number,
  dimIndex: number,
  target: string
): void {
  const ind = (n: number) => indent(baseIndent + n);
  const dim = member.dimensions[dimIndex];
  const isLast = dimIndex === member.dimensions.length - 1;
  const loopVar = `i${dimIndex}`;
  const sizeExpr = dim.isConstant ? dim.size : `target.${dim.size}`;

  // Handle byte arrays specially - use Uint8Array
  if (member.type === "byte" && isLast) {
    lines.push(`${ind(0)}${target} = new Uint8Array(view.buffer, view.byteOffset + offset, ${sizeExpr});`);
    lines.push(`${ind(0)}offset += ${sizeExpr};`);
    return;
  }

  // Initialize array
  lines.push(`${ind(0)}${target} = new Array(${sizeExpr});`);
  lines.push(`${ind(0)}for (let ${loopVar} = 0; ${loopVar} < ${sizeExpr}; ${loopVar}++) {`);

  if (isLast) {
    // Decode element
    generateDecodePrimitive(lines, member.type, `${target}[${loopVar}]`, baseIndent + 1, allTypes);
  } else {
    // Recurse for next dimension
    generateDecodeArray(lines, member, allTypes, baseIndent + 1, dimIndex + 1, `${target}[${loopVar}]`);
  }

  lines.push(`${ind(0)}}`);
}

function generateEncodeOne(
  lines: string[],
  member: LcmMember,
  allTypes: Map<string, LcmType>,
  baseIndent: number
): void {
  if (member.dimensions.length === 0) {
    generateEncodePrimitive(lines, member.type, `this.${member.name}`, baseIndent, allTypes);
  } else {
    generateEncodeArray(lines, member, allTypes, baseIndent, 0, `this.${member.name}`);
  }
}

function generateEncodePrimitive(
  lines: string[],
  type: string,
  source: string,
  baseIndent: number,
  allTypes: Map<string, LcmType>
): void {
  const ind = (n: number) => indent(baseIndent + n);

  if (isPrimitive(type)) {
    switch (type) {
      case "int8_t":
        lines.push(`${ind(0)}view.setInt8(offset, ${source});`);
        lines.push(`${ind(0)}offset += 1;`);
        break;
      case "byte":
        lines.push(`${ind(0)}view.setUint8(offset, ${source});`);
        lines.push(`${ind(0)}offset += 1;`);
        break;
      case "boolean":
        lines.push(`${ind(0)}view.setInt8(offset, ${source} ? 1 : 0);`);
        lines.push(`${ind(0)}offset += 1;`);
        break;
      case "int16_t":
        lines.push(`${ind(0)}view.setInt16(offset, ${source}, false);`);
        lines.push(`${ind(0)}offset += 2;`);
        break;
      case "int32_t":
        lines.push(`${ind(0)}view.setInt32(offset, ${source}, false);`);
        lines.push(`${ind(0)}offset += 4;`);
        break;
      case "int64_t":
        lines.push(`${ind(0)}view.setBigInt64(offset, ${source}, false);`);
        lines.push(`${ind(0)}offset += 8;`);
        break;
      case "float":
        lines.push(`${ind(0)}view.setFloat32(offset, ${source}, false);`);
        lines.push(`${ind(0)}offset += 4;`);
        break;
      case "double":
        lines.push(`${ind(0)}view.setFloat64(offset, ${source}, false);`);
        lines.push(`${ind(0)}offset += 8;`);
        break;
      case "string":
        lines.push(`${ind(0)}{`);
        lines.push(`${ind(1)}const encoded = new TextEncoder().encode(${source});`);
        lines.push(`${ind(1)}view.setUint32(offset, encoded.length + 1, false);`);
        lines.push(`${ind(1)}offset += 4;`);
        lines.push(`${ind(1)}new Uint8Array(view.buffer, view.byteOffset + offset).set(encoded);`);
        lines.push(`${ind(1)}offset += encoded.length;`);
        lines.push(`${ind(1)}view.setUint8(offset, 0); // null terminator`);
        lines.push(`${ind(1)}offset += 1;`);
        lines.push(`${ind(0)}}`);
        break;
    }
  } else {
    const typeName = tsType(type);
    lines.push(`${ind(0)}offset = ${source}._encodeOne(view, offset);`);
  }
}

function generateEncodeArray(
  lines: string[],
  member: LcmMember,
  allTypes: Map<string, LcmType>,
  baseIndent: number,
  dimIndex: number,
  source: string
): void {
  const ind = (n: number) => indent(baseIndent + n);
  const dim = member.dimensions[dimIndex];
  const isLast = dimIndex === member.dimensions.length - 1;
  const loopVar = `i${dimIndex}`;
  const sizeExpr = dim.isConstant ? dim.size : `this.${dim.size}`;

  // Handle byte arrays specially
  if (member.type === "byte" && isLast) {
    lines.push(`${ind(0)}new Uint8Array(view.buffer, view.byteOffset + offset).set(${source}.subarray(0, ${sizeExpr}));`);
    lines.push(`${ind(0)}offset += ${sizeExpr};`);
    return;
  }

  lines.push(`${ind(0)}for (let ${loopVar} = 0; ${loopVar} < ${sizeExpr}; ${loopVar}++) {`);

  if (isLast) {
    generateEncodePrimitive(lines, member.type, `${source}[${loopVar}]`, baseIndent + 1, allTypes);
  } else {
    generateEncodeArray(lines, member, allTypes, baseIndent + 1, dimIndex + 1, `${source}[${loopVar}]`);
  }

  lines.push(`${ind(0)}}`);
}

function generateEncodedSize(
  lines: string[],
  member: LcmMember,
  allTypes: Map<string, LcmType>,
  baseIndent: number
): void {
  const ind = (n: number) => indent(baseIndent + n);

  if (member.dimensions.length === 0) {
    // Scalar
    if (isPrimitive(member.type)) {
      if (member.type === "string") {
        lines.push(`${ind(0)}size += 4 + new TextEncoder().encode(this.${member.name}).length + 1;`);
      } else {
        lines.push(`${ind(0)}size += ${primitiveSize(member.type)};`);
      }
    } else {
      lines.push(`${ind(0)}size += this.${member.name}._encodedSize();`);
    }
  } else {
    // Array
    generateArraySize(lines, member, allTypes, baseIndent, 0, `this.${member.name}`);
  }
}

function generateArraySize(
  lines: string[],
  member: LcmMember,
  allTypes: Map<string, LcmType>,
  baseIndent: number,
  dimIndex: number,
  source: string
): void {
  const ind = (n: number) => indent(baseIndent + n);
  const dim = member.dimensions[dimIndex];
  const isLast = dimIndex === member.dimensions.length - 1;
  const sizeExpr = dim.isConstant ? dim.size : `this.${dim.size}`;

  if (isLast) {
    if (isPrimitive(member.type)) {
      if (member.type === "string") {
        const loopVar = `i${dimIndex}`;
        lines.push(`${ind(0)}for (let ${loopVar} = 0; ${loopVar} < ${sizeExpr}; ${loopVar}++) {`);
        lines.push(`${ind(1)}size += 4 + new TextEncoder().encode(${source}[${loopVar}]).length + 1;`);
        lines.push(`${ind(0)}}`);
      } else {
        lines.push(`${ind(0)}size += ${sizeExpr} * ${primitiveSize(member.type)};`);
      }
    } else {
      const loopVar = `i${dimIndex}`;
      lines.push(`${ind(0)}for (let ${loopVar} = 0; ${loopVar} < ${sizeExpr}; ${loopVar}++) {`);
      lines.push(`${ind(1)}size += ${source}[${loopVar}]._encodedSize();`);
      lines.push(`${ind(0)}}`);
    }
  } else {
    const loopVar = `i${dimIndex}`;
    lines.push(`${ind(0)}for (let ${loopVar} = 0; ${loopVar} < ${sizeExpr}; ${loopVar}++) {`);
    generateArraySize(lines, member, allTypes, baseIndent + 1, dimIndex + 1, `${source}[${loopVar}]`);
    lines.push(`${ind(0)}}`);
  }
}

function generateEnum(enumType: LcmEnum): string {
  const lines: string[] = [];

  // Export const enum for the values
  lines.push(`export const ${enumType.name} = {`);
  for (const value of enumType.values) {
    lines.push(`${indent(1)}${value.name}: ${value.value},`);
  }
  lines.push("} as const;");
  lines.push("");

  // Type for the enum values
  lines.push(`export type ${enumType.name}Value = (typeof ${enumType.name})[keyof typeof ${enumType.name}];`);
  lines.push("");

  // Wrapper class for encoding/decoding
  lines.push(`export class ${enumType.name}Type {`);
  lines.push(`${indent(1)}static readonly _HASH = 0x${enumType.hash.toString(16)}n;`);
  lines.push(`${indent(1)}static readonly _NAME = "${enumType.fullName}";`);
  lines.push(`${indent(1)}value: ${enumType.name}Value;`);
  lines.push("");
  lines.push(`${indent(1)}constructor(value: ${enumType.name}Value = ${enumType.values[0]?.value ?? 0}) {`);
  lines.push(`${indent(2)}this.value = value;`);
  lines.push(`${indent(1)}}`);
  lines.push("");
  lines.push(`${indent(1)}static decode(data: Uint8Array): ${enumType.name}Type {`);
  lines.push(`${indent(2)}const view = new DataView(data.buffer, data.byteOffset, data.byteLength);`);
  lines.push(`${indent(2)}const hash = view.getBigUint64(0, false);`);
  lines.push(`${indent(2)}if (hash !== ${enumType.name}Type._HASH) {`);
  lines.push(`${indent(3)}throw new Error("Hash mismatch");`);
  lines.push(`${indent(2)}}`);
  lines.push(`${indent(2)}return new ${enumType.name}Type(view.getInt32(8, false) as ${enumType.name}Value);`);
  lines.push(`${indent(1)}}`);
  lines.push("");
  lines.push(`${indent(1)}encode(): Uint8Array {`);
  lines.push(`${indent(2)}const data = new Uint8Array(12);`);
  lines.push(`${indent(2)}const view = new DataView(data.buffer);`);
  lines.push(`${indent(2)}view.setBigUint64(0, ${enumType.name}Type._HASH, false);`);
  lines.push(`${indent(2)}view.setInt32(8, this.value, false);`);
  lines.push(`${indent(2)}return data;`);
  lines.push(`${indent(1)}}`);
  lines.push("}");

  return lines.join("\n");
}

export function generate(file: LcmFile): string {
  const lines: string[] = [];

  lines.push("// Auto-generated by lcm-ts. DO NOT EDIT.");
  lines.push("");

  // Build type map for resolving nested types
  const allTypes = new Map<string, LcmType>();
  for (const type of file.types) {
    allTypes.set(type.fullName, type);
    allTypes.set(type.name, type);
  }

  // Generate imports for cross-package dependencies (would need to be handled separately)

  // Generate each type
  for (const type of file.types) {
    if (type.kind === "struct") {
      lines.push(generateStruct(type, allTypes));
    } else {
      lines.push(generateEnum(type));
    }
    lines.push("");
  }

  return lines.join("\n");
}

export function generateToFile(lcmFile: LcmFile, outDir: string, quiet = false): void {
  // Create output directory if needed
  const packagePath = lcmFile.package.replace(/\./g, "/");
  const fullOutDir = packagePath ? `${outDir}/${packagePath}` : outDir;

  Deno.mkdirSync(fullOutDir, { recursive: true });

  // Write one file per type
  for (const type of lcmFile.types) {
    const typeOutput = generate({ package: lcmFile.package, types: [type] });
    const outPath = `${fullOutDir}/${type.name}.ts`;
    Deno.writeTextFileSync(outPath, typeOutput);
    if (!quiet) {
      console.log(`Generated: ${outPath}`);
    }
  }
}
