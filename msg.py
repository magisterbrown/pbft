from ctypes import *

class Message(Structure):
    _fields_ = [("from_id", c_int),
                ("to_id", c_int),
                ("msg", c_char)]
