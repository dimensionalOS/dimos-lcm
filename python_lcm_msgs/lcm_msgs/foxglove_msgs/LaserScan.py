"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""


from io import BytesIO
import struct
import sys

from lcm_msgs import geometry_msgs
from lcm_msgs import builtin_interfaces
class LaserScan(object):

    msg_name = "foxglove_msgs.LaserScan"

    __slots__ = ["ranges_length", "intensities_length", "timestamp", "frame_id", "pose", "start_angle", "end_angle", "ranges", "intensities"]

    __typenames__ = ["int32_t", "int32_t", "builtin_interfaces.Time", "string", "geometry_msgs.Pose", "double", "double", "double", "double"]

    __dimensions__ = [None, None, None, None, None, None, None, ["ranges_length"], ["intensities_length"]]

    ranges_length: 'int32_t'
    intensities_length: 'int32_t'
    timestamp: builtin_interfaces.Time
    frame_id: 'string'
    pose: geometry_msgs.Pose
    start_angle: 'double'
    end_angle: 'double'
    ranges: 'double'
    intensities: 'double'

    def __init__(self, ranges_length=0, intensities_length=0, timestamp=builtin_interfaces.Time(), frame_id="", pose=geometry_msgs.Pose(), start_angle=0.0, end_angle=0.0, ranges=[], intensities=[]):
        # LCM Type: int32_t
        self.ranges_length = ranges_length
        # LCM Type: int32_t
        self.intensities_length = intensities_length
        # LCM Type: builtin_interfaces.Time
        self.timestamp = timestamp
        # LCM Type: string
        self.frame_id = frame_id
        # LCM Type: geometry_msgs.Pose
        self.pose = pose
        # LCM Type: double
        self.start_angle = start_angle
        # LCM Type: double
        self.end_angle = end_angle
        # LCM Type: double[ranges_length]
        self.ranges = ranges
        # LCM Type: double[intensities_length]
        self.intensities = intensities

    def lcm_encode(self):
        buf = BytesIO()
        buf.write(LaserScan._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">ii", self.ranges_length, self.intensities_length))
        assert self.timestamp._get_packed_fingerprint() == builtin_interfaces.Time._get_packed_fingerprint()
        self.timestamp._encode_one(buf)
        __frame_id_encoded = self.frame_id.encode('utf-8')
        buf.write(struct.pack('>I', len(__frame_id_encoded)+1))
        buf.write(__frame_id_encoded)
        buf.write(b"\0")
        assert self.pose._get_packed_fingerprint() == geometry_msgs.Pose._get_packed_fingerprint()
        self.pose._encode_one(buf)
        buf.write(struct.pack(">dd", self.start_angle, self.end_angle))
        buf.write(struct.pack('>%dd' % self.ranges_length, *self.ranges[:self.ranges_length]))
        buf.write(struct.pack('>%dd' % self.intensities_length, *self.intensities[:self.intensities_length]))

    @classmethod
    def lcm_decode(cls, data: bytes):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != cls._get_packed_fingerprint():
            raise ValueError("Decode error")
        return cls._decode_one(buf)

    @classmethod
    def _decode_one(cls, buf):
        self = cls()
        self.ranges_length, self.intensities_length = struct.unpack(">ii", buf.read(8))
        self.timestamp = cls._get_field_type('timestamp')._decode_one(buf)
        __frame_id_len = struct.unpack('>I', buf.read(4))[0]
        self.frame_id = buf.read(__frame_id_len)[:-1].decode('utf-8', 'replace')
        self.pose = cls._get_field_type('pose')._decode_one(buf)
        self.start_angle, self.end_angle = struct.unpack(">dd", buf.read(16))
        self.ranges = struct.unpack('>%dd' % self.ranges_length, buf.read(self.ranges_length * 8))
        self.intensities = struct.unpack('>%dd' % self.intensities_length, buf.read(self.intensities_length * 8))
        return self

    @classmethod
    def _get_field_type(cls, field_name):
        """Get the type for a field from annotations."""
        annotation = cls.__annotations__.get(field_name)
        if annotation is None:
            return None
        if isinstance(annotation, str):
            module = sys.modules[cls.__module__]
            if hasattr(module, annotation):
                return getattr(module, annotation)
            return None
        return annotation

    @classmethod
    def _get_hash_recursive(cls, parents):
        if cls in parents: return 0
        newparents = parents + [cls]
        tmphash = (0x22e7c769ba6a90c2+ builtin_interfaces.Time._get_hash_recursive(newparents)+ geometry_msgs.Pose._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _packed_fingerprint = None

    @classmethod
    def _get_packed_fingerprint(cls):
        if cls._packed_fingerprint is None:
            cls._packed_fingerprint = struct.pack(">Q", cls._get_hash_recursive([]))
        return cls._packed_fingerprint

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", cls._get_packed_fingerprint())[0]

