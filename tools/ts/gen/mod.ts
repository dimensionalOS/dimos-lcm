#!/usr/bin/env -S deno run --allow-read --allow-write

// LCM TypeScript Code Generator
// Usage: deno run --allow-read --allow-write mod.ts [options] <input.lcm...>

import { parseArgs } from "jsr:@std/cli/parse-args";
import { parseFile } from "./parser.ts";
import { generate, generateToFile } from "./generator.ts";
import type { LcmFile } from "./types.ts";

const args = parseArgs(Deno.args, {
  string: ["output", "o"],
  boolean: ["help", "h", "stdout", "quiet", "q"],
  alias: {
    o: "output",
    h: "help",
    q: "quiet",
  },
  default: {
    output: ".",
  },
});

function printHelp(): void {
  console.log(`lcm-ts - LCM TypeScript Code Generator

Usage:
  lcm-ts [options] <input.lcm...>

Options:
  -o, --output <dir>   Output directory (default: .)
  --stdout             Print to stdout instead of files
  -q, --quiet          Suppress per-file output messages
  -h, --help           Show this help

Examples:
  lcm-ts -o ./generated types/*.lcm
  lcm-ts --stdout example.lcm
`);
}

if (args.help || args._.length === 0) {
  printHelp();
  Deno.exit(args.help ? 0 : 1);
}

// Parse all input files
const files: LcmFile[] = [];
for (const input of args._) {
  const path = String(input);
  try {
    const file = parseFile(path);
    files.push(file);
  } catch (e) {
    console.error(`Error parsing ${path}: ${e}`);
    Deno.exit(1);
  }
}

// Generate output
if (args.stdout) {
  for (const file of files) {
    console.log(generate(file));
  }
} else {
  for (const file of files) {
    generateToFile(file, args.output, args.quiet);
  }
}
