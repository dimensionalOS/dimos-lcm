"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""


from io import BytesIO
import struct
import sys

from . import *
from .MultiArrayLayout import MultiArrayLayout
class Int64MultiArray(object):

    msg_name = "std_msgs.Int64MultiArray"

    __slots__ = ["data_length", "layout", "data"]

    __typenames__ = ["int32_t", "MultiArrayLayout", "int64_t"]

    __dimensions__ = [None, None, ["data_length"]]

    data_length: 'int32_t'
    layout: MultiArrayLayout
    data: 'int64_t'

    def __init__(self, data_length=0, layout=MultiArrayLayout(), data=[]):
        # LCM Type: int32_t
        self.data_length = data_length
        # LCM Type: MultiArrayLayout
        self.layout = layout
        # LCM Type: int64_t[data_length]
        self.data = data

    def lcm_encode(self):
        buf = BytesIO()
        buf.write(Int64MultiArray._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">i", self.data_length))
        assert self.layout._get_packed_fingerprint() == MultiArrayLayout._get_packed_fingerprint()
        self.layout._encode_one(buf)
        buf.write(struct.pack('>%dq' % self.data_length, *self.data[:self.data_length]))

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
        self.data_length = struct.unpack(">i", buf.read(4))[0]
        self.layout = cls._get_field_type('layout')._decode_one(buf)
        self.data = struct.unpack('>%dq' % self.data_length, buf.read(self.data_length * 8))
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
        tmphash = (0xaa51366c8f22187e+ MultiArrayLayout._get_hash_recursive(newparents)) & 0xffffffffffffffff
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

