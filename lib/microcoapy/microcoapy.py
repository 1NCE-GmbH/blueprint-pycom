# -*- coding: utf-8 -*-
import binascii

import uos
import usocket as socket
import utime as time

import lib.microcoapy.coap_macros as macros
from lib.microcoapy.coap_packet import CoapPacket
from lib.microcoapy.coap_reader import parse_packet_header_info
from lib.microcoapy.coap_reader import parse_packet_options_and_payload
from lib.microcoapy.coap_writer import write_packet_header_info
from lib.microcoapy.coap_writer import write_packet_options
from lib.microcoapy.coap_writer import write_packet_payload


class Coap:
    TRANSMISSION_STATE = macros.enum(
        STATE_IDLE=0,
        STATE_SEPARATE_ACK_RECEIVED_WAITING_DATA=1
    )

    def __init__(self):
        self.debug = True
        self.sock = None
        self.callbacks = {}
        self.response_callback = None
        self.port = 0
        self.isServer = False
        self.state = self.TRANSMISSION_STATE.STATE_IDLE
        self.isCustomSocket = False

        # beta flags
        self.discardRetransmissions = False
        self.lastPacketStr = ""

    def log(self, s):
        if self.debug:
            print("[microcoapy]: " + s)

    # Create and initialize a new UDP socket to listen to.
    # port: the local port to be used.
    def start(self, port=macros.COAP_DEFAULT_PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', port))

    # Stop and destroy the socket that has been created by
    # a previous call of 'start' function
    def stop(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None

    # Set a custom instance of a UDP socket
    # Is used instead of calling start/stop functions.
    #
    # Note: This overrides the automatic socket that has been created
    # by the 'start' function.
    # The custom socket must support functions:
    # * socket.sendto(bytes, address)
    # * socket.recvfrom(bufsize)
    # * socket.setblocking(flag)
    def set_custom_socket(self, custom_socket):
        self.stop()
        self.isCustomSocket = True
        self.sock = custom_socket

    def add_incoming_request_callback(self, request_url, callback):
        self.callbacks[request_url] = callback
        self.isServer = True

    def send_packet(self, ip, port, coap_packet):
        if coap_packet.content_format != macros.COAP_CONTENT_FORMAT.COAP_NONE:
            option_buffer = bytearray(2)
            option_buffer[0] = (coap_packet.content_format & 0xFF00) >> 8
            option_buffer[1] = (coap_packet.content_format & 0x00FF)
            coap_packet.add_option(macros.COAP_OPTION_NUMBER.COAP_CONTENT_FORMAT, option_buffer)

        if (coap_packet.query is not None) and (len(coap_packet.query) > 0):
            coap_packet.add_option(macros.COAP_OPTION_NUMBER.COAP_URI_QUERY, coap_packet.query)

        buffer = bytearray()
        write_packet_header_info(buffer, coap_packet)

        write_packet_options(buffer, coap_packet)

        write_packet_payload(buffer, coap_packet)

        status = 0
        try:
            socket_address = (ip, port)
            try:
                socket_address = socket.getaddrinfo(ip, port)[0][-1]
            except Exception as e:
                pass

            status = self.sock.sendto(buffer, socket_address)

            if status > 0:
                status = coap_packet.message_id

            self.log('Packet sent. messageid: ' + str(status))
        except Exception as e:
            status = 0
            print('Exception while sending packet...')
            import sys
            sys.print_exception(e)

        return status

    def send(self, ip, port, url, packet_type, method, token, payload, content_format, query_option):
        packet = CoapPacket()
        packet.type = packet_type
        packet.method = method
        packet.token = token
        packet.payload = payload
        packet.content_format = content_format
        packet.query = query_option

        return self.send_ex(ip, port, url, packet)

    def send_ex(self, ip, port, url, packet):
        self.state = self.TRANSMISSION_STATE.STATE_IDLE
        # messageId field: 16bit -> 0-65535
        # urandom to generate 2 bytes
        random_bytes = uos.urandom(2)
        packet.message_id = (random_bytes[0] << 8) | random_bytes[1]
        packet.set_uri_host(ip)
        packet.set_uri_path(url)

        return self.send_packet(ip, port, packet)

    # to be tested
    def send_response(self, ip, port, message_id, payload, method, content_format, token):
        packet = CoapPacket()

        packet.type = macros.COAP_TYPE.COAP_ACK
        packet.method = method
        packet.token = token
        packet.payload = payload
        packet.message_id = message_id
        packet.content_format = content_format

        return self.send_packet(ip, port, packet)

    def get(self, ip, port, url, token=bytearray()):
        return self.send(ip, port, url, macros.COAP_TYPE.COAP_CON, macros.COAP_METHOD.COAP_GET, token, None,
                         macros.COAP_CONTENT_FORMAT.COAP_NONE, None)

    def put(self, ip, port, url, payload=bytearray(), query_option=None,
            content_format=macros.COAP_CONTENT_FORMAT.COAP_NONE, token=bytearray()):
        return self.send(ip, port, url, macros.COAP_TYPE.COAP_CON, macros.COAP_METHOD.COAP_PUT, token, payload,
                         content_format, query_option)

    def post(self, ip, port, url, payload=bytearray(), query_option=None,
             content_format=macros.COAP_CONTENT_FORMAT.COAP_NONE, token=bytearray()):
        return self.send(ip, port, url, macros.COAP_TYPE.COAP_CON, macros.COAP_METHOD.COAP_POST, token, payload,
                         content_format, query_option)

    def get_non_confirmable(self, ip, port, url, token=bytearray()):
        return self.send(ip, port, url, macros.COAP_TYPE.COAP_NONCON, macros.COAP_METHOD.COAP_GET, token, None,
                         macros.COAP_CONTENT_FORMAT.COAP_NONE, None)

    def put_non_confirmable(self, ip, port, url, payload=bytearray(), query_option=None,
                            content_format=macros.COAP_CONTENT_FORMAT.COAP_NONE, token=bytearray()):
        return self.send(ip, port, url, macros.COAP_TYPE.COAP_NONCON, macros.COAP_METHOD.COAP_PUT, token, payload,
                         content_format, query_option)

    def post_non_confirmable(self, ip, port, url, payload=bytearray(), query_option=None,
                             content_format=macros.COAP_CONTENT_FORMAT.COAP_NONE, token=bytearray()):
        return self.send(ip, port, url, macros.COAP_TYPE.COAP_NONCON, macros.COAP_METHOD.COAP_POST, token, payload,
                         content_format, query_option)

    def handle_incoming_request(self, request_packet, source_ip, source_port):
        url = ""
        for opt in request_packet.options:
            if (opt.number == macros.COAP_OPTION_NUMBER.COAP_URI_PATH) and (len(opt.buffer) > 0):
                if url != "":
                    url += "/"
                url += opt.buffer.decode('unicode_escape')

        url_callback = None
        if url != "":
            url_callback = self.callbacks.get(url)

        if url_callback is None:
            print('Callback for url [', url, "] not found")
            self.send_response(source_ip, source_port, request_packet.message_id,
                               None, macros.COAP_RESPONSE_CODE.COAP_NOT_FOUND,
                               macros.COAP_CONTENT_FORMAT.COAP_NONE, request_packet.token)
        else:
            url_callback(request_packet, source_ip, source_port)

    def read_bytes_from_socket(self, num_of_bytes):
        try:
            return self.sock.recvfrom(num_of_bytes)
        except Exception:
            return None, None

    def parse_packet_token(self, buffer, packet):
        if packet.tokenLength == 0:
            packet.token = None
        elif packet.tokenLength <= 8:
            packet.token = buffer[4:4 + packet.tokenLength]
        else:
            (tempBuffer, tempRemoteAddress) = self.read_bytes_from_socket(macros.BUF_MAX_SIZE - len(buffer))
            if tempBuffer is not None:
                buffer.extend(tempBuffer)
            return False
        return True

    def loop(self, blocking=True):
        if self.sock is None:
            return False

        self.sock.setblocking(blocking)
        (buffer, remoteAddress) = self.read_bytes_from_socket(macros.BUF_MAX_SIZE)
        self.sock.setblocking(True)

        while (buffer is not None) and (len(buffer) > 0):
            buffer_len = len(buffer)
            if (buffer_len < macros.COAP_HEADER_SIZE) or (((buffer[0] & 0xC0) >> 6) != 1):
                (tempBuffer, tempRemoteAddress) = self.read_bytes_from_socket(macros.BUF_MAX_SIZE - buffer_len)
                if tempBuffer is not None:
                    buffer.extend(tempBuffer)
                continue

            packet = CoapPacket()

            self.log("Incoming Packet bytes: " + str(binascii.hexlify(bytearray(buffer))))

            parse_packet_header_info(buffer, packet)

            if not self.parse_packet_token(buffer, packet):
                continue

            if not parse_packet_options_and_payload(buffer, packet):
                return False

            # beta functionality
            if self.discardRetransmissions:
                if packet.to_string() == self.lastPacketStr:
                    self.log("Discarded retransmission message: " + packet.to_string())
                    return False
                else:
                    self.lastPacketStr = packet.to_string()
            ####

            if self.isServer:
                self.handle_incoming_request(packet, remoteAddress[0], remoteAddress[1])
            else:
                # To handle cases of Separate response (rfc7252 #5.2.2)
                if packet.type == macros.COAP_TYPE.COAP_ACK and \
                        packet.method == macros.COAP_METHOD.COAP_EMPTY_MESSAGE:
                    self.state = self.TRANSMISSION_STATE.STATE_SEPARATE_ACK_RECEIVED_WAITING_DATA
                    return False
                # case of piggybacked response where the response is in the ACK (rfc7252 #5.2.1)
                # or the data of a separate message
                else:
                    if self.state == self.TRANSMISSION_STATE.STATE_SEPARATE_ACK_RECEIVED_WAITING_DATA:
                        self.state = self.TRANSMISSION_STATE.STATE_IDLE
                        self.send_response(remoteAddress[0], remoteAddress[1], packet.message_id,
                                           None, macros.COAP_TYPE.COAP_ACK,
                                           macros.COAP_CONTENT_FORMAT.COAP_NONE, packet.token)
                    if self.response_callback is not None:
                        self.response_callback(packet, remoteAddress)
            return True

        return False

    def poll(self, timeout_ms=-1, poll_period_ms=500):
        start_time = time.ticks_ms()
        status = False
        while not status:
            status = self.loop(False)
            if time.ticks_diff(time.ticks_ms(), start_time) >= timeout_ms:
                break
            time.sleep_ms(poll_period_ms)
        return status

    def set_response_callback(self, callback):
        self.response_callback = callback
