# -*- coding: utf-8 -*-
import usocket as socket

import config
from lib import logging

logging.basic_config(level=logging.INFO)
logger = logging.get_logger("__main__")

if __name__ == '__main__':
    message = "Hello, UDP. Can you hear me?".encode()

    logger.info("Opening UDP Socket")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = socket.getaddrinfo(config.UDP_ENDPOINT_ADDRESS, config.UDP_ENDPOINT_PORT)[0][-1]
    logger.info("Resolved Address [{}]".format(addr))
    logger.info(
        "Sending UDP message to {}:{} with body {}".format(
            config.UDP_ENDPOINT_ADDRESS,
            config.UDP_ENDPOINT_PORT,
            message))
    s.sendto(message, addr)
    logger.info("Sent UDP Message to the UDP Broker")
