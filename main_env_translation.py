# -*- coding: utf-8 -*-
import usocket as socket
import utime as time

import config
from lib import logging
from lib.translator.message_service import fill_bytes, ValueType

logging.basic_config(level=logging.INFO)
logger = logging.get_logger("__main__")


def write_udp_env_data_coll_message(input_values):
    message_bytes = bytearray(17)
    message_bytes = fill_bytes(message_bytes, 0, 4, input_values[0], ValueType.FLOAT)
    message_bytes = fill_bytes(message_bytes, 4, 8, input_values[1], ValueType.FLOAT)
    message_bytes = fill_bytes(message_bytes, 8, 12, input_values[2], ValueType.FLOAT)
    message_bytes = fill_bytes(message_bytes, 12, 16, input_values[3], ValueType.FLOAT)
    message_bytes = fill_bytes(message_bytes, 16, 17, input_values[4], ValueType.CHAR)
    return message_bytes


if __name__ == '__main__':
    logger.info("Opening UDP Socket")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = socket.getaddrinfo(config.UDP_ENDPOINT_ADDRESS, config.UDP_ENDPOINT_PORT)[0][-1]
    logger.info("Resolved Address [{}]".format(addr))

    with open(config.ENV_DATA_COLLECTOR_TRANSLATION_DATA_PATH, "r") as file:
        for line in file.readlines():
            values = line.split(",")
            message = write_udp_env_data_coll_message(values)

            logger.info(
                "Sending UDP message to {}:{} with body {}".format(
                    config.UDP_ENDPOINT_ADDRESS,
                    config.UDP_ENDPOINT_PORT,
                    message))
            s.sendto(message, addr)
            logger.info("Sent UDP Message to the UDP Broker")
            time.sleep(60)

