# -*- coding: utf-8 -*-
import usocket as socket
import utime as time

import config
from lib import logging
from lib.translator.message_service import fill_bytes, ValueType

logging.basic_config(level=logging.INFO)
logger = logging.get_logger("__main__")


def write_udp_gps_message(input_values):
    if input_values[0] == "T":
        message_bytes = bytearray(98)
        message_bytes = fill_bytes(message_bytes, 0, 1, input_values[0], ValueType.CHAR)
        message_bytes = fill_bytes(message_bytes, 1, 20, input_values[1], ValueType.STRING)
        message_bytes = fill_bytes(message_bytes, 20, 28, input_values[2], ValueType.DOUBLE)
        message_bytes = fill_bytes(message_bytes, 28, 36, input_values[3], ValueType.DOUBLE)
        message_bytes = fill_bytes(message_bytes, 36, 38, input_values[4], ValueType.SHORT)
        message_bytes = fill_bytes(message_bytes, 38, 42, input_values[5], ValueType.FLOAT)
        message_bytes = fill_bytes(message_bytes, 42, 46, input_values[6], ValueType.FLOAT)
        message_bytes = fill_bytes(message_bytes, 46, 50, input_values[7], ValueType.FLOAT)
        message_bytes = fill_bytes(message_bytes, 50, 52, input_values[8], ValueType.SHORT)
        message_bytes = fill_bytes(message_bytes, 52, 54, input_values[9], ValueType.SHORT)
        message_bytes = fill_bytes(message_bytes, 54, 56, input_values[10], ValueType.SHORT)
        message_bytes = fill_bytes(message_bytes, 56, 71, input_values[11], ValueType.STRING)
        message_bytes = fill_bytes(message_bytes, 71, 98, input_values[12], ValueType.STRING)
        return message_bytes
    elif input_values[0] == "S":
        message_bytes = bytearray(36)
        message_bytes = fill_bytes(message_bytes, 0, 1, input_values[0], ValueType.CHAR)
        message_bytes = fill_bytes(message_bytes, 1, 36, input_values[1], ValueType.STRING)
        return message_bytes


if __name__ == '__main__':
    logger.info("Opening UDP Socket")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = socket.getaddrinfo(config.UDP_ENDPOINT_ADDRESS, config.UDP_ENDPOINT_PORT)[0][-1]
    logger.info("Resolved Address [{}]".format(addr))

    with open(config.GPS_TRANSLATION_DATA_PATH, "r") as file:
        for line in file.readlines():
            values = line.split(",")
            message = write_udp_gps_message(values)

            logger.info(
                "Sending UDP message to {}:{} with body {}".format(
                    config.UDP_ENDPOINT_ADDRESS,
                    config.UDP_ENDPOINT_PORT,
                    message))
            s.sendto(message, addr)
            logger.info("Sent UDP Message to the UDP Broker")
            time.sleep(60)

