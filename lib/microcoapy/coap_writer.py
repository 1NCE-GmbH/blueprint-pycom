# -*- coding: utf-8 -*-
from lib.microcoapy.coap_macros import BUF_MAX_SIZE
from lib.microcoapy.coap_macros import COAP_VERSION


def coap_option_delta(v):
    if v < 13:
        return 0xFF & v
    elif v <= 0xFF + 13:
        return 13
    else:
        return 14


def write_packet_header_info(buffer, packet):
    # make coap packet base header
    buffer.append(COAP_VERSION.COAP_VERSION_1 << 6)
    buffer[0] |= (packet.type & 0x03) << 4
    # max: 8 bytes of tokens, if token length is greater, it is ignored
    token_length = 0
    if (packet.token is not None) and (len(packet.token) <= 0x0F):
        token_length = len(packet.token)

    buffer[0] |= (token_length & 0x0F)
    buffer.append(packet.method)
    buffer.append(packet.message_id >> 8)
    buffer.append(packet.message_id & 0xFF)

    if token_length > 0:
        buffer.extend(packet.token)


def write_packet_options(buffer, packet):
    running_delta = 0
    # make option header
    for opt in packet.options:
        if (opt is None) or (opt.buffer is None) or (len(opt.buffer) == 0):
            continue

        opt_buffer_len = len(opt.buffer)

        if (len(buffer) + 5 + opt_buffer_len) >= BUF_MAX_SIZE:
            return 0

        optdelta = opt.number - running_delta
        delta = coap_option_delta(optdelta)
        length = coap_option_delta(opt_buffer_len)

        buffer.append(0xFF & (delta << 4 | length))
        if delta == 13:
            buffer.append(optdelta - 13)
        elif delta == 14:
            buffer.append((optdelta - 269) >> 8)
            buffer.append(0xFF & (optdelta - 269))

        if length == 13:
            buffer.append(opt_buffer_len - 13)
        elif length == 14:
            buffer.append(opt_buffer_len >> 8)
            buffer.append(0xFF & (opt_buffer_len - 269))

        buffer.extend(opt.buffer)
        running_delta = opt.number


def write_packet_payload(buffer, packet):
    # make payload
    if (packet.payload is not None) and (len(packet.payload)):
        if (len(buffer) + 1 + len(packet.payload)) >= BUF_MAX_SIZE:
            return 0
        buffer.append(0xFF)
        buffer.extend(packet.payload)
