"""Benchmark message menu.

This is the canonical list of LCM types the benchmark exercises. Echo
binaries in every supported language must implement decode/encode for
each entry. The C++ echo (and any future statically-typed language)
generates a compile-time dispatch table from this list — keep them in
sync.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MenuEntry:
    type_name: str          # underscore form, matches .lcm filename stem
    package: str            # e.g. "sensor_msgs"
    class_name: str         # e.g. "Image"
    category: str           # tiny / small / medium / variable / large / huge
    description: str
    fixture_kind: str       # which generator function to call
    fixture_arg: int = 0    # parameter for the fixture (e.g. point count)


MENU: list[MenuEntry] = [
    MenuEntry(
        "std_msgs_Int32",
        "std_msgs", "Int32",
        "tiny",
        "4-byte int — codec floor",
        "int32",
    ),
    MenuEntry(
        "geometry_msgs_PoseStamped",
        "geometry_msgs", "PoseStamped",
        "small",
        "Header + Pose; common realtime control message",
        "pose_stamped",
    ),
    MenuEntry(
        "sensor_msgs_Imu",
        "sensor_msgs", "Imu",
        "medium",
        "Dense fixed-size float fields, IMU firehose",
        "imu",
    ),
    MenuEntry(
        "tf2_msgs_TFMessage",
        "tf2_msgs", "TFMessage",
        "variable",
        "Variable-length transform array",
        "tf_message",
        fixture_arg=16,
    ),
    MenuEntry(
        "sensor_msgs_LaserScan",
        "sensor_msgs", "LaserScan",
        "large",
        "Dense float array under UDP fragment threshold",
        "laser_scan",
        fixture_arg=3600,
    ),
    MenuEntry(
        "sensor_msgs_Image",
        "sensor_msgs", "Image",
        "large_fragmented",
        "640x480 RGB image; crosses LCM fragment boundary",
        "image_rgb",
        fixture_arg=640 * 480,
    ),
    MenuEntry(
        "sensor_msgs_PointCloud2",
        "sensor_msgs", "PointCloud2",
        "huge_fragmented",
        "100k XYZ point cloud; stresses fragment reassembly",
        "point_cloud_xyz",
        fixture_arg=100_000,
    ),
]


def by_name(name: str) -> MenuEntry:
    for entry in MENU:
        if entry.type_name == name:
            return entry
    raise KeyError(f"benchmark menu has no entry for {name!r}")
