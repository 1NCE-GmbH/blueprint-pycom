# -*- coding: utf-8 -*-
import lib.microcoapy.coap_macros as macros
from lib.microcoapy.coap_option import CoapOption


class CoapPacket:
    def __init__(self):
        self.version = macros.COAP_VERSION.COAP_VERSION_UNSUPPORTED
        self.type = macros.COAP_TYPE.COAP_CON  # uint8_t
        self.method = macros.COAP_METHOD.COAP_GET  # uint8_t
        self.token = bytearray()
        self.payload = bytearray()
        self.message_id = 0
        self.content_format = macros.COAP_CONTENT_FORMAT.COAP_NONE
        self.query = bytearray()  # uint8_t*
        self.options = []

    def add_option(self, number, opt_payload):
        if len(self.options) >= macros.MAX_OPTION_NUM:
            return
        self.options.append(CoapOption(number, opt_payload))

    def set_uri_host(self, address):
        self.add_option(macros.COAP_OPTION_NUMBER.COAP_URI_HOST, address)

    def set_uri_path(self, url):
        for subPath in url.split('/'):
            self.add_option(macros.COAP_OPTION_NUMBER.COAP_URI_PATH, subPath)

    def to_string(self):
        class_, detail = macros.CoapResponseCode.decode(self.method)
        return "type: {}, method: {}.{:02d}, messageid: {}, payload: {}".format(
            macros.coap_type_to_string(self.type),
            class_, detail,
            self.message_id,
            self.payload)
