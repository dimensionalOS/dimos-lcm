# LCM Message Definitions

This repository contains LCM message definitions for the Dimos project and tools to generate those language bindings.

It depends on our [LCM fork](https://github.com/dimensionalOS/lcm) for generation since we introduced some convinience changes to python message definitions.

lcmgen from our lcm fork is conviniently pulled and built by our `flake.nix`

## Generating Bindings

Run `generate.sh` to regenerate all bindings:

```sh
./generate.sh
```

This will:
1. Convert ROS messages to LCM definitions (from `sources/ros_msgs/` to `lcm_types/`)
2. Generate Python bindings (`generated/python_lcm_msgs/`)
3. Generate C++ bindings (`generated/cpp_lcm_msgs/`)
4. Generate C# bindings (`generated/cs_lcm_msgs/`)
5. Generate Java bindings (`generated/java_lcm_msgs/`)
6. Generate Typescript bindings (`generated/ts_lcm_msgs/`)
7. Generate Rust bindings (`generated/rust_lcm_msgs/`)

## Directory Structure

- `sources/` - Source ROS message definitions and conversion tools
- `lcm_types/` - Generated LCM message definitions
- `generated/` - Generated language bindings

## Python Package

This repo is also a Python package and you can install it via `pip install dimos-lcm`
It is not very useful standalone and is meant to be used in conjuction with actual [dimOS](https://github.com/dimensionalOS/dimos)

## Control values

`control_msgs.ControlValues` carries continuous command or state data
between a control coordinator and device-owning connections. The stream/topic
determines the direction; both use the same wire type.

| Field | Meaning |
|-------|---------|
| `source` | Publisher identity |
| `source_ts` | Publisher Unix timestamp in seconds |
| `epoch` | State generation or command session, established outside the data message |
| `sequence` | Increasing frame number within that source, stream, and epoch |
| `interface_names` | Canonical interface names declared by startup configuration |
| `values` | Corresponding `float64` values |

The two array-length fields are LCM encoding fields and must match their arrays
and each other. Consumers must reject duplicate or undeclared names, non-finite
values, and invalid or stale epochs/sequences. The generated codecs serialize
data; they do not enforce these application-level checks. Timestamps alone do
not establish freshness across machines with unsynchronized clocks.

Interface names and their units, ownership, and supported combinations come from
the resolved connection configuration. The codec does not interpret names or
distinguish robot families. Examples include joint position/velocity for arms,
position/velocity/effort/gains for whole-body control, pose coordinates, and
linear/angular velocity for bases. Pose reference frames must be defined by the
interface contract; they are not inferred from the values.

Empty frames are encodable. Whether they serve as heartbeats, whether frames are
complete or sparse, and what an omitted command means are runtime contract
decisions, not codec behavior. This schema does not authorize motion or implement
a watchdog.

Descriptions are supplied through startup configuration, not LCM announcements.
Discrete lifecycle requests and their results belong to RPC. No description,
readiness, or lifecycle message types are added by this contract.

Validate the Python codec with:

```sh
python -m unittest discover -s tests -v
```
