# -*- coding: utf-8 -*-
import ustruct as struct


class ValueType:
    STRING = "string"
    CHAR = "char"
    DOUBLE = "double"
    FLOAT = "float"
    INT = "int"
    UINT = "uint"
    SHORT = "short"
    BOOLEAN = "boolean"


def fill_bytes(byte_array, start, end, value, value_type):
    if value_type == ValueType.CHAR and value is not None and value is not '':
        byte_array[start:end] = struct.pack("s", value)
    elif value_type == ValueType.STRING and value is not None and value is not '':
        byte_array[start:end] = struct.pack("{}s".format(end - start), value)
    elif value_type == ValueType.DOUBLE and value is not None and value is not '':
        byte_array[start:end] = struct.pack("d", float(value))
    elif value_type == ValueType.FLOAT and value is not None and value is not '':
        byte_array[start:end] = struct.pack("f", float(value))
    elif value_type == ValueType.INT and value is not None and value is not '':
        byte_array[start:end] = struct.pack("i", int(value))
    elif value_type == ValueType.UINT and value is not None and value is not '':
        byte_array[start:end] = struct.pack("I", int(value))
    elif value_type == ValueType.SHORT and value is not None and value is not '':
        byte_array[start:end] = struct.pack("h", int(value))
    return byte_array
