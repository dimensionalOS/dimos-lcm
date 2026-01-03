// LCM AST Types

export interface LcmDimension {
  size: string;
  isConstant: boolean; // true if numeric literal, false if refers to a field
}

export interface LcmMember {
  type: string;
  name: string;
  dimensions: LcmDimension[];
  comment?: string;
}

export interface LcmConstant {
  type: string;
  name: string;
  value: string;
}

export interface LcmStruct {
  kind: "struct";
  package: string;
  name: string;
  fullName: string;
  members: LcmMember[];
  constants: LcmConstant[];
  hash: bigint;
  comment?: string;
}

export interface LcmEnumValue {
  name: string;
  value: number;
}

export interface LcmEnum {
  kind: "enum";
  package: string;
  name: string;
  fullName: string;
  values: LcmEnumValue[];
  hash: bigint;
  comment?: string;
}

export type LcmType = LcmStruct | LcmEnum;

export interface LcmFile {
  package: string;
  types: LcmType[];
}

export const LCM_PRIMITIVES = [
  "int8_t",
  "int16_t",
  "int32_t",
  "int64_t",
  "float",
  "double",
  "string",
  "boolean",
  "byte",
] as const;

export type LcmPrimitive = (typeof LCM_PRIMITIVES)[number];

export function isPrimitive(type: string): type is LcmPrimitive {
  return LCM_PRIMITIVES.includes(type as LcmPrimitive);
}
