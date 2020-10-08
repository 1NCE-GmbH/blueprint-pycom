# -*- coding: utf-8 -*-
import lib.microcoapy.coap_macros as macros
from lib.microcoapy.coap_option import CoapOption


def parse_option(packet, running_delta, buffer, i):
    option = CoapOption()
    header_length = 1

    error_message = (False, running_delta, i)

    if buffer is None:
        return error_message

    buffer_length = len(buffer) - i

    if buffer_length < header_length:
        return error_message

    delta = (buffer[i] & 0xF0) >> 4
    length = buffer[i] & 0x0F

    if delta == 15 or length == 15:
        return error_message

    if delta == 13:
        header_length += 1
        if buffer_length < header_length:
            return error_message
        delta = buffer[i + 1] + 13
        i += 1
    elif delta == 14:
        header_length += 2
        if buffer_length < header_length:
            return error_message
        delta = ((buffer[i + 1] << 8) | buffer[i + 2]) + 269
        i += 2

    if length == 13:
        header_length += 1
        if buffer_length < header_length:
            return error_message
        length = buffer[i + 1] + 13
        i += 1
    elif length == 14:
        header_length += 2
        if buffer_length < header_length:
            return error_message
        length = ((buffer[i + 1] << 8) | buffer[i + 2]) + 269
        i += 2

    end_of_option_index = (i + 1 + length)

    if end_of_option_index > len(buffer):
        return error_message

    option.number = delta + running_delta
    option.buffer = buffer[i + 1:i + 1 + length]
    packet.options.append(option)

    return True, running_delta + delta, end_of_option_index


def parse_packet_header_info(buffer, packet):
    packet.version = (buffer[0] & 0xC0) >> 6
    packet.type = (buffer[0] & 0x30) >> 4
    packet.tokenLength = buffer[0] & 0x0F
    packet.method = buffer[1]
    packet.message_id = 0xFF00 & (buffer[2] << 8)
    packet.message_id |= 0x00FF & buffer[3]


def parse_packet_options_and_payload(buffer, packet):
    buffer_length = len(buffer)
    if (macros.COAP_HEADER_SIZE + packet.tokenLength) < buffer_length:
        delta = 0
        buffer_index = macros.COAP_HEADER_SIZE + packet.tokenLength
        while (len(packet.options) < macros.MAX_OPTION_NUM) and \
                (buffer_index < buffer_length) and \
                (buffer[buffer_index] != 0xFF):
            (status, delta, buffer_index) = parse_option(packet, delta, buffer, buffer_index)
            if status is False:
                return False

        if ((buffer_index + 1) < buffer_length) and (buffer[buffer_index] == 0xFF):
            packet.payload = buffer[buffer_index + 1:]  # does this works?
        else:
            packet.payload = None
    return True
