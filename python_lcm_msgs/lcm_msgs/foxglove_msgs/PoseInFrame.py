"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""


from io import BytesIO
import struct
import sys

from lcm_msgs import geometry_msgs
from lcm_msgs import builtin_interfaces
class PoseInFrame(object):

    msg_name = "foxglove_msgs.PoseInFrame"

    __slots__ = ["timestamp", "frame_id", "pose"]

    __typenames__ = ["builtin_interfaces.Time", "string", "geometry_msgs.Pose"]

    __dimensions__ = [None, None, None]

    timestamp: builtin_interfaces.Time
    frame_id: 'string'
    pose: geometry_msgs.Pose

    def __init__(self, timestamp=builtin_interfaces.Time(), frame_id="", pose=geometry_msgs.Pose()):
        # LCM Type: builtin_interfaces.Time
        self.timestamp = timestamp
        # LCM Type: string
        self.frame_id = frame_id
        # LCM Type: geometry_msgs.Pose
        self.pose = pose

    def lcm_encode(self):
        buf = BytesIO()
        buf.write(PoseInFrame._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        assert self.timestamp._get_packed_fingerprint() == builtin_interfaces.Time._get_packed_fingerprint()
        self.timestamp._encode_one(buf)
        __frame_id_encoded = self.frame_id.encode('utf-8')
        buf.write(struct.pack('>I', len(__frame_id_encoded)+1))
        buf.write(__frame_id_encoded)
        buf.write(b"\0")
        assert self.pose._get_packed_fingerprint() == geometry_msgs.Pose._get_packed_fingerprint()
        self.pose._encode_one(buf)

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
        self.timestamp = cls._get_field_type('timestamp')._decode_one(buf)
        __frame_id_len = struct.unpack('>I', buf.read(4))[0]
        self.frame_id = buf.read(__frame_id_len)[:-1].decode('utf-8', 'replace')
        self.pose = cls._get_field_type('pose')._decode_one(buf)
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
        tmphash = (0x84c6ef3a0a4c5cd6+ builtin_interfaces.Time._get_hash_recursive(newparents)+ geometry_msgs.Pose._get_hash_recursive(newparents)) & 0xffffffffffffffff
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

