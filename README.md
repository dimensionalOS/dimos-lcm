# LCM Message Definitions

This repository contains LCM message definitions for the Dimos project and tools to generate language bindings.

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

## Directory Structure

- `sources/` - Source ROS message definitions and conversion tools
- `lcm_types/` - Generated LCM message definitions
- `generated/` - Generated language bindings

