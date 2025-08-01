"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""


from io import BytesIO
import struct
import sys

from lcm_msgs import geometry_msgs
from lcm_msgs import std_msgs
class InteractiveMarkerPose(object):

    msg_name = "visualization_msgs.InteractiveMarkerPose"

    __slots__ = ["header", "pose", "name"]

    __typenames__ = ["std_msgs.Header", "geometry_msgs.Pose", "string"]

    __dimensions__ = [None, None, None]

    header: std_msgs.Header
    pose: geometry_msgs.Pose
    name: 'string'

    def __init__(self, header=std_msgs.Header(), pose=geometry_msgs.Pose(), name=""):
        # LCM Type: std_msgs.Header
        self.header = header
        # LCM Type: geometry_msgs.Pose
        self.pose = pose
        # LCM Type: string
        self.name = name

    def lcm_encode(self):
        buf = BytesIO()
        buf.write(InteractiveMarkerPose._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        assert self.header._get_packed_fingerprint() == std_msgs.Header._get_packed_fingerprint()
        self.header._encode_one(buf)
        assert self.pose._get_packed_fingerprint() == geometry_msgs.Pose._get_packed_fingerprint()
        self.pose._encode_one(buf)
        __name_encoded = self.name.encode('utf-8')
        buf.write(struct.pack('>I', len(__name_encoded)+1))
        buf.write(__name_encoded)
        buf.write(b"\0")

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
        self.header = cls._get_field_type('header')._decode_one(buf)
        self.pose = cls._get_field_type('pose')._decode_one(buf)
        __name_len = struct.unpack('>I', buf.read(4))[0]
        self.name = buf.read(__name_len)[:-1].decode('utf-8', 'replace')
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
        tmphash = (0x8c873ae70410464d+ std_msgs.Header._get_hash_recursive(newparents)+ geometry_msgs.Pose._get_hash_recursive(newparents)) & 0xffffffffffffffff
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

