"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""


from io import BytesIO
import struct

from lcm_msgs import geometry_msgs
from . import *
from .Color import Color
class CubePrimitive(object):

    msg_name = "foxglove_msgs.CubePrimitive"

    __slots__ = ["pose", "size", "color"]

    __typenames__ = ["geometry_msgs.Pose", "geometry_msgs.Vector3", "Color"]

    __dimensions__ = [None, None, None]

    def __init__(self, pose=geometry_msgs.Pose(), size=geometry_msgs.Vector3(), color=Color()):
        # LCM Type: geometry_msgs.Pose
        self.pose = pose
        # LCM Type: geometry_msgs.Vector3
        self.size = size
        # LCM Type: Color
        self.color = color

    def lcm_encode(self):
        buf = BytesIO()
        buf.write(CubePrimitive._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        assert self.pose._get_packed_fingerprint() == geometry_msgs.Pose._get_packed_fingerprint()
        self.pose._encode_one(buf)
        assert self.size._get_packed_fingerprint() == geometry_msgs.Vector3._get_packed_fingerprint()
        self.size._encode_one(buf)
        assert self.color._get_packed_fingerprint() == Color._get_packed_fingerprint()
        self.color._encode_one(buf)

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
        self = CubePrimitive()
        self.pose = geometry_msgs.Pose._decode_one(buf)
        self.size = geometry_msgs.Vector3._decode_one(buf)
        self.color = Color._decode_one(buf)
        return self

    @classmethod
    def _get_hash_recursive(cls, parents):
        if cls in parents: return 0
        newparents = parents + [cls]
        tmphash = (0xe7e8912ea6542887+ geometry_msgs.Pose._get_hash_recursive(newparents)+ geometry_msgs.Vector3._get_hash_recursive(newparents)+ Color._get_hash_recursive(newparents)) & 0xffffffffffffffff
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

