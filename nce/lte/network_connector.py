# -*- coding: utf-8 -*-
from network import LTE

from lib import logging
import time


class NetworkConnector:

    def __init__(self):
        self.logger = logging.get_logger(__name__)
        self.lte = LTE()

    def _attach(self):
        """
            Attaches to the 1nce LTE network
        """
        self.lte.attach()
        while not self.lte.isattached():
            time.sleep(0.5)
            print(".", end="")
        self.logger.info("Sim attached to iot.1nce.net")

    def connect(self):
        """
            Connects to the 1nce LTE network
        """
        self._attach()
        self.lte.connect()
        while not self.lte.isconnected():
            time.sleep(0.5)
        self.logger.info("Sim connected to iot.1nce.net")

    def disconnect(self):
        self.lte.disconnect()
        self.logger.info("Sim disconnected from iot.1nce.net")

    def get_reception(self):
        """
            Gets the current reception to the 1nce network

        :return: Number Reception to the 1nce network
        """
        return self.lte.send_at_cmd("AT+CSQ")
