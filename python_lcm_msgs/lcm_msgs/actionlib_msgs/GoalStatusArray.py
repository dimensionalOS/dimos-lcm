"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""


from io import BytesIO
import struct
import sys

from . import *
from lcm_msgs import std_msgs
from .GoalStatus import GoalStatus
class GoalStatusArray(object):

    msg_name = "GoalStatusArray"

    __slots__ = ["status_list_length", "header", "status_list"]

    __typenames__ = ["int32_t", "std_msgs.Header", "GoalStatus"]

    __dimensions__ = [None, None, ["status_list_length"]]

    status_list_length: 'int32_t'
    header: std_msgs.Header
    status_list: GoalStatus

    def __init__(self, status_list_length=0, header=std_msgs.Header(), status_list=[]):
        # LCM Type: int32_t
        self.status_list_length = status_list_length
        # LCM Type: std_msgs.Header
        self.header = header
        # LCM Type: GoalStatus[status_list_length]
        self.status_list = status_list

    def lcm_encode(self):
        buf = BytesIO()
        buf.write(GoalStatusArray._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">i", self.status_list_length))
        assert self.header._get_packed_fingerprint() == std_msgs.Header._get_packed_fingerprint()
        self.header._encode_one(buf)
        for i0 in range(self.status_list_length):
            assert self.status_list[i0]._get_packed_fingerprint() == GoalStatus._get_packed_fingerprint()
            self.status_list[i0]._encode_one(buf)

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
        self.status_list_length = struct.unpack(">i", buf.read(4))[0]
        self.header = cls._get_field_type('header')._decode_one(buf)
        self.status_list = []
        for i0 in range(self.status_list_length):
            self.status_list.append(cls._get_field_type('status_list')._decode_one(buf))
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
        tmphash = (0xf5c35b2e7eed0fa+ std_msgs.Header._get_hash_recursive(newparents)+ GoalStatus._get_hash_recursive(newparents)) & 0xffffffffffffffff
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

