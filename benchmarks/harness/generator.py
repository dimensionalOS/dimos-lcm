"""Fixture builders that produce a populated LCM message instance per menu entry."""

import math

from .loader import load_class


def _header():
    Header = load_class("std_msgs_Header")
    Time = load_class("std_msgs_Time")
    h = Header()
    h.seq = 0
    h.frame_id = "bench_frame"
    h.stamp = Time(sec=0, nsec=0)
    return h


def make_int32(_: int = 0):
    Int32 = load_class("std_msgs_Int32")
    return Int32(data=42)


def make_pose_stamped(_: int = 0):
    PoseStamped = load_class("geometry_msgs_PoseStamped")
    Pose = load_class("geometry_msgs_Pose")
    Point = load_class("geometry_msgs_Point")
    Quaternion = load_class("geometry_msgs_Quaternion")
    pose = Pose(
        position=Point(x=1.0, y=2.0, z=3.0),
        orientation=Quaternion(x=0.0, y=0.0, z=0.0, w=1.0),
    )
    return PoseStamped(header=_header(), pose=pose)


def make_imu(_: int = 0):
    Imu = load_class("sensor_msgs_Imu")
    Vector3 = load_class("geometry_msgs_Vector3")
    Quaternion = load_class("geometry_msgs_Quaternion")
    return Imu(
        header=_header(),
        orientation=Quaternion(x=0.0, y=0.0, z=0.0, w=1.0),
        orientation_covariance=[0.01] * 9,
        angular_velocity=Vector3(x=0.1, y=-0.2, z=0.3),
        angular_velocity_covariance=[0.01] * 9,
        linear_acceleration=Vector3(x=0.01, y=0.02, z=9.81),
        linear_acceleration_covariance=[0.01] * 9,
    )


def make_tf_message(count: int):
    TFMessage = load_class("tf2_msgs_TFMessage")
    TransformStamped = load_class("geometry_msgs_TransformStamped")
    Transform = load_class("geometry_msgs_Transform")
    Vector3 = load_class("geometry_msgs_Vector3")
    Quaternion = load_class("geometry_msgs_Quaternion")
    transforms = []
    for i in range(count):
        ts = TransformStamped(
            header=_header(),
            child_frame_id=f"frame_{i}",
            transform=Transform(
                translation=Vector3(x=float(i), y=float(i) * 0.5, z=0.0),
                rotation=Quaternion(x=0.0, y=0.0, z=0.0, w=1.0),
            ),
        )
        transforms.append(ts)
    return TFMessage(transforms_length=count, transforms=transforms)


def make_laser_scan(beams: int):
    LaserScan = load_class("sensor_msgs_LaserScan")
    ranges = [1.0 + 0.001 * i for i in range(beams)]
    intensities = [10.0] * beams
    return LaserScan(
        header=_header(),
        ranges_length=beams,
        intensities_length=beams,
        angle_min=-math.pi,
        angle_max=math.pi,
        angle_increment=(2 * math.pi) / beams,
        time_increment=0.0,
        scan_time=0.1,
        range_min=0.05,
        range_max=30.0,
        ranges=ranges,
        intensities=intensities,
    )


def make_image_rgb(num_pixels: int):
    Image = load_class("sensor_msgs_Image")
    width = 640
    height = max(1, num_pixels // width)
    nbytes = width * height * 3
    data = bytes((i & 0xFF for i in range(nbytes)))
    return Image(
        header=_header(),
        height=height,
        width=width,
        encoding="rgb8",
        is_bigendian=0,
        step=width * 3,
        data_length=nbytes,
        data=data,
    )


def make_point_cloud_xyz(num_points: int):
    PointCloud2 = load_class("sensor_msgs_PointCloud2")
    PointField = load_class("sensor_msgs_PointField")
    fields = [
        PointField(name="x", offset=0, datatype=7, count=1),
        PointField(name="y", offset=4, datatype=7, count=1),
        PointField(name="z", offset=8, datatype=7, count=1),
    ]
    point_step = 12
    data = bytes((i & 0xFF for i in range(num_points * point_step)))
    return PointCloud2(
        header=_header(),
        height=1,
        width=num_points,
        fields_length=len(fields),
        fields=fields,
        is_bigendian=False,
        point_step=point_step,
        row_step=point_step * num_points,
        data_length=len(data),
        data=data,
        is_dense=True,
    )


_FIXTURE_BUILDERS = {
    "int32": make_int32,
    "pose_stamped": make_pose_stamped,
    "imu": make_imu,
    "tf_message": make_tf_message,
    "laser_scan": make_laser_scan,
    "image_rgb": make_image_rgb,
    "point_cloud_xyz": make_point_cloud_xyz,
}


def build_fixture(fixture_kind: str, fixture_arg: int):
    try:
        builder = _FIXTURE_BUILDERS[fixture_kind]
    except KeyError as exc:
        raise KeyError(f"no fixture builder for {fixture_kind!r}") from exc
    return builder(fixture_arg)
