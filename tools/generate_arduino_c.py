#!/usr/bin/env python3
"""
generate_arduino_c.py — Generate Arduino-compatible C headers from .lcm files.

Reads .lcm type definitions and emits lightweight C headers with:
  - typedef struct (no dynamic allocation)
  - encoded_size()  (compile-time constant)
  - encode()        (big-endian, LCM wire format without fingerprint)
  - decode()
  - LCM fingerprint hash constant (matching C++ getHash())
  - dimos_lcm_type_t type descriptor for the pubsub layer

Only fixed-size types are supported (no strings, no variable-length arrays).
Types with unsupported fields are skipped with a warning.
"""

import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# LCM primitive types → (C type, encoder prefix, wire size in bytes)
PRIMITIVE_MAP = {
    "boolean":  ("int8_t",  "int8_t",  1),
    "byte":     ("uint8_t", "byte",    1),
    "int8_t":   ("int8_t",  "int8_t",  1),
    "int16_t":  ("int16_t", "int16_t", 2),
    "int32_t":  ("int32_t", "int32_t", 4),
    "int64_t":  ("int64_t", "int64_t", 8),
    "float":    ("float",   "float",   4),
    "double":   ("double",  "double",  8),
}

# Field name overrides: (package, struct, lcm_field) → arduino_field
# Used when the dimos4 hand-written headers use different names than the LCM defs
FIELD_NAME_OVERRIDES = {
    ("builtin_interfaces", "Time", "nanosec"): "nsec",
}


@dataclass
class LcmField:
    name: str
    type_name: str       # e.g. "double", "int32_t", "Vector3", "geometry_msgs.Vector3"
    array_size: int = 0  # 0 = scalar, >0 = fixed array, -1 = variable-length


@dataclass
class LcmStruct:
    package: str
    name: str
    fields: list[LcmField] = field(default_factory=list)
    constants: list[tuple[str, str, str]] = field(default_factory=list)  # (type, name, value)


def parse_lcm_file(path: Path) -> LcmStruct | None:
    """Parse a single .lcm file into an LcmStruct."""
    text = path.read_text()

    pkg_match = re.search(r"package\s+([\w.]+)\s*;", text)
    if not pkg_match:
        return None
    package = pkg_match.group(1)

    struct_match = re.search(r"struct\s+(\w+)\s*\{([^}]*)\}", text, re.DOTALL)
    if not struct_match:
        return None
    name = struct_match.group(1)
    body = struct_match.group(2)

    s = LcmStruct(package=package, name=name)

    for line in body.strip().splitlines():
        line = line.strip().rstrip(";").strip()
        if not line or line.startswith("//"):
            continue

        # Constants: const int8_t NAME = VALUE
        const_match = re.match(r"const\s+(\S+)\s+(\w+)\s*=\s*(.+)", line)
        if const_match:
            s.constants.append((const_match.group(1), const_match.group(2), const_match.group(3).strip()))
            continue

        # Fields: type name  OR  type name[size]
        # Variable-length dimension fields (e.g. "int32_t foo_length") are kept;
        # the field they dimension will be marked variable-length.
        arr_match = re.match(r"(\S+)\s+(\w+)\[(\w+)\]", line)
        if arr_match:
            type_name = arr_match.group(1)
            field_name = arr_match.group(2)
            size_str = arr_match.group(3)
            try:
                array_size = int(size_str)
            except ValueError:
                # Variable-length array (size is a field name) — not supported
                array_size = -1
            s.fields.append(LcmField(name=field_name, type_name=type_name, array_size=array_size))
            continue

        parts = line.split()
        if len(parts) == 2:
            s.fields.append(LcmField(name=parts[1], type_name=parts[0]))

    return s


def resolve_type(type_name: str, current_package: str) -> tuple[str, str | None]:
    """Resolve a type name to (simple_name, package_or_None).

    Returns (simple_name, None) for primitives, (simple_name, package) for structs.
    """
    if type_name in PRIMITIVE_MAP:
        return type_name, None

    # Fully qualified: geometry_msgs.Vector3
    if "." in type_name:
        pkg, name = type_name.rsplit(".", 1)
        return name, pkg

    # Unqualified struct in same package
    return type_name, current_package


def is_arduino_compatible(struct: LcmStruct, all_structs: dict[tuple[str, str], LcmStruct]) -> bool:
    """Check if a struct can be generated for Arduino (fixed-size, no strings)."""
    for f in struct.fields:
        if f.type_name == "string":
            return False
        if f.array_size == -1:  # variable-length
            return False
        simple, pkg = resolve_type(f.type_name, struct.package)
        if pkg is not None:
            dep = all_structs.get((pkg, simple))
            if dep is None or not is_arduino_compatible(dep, all_structs):
                return False
    return True


def wire_size(struct: LcmStruct, all_structs: dict[tuple[str, str], LcmStruct]) -> int:
    """Compute total wire size in bytes for a fixed-size struct."""
    total = 0
    for f in struct.fields:
        if f.type_name in PRIMITIVE_MAP:
            sz = PRIMITIVE_MAP[f.type_name][2]
        else:
            simple, pkg = resolve_type(f.type_name, struct.package)
            dep = all_structs[(pkg, simple)]
            sz = wire_size(dep, all_structs)

        if f.array_size > 0:
            sz *= f.array_size
        total += sz
    return total


def c_field_name(pkg: str, struct_name: str, field_name: str) -> str:
    """Apply field name overrides."""
    return FIELD_NAME_OVERRIDES.get((pkg, struct_name, field_name), field_name)


def generate_header(
    struct: LcmStruct,
    all_structs: dict[tuple[str, str], LcmStruct],
    fingerprints: dict[str, int] | None = None,
) -> str:
    """Generate the full C header for one struct."""
    pkg = struct.package
    name = struct.name
    prefix = f"dimos_msg__{name}"
    guard = f"DIMOS_ARDUINO_MSG_{name.upper()}_H"
    total_size = wire_size(struct, all_structs)

    # Determine includes
    includes: list[str] = []
    has_primitive_only = True
    deps_seen: set[tuple[str, str]] = set()
    for f in struct.fields:
        simple, fpkg = resolve_type(f.type_name, pkg)
        if fpkg is not None:
            has_primitive_only = False
            if (fpkg, simple) not in deps_seen:
                deps_seen.add((fpkg, simple))
                includes.append(f'#include "{fpkg}/{simple}.h"')

    if has_primitive_only:
        includes.append('#include "lcm_coretypes_arduino.h"')

    # Build wire format comment
    field_descs = []
    for f in struct.fields:
        fname = c_field_name(pkg, name, f.name)
        if f.type_name in PRIMITIVE_MAP:
            _, _, sz = PRIMITIVE_MAP[f.type_name]
            if f.array_size > 0:
                field_descs.append(f"{f.array_size}x {f.type_name}({sz * f.array_size})")
            else:
                field_descs.append(f"{f.type_name}")
        else:
            simple, fpkg = resolve_type(f.type_name, pkg)
            dep = all_structs[(fpkg, simple)]
            dsz = wire_size(dep, all_structs)
            if f.array_size > 0:
                field_descs.append(f"{f.array_size}x {simple}({dsz * f.array_size})")
            else:
                field_descs.append(f"{simple}({dsz})")

    wire_comment = " + ".join(field_descs) + f" = {total_size} bytes"

    lines = []
    lines.append(f"/*")
    lines.append(f" * {pkg}/{name} — Arduino-compatible LCM C encode/decode.")
    lines.append(f" * Wire format: {wire_comment}.")
    lines.append(f" */")
    lines.append(f"#ifndef {guard}")
    lines.append(f"#define {guard}")
    lines.append(f"")
    for inc in includes:
        lines.append(inc)
    lines.append(f"")
    lines.append(f"#ifdef __cplusplus")
    lines.append(f'extern "C" {{')
    lines.append(f"#endif")
    lines.append(f"")

    # Struct definition
    lines.append(f"typedef struct {{")
    for f in struct.fields:
        fname = c_field_name(pkg, name, f.name)
        if f.type_name in PRIMITIVE_MAP:
            ctype = PRIMITIVE_MAP[f.type_name][0]
        else:
            simple, fpkg = resolve_type(f.type_name, pkg)
            ctype = f"dimos_msg__{simple}"

        if f.array_size > 0:
            lines.append(f"    {ctype} {fname}[{f.array_size}];")
        else:
            lines.append(f"    {ctype} {fname};")
    lines.append(f"}} {prefix};")
    lines.append(f"")

    # encoded_size
    lines.append(f"static inline int {prefix}__encoded_size(void) {{ return {total_size}; }}")
    lines.append(f"")

    # encode
    lines.append(f"static inline int {prefix}__encode(void *buf, int offset, int maxlen,")
    lines.append(f"    const {prefix} *p)")
    lines.append(f"{{")

    if len(struct.fields) == 1 and struct.fields[0].array_size == 0:
        # Single-field shortcut (like Bool, Int32, Float32, Float64)
        f = struct.fields[0]
        fname = c_field_name(pkg, name, f.name)
        if f.type_name in PRIMITIVE_MAP:
            enc_prefix = PRIMITIVE_MAP[f.type_name][1]
            lines.append(f"    return __{enc_prefix}_encode_array(buf, offset, maxlen, &p->{fname}, 1);")
        else:
            simple, fpkg = resolve_type(f.type_name, pkg)
            lines.append(f"    return dimos_msg__{simple}__encode(buf, offset, maxlen, &p->{fname});")
    else:
        lines.append(f"    int pos = 0, thislen;")
        for f in struct.fields:
            fname = c_field_name(pkg, name, f.name)
            if f.type_name in PRIMITIVE_MAP:
                enc_prefix = PRIMITIVE_MAP[f.type_name][1]
                if f.array_size > 0:
                    lines.append(f"    thislen = __{enc_prefix}_encode_array(buf, offset + pos, maxlen - pos, p->{fname}, {f.array_size});")
                else:
                    lines.append(f"    thislen = __{enc_prefix}_encode_array(buf, offset + pos, maxlen - pos, &p->{fname}, 1);")
            else:
                simple, fpkg = resolve_type(f.type_name, pkg)
                if f.array_size > 0:
                    # Array of structs — encode each element
                    lines.append(f"    for (int _i = 0; _i < {f.array_size}; _i++) {{")
                    lines.append(f"        thislen = dimos_msg__{simple}__encode(buf, offset + pos, maxlen - pos, &p->{fname}[_i]);")
                    lines.append(f"        if (thislen < 0) return thislen; pos += thislen;")
                    lines.append(f"    }}")
                    continue
                else:
                    lines.append(f"    thislen = dimos_msg__{simple}__encode(buf, offset + pos, maxlen - pos, &p->{fname});")
            lines.append(f"    if (thislen < 0) return thislen; pos += thislen;")
        lines.append(f"    return pos;")
    lines.append(f"}}")
    lines.append(f"")

    # decode
    lines.append(f"static inline int {prefix}__decode(const void *buf, int offset,")
    lines.append(f"    int maxlen, {prefix} *p)")
    lines.append(f"{{")

    if len(struct.fields) == 1 and struct.fields[0].array_size == 0:
        f = struct.fields[0]
        fname = c_field_name(pkg, name, f.name)
        if f.type_name in PRIMITIVE_MAP:
            enc_prefix = PRIMITIVE_MAP[f.type_name][1]
            lines.append(f"    return __{enc_prefix}_decode_array(buf, offset, maxlen, &p->{fname}, 1);")
        else:
            simple, fpkg = resolve_type(f.type_name, pkg)
            lines.append(f"    return dimos_msg__{simple}__decode(buf, offset, maxlen, &p->{fname});")
    else:
        lines.append(f"    int pos = 0, thislen;")
        for f in struct.fields:
            fname = c_field_name(pkg, name, f.name)
            if f.type_name in PRIMITIVE_MAP:
                enc_prefix = PRIMITIVE_MAP[f.type_name][1]
                if f.array_size > 0:
                    lines.append(f"    thislen = __{enc_prefix}_decode_array(buf, offset + pos, maxlen - pos, p->{fname}, {f.array_size});")
                else:
                    lines.append(f"    thislen = __{enc_prefix}_decode_array(buf, offset + pos, maxlen - pos, &p->{fname}, 1);")
            else:
                simple, fpkg = resolve_type(f.type_name, pkg)
                if f.array_size > 0:
                    lines.append(f"    for (int _i = 0; _i < {f.array_size}; _i++) {{")
                    lines.append(f"        thislen = dimos_msg__{simple}__decode(buf, offset + pos, maxlen - pos, &p->{fname}[_i]);")
                    lines.append(f"        if (thislen < 0) return thislen; pos += thislen;")
                    lines.append(f"    }}")
                    continue
                else:
                    lines.append(f"    thislen = dimos_msg__{simple}__decode(buf, offset + pos, maxlen - pos, &p->{fname});")
            lines.append(f"    if (thislen < 0) return thislen; pos += thislen;")
        lines.append(f"    return pos;")
    lines.append(f"}}")
    lines.append(f"")

    # LCM fingerprint hash constant
    fq_name = f"{pkg}.{name}"
    fp_val = fingerprints.get(fq_name, 0) if fingerprints else 0
    # Convert to signed int64_t for C (matching C++ getHash() return type)
    if fp_val >= 0x8000000000000000:
        signed_fp = fp_val - 0x10000000000000000
    else:
        signed_fp = fp_val

    lines.append(f"/* LCM fingerprint hash — matches C++ {name}::getHash() */")
    lines.append(f"static inline int64_t {prefix}__fingerprint(void) {{")
    lines.append(f"    return (int64_t){signed_fp}LL;")
    lines.append(f"}}")
    lines.append(f"")

    # Type descriptor for the pubsub layer (requires dimos_lcm_pubsub.h)
    lines.append(f"/* Type descriptor for dimos_lcm_pubsub — include dimos_lcm_pubsub.h first */")
    lines.append(f"#ifdef DIMOS_LCM_PUBSUB_H")
    lines.append(f"static const dimos_lcm_type_t {prefix}__type = {{")
    lines.append(f'    /* name */          "{fq_name}",')
    lines.append(f"    /* fingerprint */   (int64_t){signed_fp}LL,")
    lines.append(f"    /* encoded_size */  {total_size},")
    lines.append(f"    /* decode */        (int (*)(const void *, int, int, void *)){prefix}__decode")
    lines.append(f"}};")
    lines.append(f"#endif")
    lines.append(f"")

    lines.append(f"#ifdef __cplusplus")
    lines.append(f"}}")
    lines.append(f"#endif")
    lines.append(f"")
    lines.append(f"#endif")
    lines.append(f"")

    return "\n".join(lines)


def extract_base_hashes(cpp_dir: Path) -> dict[str, dict]:
    """Extract base hash constants and dependencies from generated C++ headers.

    Returns a dict keyed by "package.TypeName" with:
      - 'base': uint64_t base hash constant
      - 'deps': list of "package.TypeName" dependencies (in order)
    """
    import glob as _glob
    result = {}
    for f in sorted(_glob.glob(str(cpp_dir / "*" / "*.hpp"))):
        type_name = f.replace(str(cpp_dir) + "/", "").replace(".hpp", "").replace("/", ".")
        text = open(f).read()

        short_name = type_name.split(".")[-1]
        idx = text.find(short_name + "::_computeHash(")
        if idx < 0:
            continue

        # Find function body by brace matching
        brace_start = text.find("{", idx)
        if brace_start < 0:
            continue
        depth = 0
        end = brace_start
        for i in range(brace_start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            if depth == 0:
                end = i
                break
        body = text[brace_start : end + 1]

        base_m = re.search(r"(0x[0-9a-fA-F]+)LL", body)
        if base_m is None:
            continue
        base = int(base_m.group(1), 16)

        deps = re.findall(r"(\w+)::(\w+)::_computeHash", body)
        dep_list = [f"{ns}.{cls}" for ns, cls in deps]

        result[type_name] = {"base": base, "deps": dep_list}
    return result


def compute_fingerprints(
    hash_info: dict[str, dict],
) -> dict[str, int]:
    """Compute LCM fingerprint hashes matching C++ getHash() output.

    Returns dict of "package.TypeName" -> uint64_t hash value.
    """
    computed: dict[str, int] = {}

    def _compute(type_name: str, visited: set[str] | None = None) -> int:
        if type_name in computed:
            return computed[type_name]
        if visited is None:
            visited = set()
        if type_name in visited:
            return 0  # cycle detection (matches C++ linked-list check)
        visited = visited | {type_name}

        info = hash_info.get(type_name)
        if info is None:
            return 0

        h = info["base"]
        for dep in info["deps"]:
            h = (h + _compute(dep, visited)) & 0xFFFFFFFFFFFFFFFF
        h = ((h << 1) | (h >> 63)) & 0xFFFFFFFFFFFFFFFF

        computed[type_name] = h
        return h

    for name in hash_info:
        _compute(name)
    return computed


def topological_sort(structs: dict[tuple[str, str], LcmStruct]) -> list[LcmStruct]:
    """Sort structs so dependencies come first."""
    visited: set[tuple[str, str]] = set()
    result: list[LcmStruct] = []

    def visit(key: tuple[str, str]):
        if key in visited:
            return
        visited.add(key)
        s = structs[key]
        for f in s.fields:
            simple, fpkg = resolve_type(f.type_name, s.package)
            if fpkg is not None and (fpkg, simple) in structs:
                visit((fpkg, simple))
        result.append(s)

    for key in structs:
        visit(key)
    return result


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <lcm_types_dir> <output_dir> [cpp_headers_dir]", file=sys.stderr)
        sys.exit(1)

    lcm_dir = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    cpp_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else None

    # Parse all .lcm files
    all_structs: dict[tuple[str, str], LcmStruct] = {}
    for lcm_file in sorted(lcm_dir.glob("*.lcm")):
        s = parse_lcm_file(lcm_file)
        if s:
            all_structs[(s.package, s.name)] = s

    # Filter to Arduino-compatible types
    compatible = {
        k: v for k, v in all_structs.items()
        if is_arduino_compatible(v, all_structs)
    }

    skipped = set(all_structs.keys()) - set(compatible.keys())
    if skipped:
        print(f"Skipping {len(skipped)} types with variable-length fields:", file=sys.stderr)
        for pkg, name in sorted(skipped):
            print(f"  {pkg}/{name}", file=sys.stderr)

    # Compute LCM fingerprint hashes from C++ generated headers
    fingerprints: dict[str, int] | None = None
    if cpp_dir and cpp_dir.is_dir():
        hash_info = extract_base_hashes(cpp_dir)
        fingerprints = compute_fingerprints(hash_info)
        print(f"Computed {len(fingerprints)} fingerprint hashes from {cpp_dir}", file=sys.stderr)
    else:
        print("Warning: no C++ headers dir provided, fingerprints will be 0", file=sys.stderr)

    # Generate in topological order
    sorted_structs = topological_sort(compatible)
    generated = 0
    for s in sorted_structs:
        header = generate_header(s, compatible, fingerprints)
        pkg_dir = out_dir / s.package
        pkg_dir.mkdir(parents=True, exist_ok=True)
        out_file = pkg_dir / f"{s.name}.h"
        out_file.write_text(header)
        generated += 1

    print(f"Generated {generated} Arduino C headers in {out_dir}")


if __name__ == "__main__":
    main()
