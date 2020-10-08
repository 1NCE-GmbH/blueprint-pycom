# -*- coding: utf-8 -*-
from network import LTE

from lib import logging
import time
import re


class NetworkConnector:

    def __init__(self):
        self.logger = logging.get_logger(__name__)
        self.lte = LTE()

    def _attach(self):
        """
            Attaches to the 1nce network
        """
        self.lte.attach()
        while not self.lte.isattached():
            time.sleep(0.5)
            print(".", end="")
        self.logger.info("Sim attached to iot.1nce.net")

    def connect(self):
        """
            Connects to the 1nce network
        """
        self._attach()
        self.lte.connect()
        while not self.lte.isconnected():
            time.sleep(0.5)
        self.logger.info("Sim connected to iot.1nce.net")

    def disconnect(self):
        self.lte.disconnect()
        self.logger.info("Sim disconnected from iot.1nce.net")

    def _send_at_command(self, command):
        """
            Sends AT command over the modem

        :rtype: Response string
        """
        self.lte.pppsuspend()
        resp = self.lte.send_at_cmd(command)
        self.lte.pppresume()
        return resp

    def get_reception(self):
        """
            Gets the current reception to the 1nce network

        :return: Number Reception to the 1nce network
        """
        return self._send_at_command("AT+CSQ")

    def get_ip_address(self):
        """"
            Gets the Device it's Local IP address

        :return IP Address
        """
        resp = self._send_at_command("AT+CGPADDR=1")
        self.logger.info(resp)
        search = re.search(r"\"([1-2]?\d?\d\.[1-2]?\d?\d\.[1-2]?\d?\d\.[1-2]?\d?\d)\"", resp)
        if search:
            return search.group(1)
        return None
