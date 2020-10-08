# -*- coding: utf-8 -*-


class CoapOption:
    def __init__(self, number=-1, buffer=None):
        self.number = number
        byte_buf = bytearray()
        if buffer is not None:
            byte_buf.extend(buffer)
        self.buffer = byte_buf
