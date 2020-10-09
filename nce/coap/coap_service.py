# -*- coding: utf-8 -*-
from lib import logging
from lib.microcoapy import microcoapy


class CoapService:

    def __init__(self):
        self.logger = logging.get_logger(__name__)
        self.client = microcoapy.Coap()

    def initialize(self, message_callback):
        """

            Initializes the CoAP Client and starts it

        :param message_callback: Callback method
        """
        self.client.set_response_callback(message_callback)
        self.logger.info("Starting the CoAP Client")
        self.client.start()

    def set_message_callback_method(self, message_callback):
        """

            Sets the Message callback message method

        :param message_callback: Callback method
        """
        self.client.set_response_callback(message_callback)

    def post(self, address, port, path, message, content_format, query_options=''):
        """
            Post a CoAP Message

        :param address: CoAP Server address
        :param port: CoAP Server Port
        :param path: CoAP Server Resource Path
        :param message: CoAP Message Payload
        :param content_format: CoAP Message Content Format
        :param query_options: CoAP Query Options
        :return:
        """
        self.logger.info("Posting the CoAP Message to [IP: {} Port: {}]".format(address, port))
        return self.client.post(address, port, path, message, query_options, content_format)

    def poll(self, poll_period_ms):
        """
            Poll the CoAP Client for new incoming messages

        :param poll_period_ms: Poll period in milliseconds
        """
        self.client.poll(poll_period_ms)
