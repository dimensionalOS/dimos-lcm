"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""


from io import BytesIO
import struct
import sys

from . import *
from lcm_msgs import std_msgs
from .VisionClass import VisionClass
class LabelInfo(object):

    msg_name = "vision_msgs.LabelInfo"

    __slots__ = ["class_map_length", "header", "class_map", "threshold"]

    __typenames__ = ["int32_t", "std_msgs.Header", "VisionClass", "float"]

    __dimensions__ = [None, None, ["class_map_length"], None]

    class_map_length: 'int32_t'
    header: std_msgs.Header
    class_map: VisionClass
    threshold: 'float'

    def __init__(self, class_map_length=0, header=std_msgs.Header(), class_map=[], threshold=0.0):
        # LCM Type: int32_t
        self.class_map_length = class_map_length
        # LCM Type: std_msgs.Header
        self.header = header
        # LCM Type: VisionClass[class_map_length]
        self.class_map = class_map
        # LCM Type: float
        self.threshold = threshold

    def lcm_encode(self):
        buf = BytesIO()
        buf.write(LabelInfo._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">i", self.class_map_length))
        assert self.header._get_packed_fingerprint() == std_msgs.Header._get_packed_fingerprint()
        self.header._encode_one(buf)
        for i0 in range(self.class_map_length):
            assert self.class_map[i0]._get_packed_fingerprint() == VisionClass._get_packed_fingerprint()
            self.class_map[i0]._encode_one(buf)
        buf.write(struct.pack(">f", self.threshold))

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
        self.class_map_length = struct.unpack(">i", buf.read(4))[0]
        self.header = cls._get_field_type('header')._decode_one(buf)
        self.class_map = []
        for i0 in range(self.class_map_length):
            self.class_map.append(cls._get_field_type('class_map')._decode_one(buf))
        self.threshold = struct.unpack(">f", buf.read(4))[0]
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
        tmphash = (0x73231a5050580a67+ std_msgs.Header._get_hash_recursive(newparents)+ VisionClass._get_hash_recursive(newparents)) & 0xffffffffffffffff
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

