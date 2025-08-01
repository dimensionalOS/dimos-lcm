"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""


from io import BytesIO
import struct
import sys

from lcm_msgs import geometry_msgs
from lcm_msgs import std_msgs
from . import *
from .ChannelFloat32 import ChannelFloat32
class PointCloud(object):

    msg_name = "sensor_msgs.PointCloud"

    __slots__ = ["points_length", "channels_length", "header", "points", "channels"]

    __typenames__ = ["int32_t", "int32_t", "std_msgs.Header", "geometry_msgs.Point32", "ChannelFloat32"]

    __dimensions__ = [None, None, None, ["points_length"], ["channels_length"]]

    points_length: 'int32_t'
    channels_length: 'int32_t'
    header: std_msgs.Header
    points: geometry_msgs.Point32
    channels: ChannelFloat32

    def __init__(self, points_length=0, channels_length=0, header=std_msgs.Header(), points=[], channels=[]):
        # LCM Type: int32_t
        self.points_length = points_length
        # LCM Type: int32_t
        self.channels_length = channels_length
        # LCM Type: std_msgs.Header
        self.header = header
        # LCM Type: geometry_msgs.Point32[points_length]
        self.points = points
        # LCM Type: ChannelFloat32[channels_length]
        self.channels = channels

    def lcm_encode(self):
        buf = BytesIO()
        buf.write(PointCloud._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">ii", self.points_length, self.channels_length))
        assert self.header._get_packed_fingerprint() == std_msgs.Header._get_packed_fingerprint()
        self.header._encode_one(buf)
        for i0 in range(self.points_length):
            assert self.points[i0]._get_packed_fingerprint() == geometry_msgs.Point32._get_packed_fingerprint()
            self.points[i0]._encode_one(buf)
        for i0 in range(self.channels_length):
            assert self.channels[i0]._get_packed_fingerprint() == ChannelFloat32._get_packed_fingerprint()
            self.channels[i0]._encode_one(buf)

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
        self.points_length, self.channels_length = struct.unpack(">ii", buf.read(8))
        self.header = cls._get_field_type('header')._decode_one(buf)
        self.points = []
        for i0 in range(self.points_length):
            self.points.append(cls._get_field_type('points')._decode_one(buf))
        self.channels = []
        for i0 in range(self.channels_length):
            self.channels.append(cls._get_field_type('channels')._decode_one(buf))
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
        tmphash = (0x3ff7dc99e345164e+ std_msgs.Header._get_hash_recursive(newparents)+ geometry_msgs.Point32._get_hash_recursive(newparents)+ ChannelFloat32._get_hash_recursive(newparents)) & 0xffffffffffffffff
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

