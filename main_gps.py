import gc
import config
import machine
import usocket as socket

from L76GNSS import L76GNSS
from pycoproc_2 import Pycoproc
from lib import logging
from nce.translator.message_service import fill_bytes, ValueType
from nce.network.network_connector import NetworkConnector

logging.basic_config(level=logging.INFO)
logger = logging.get_logger("__main__")

gc.enable()
py = Pycoproc()
if py.read_product_id() != Pycoproc.USB_PID_PYTRACK:
    raise Exception('Not a Pytrack')

l76 = L76GNSS(py, timeout=60, buffer=512)

if __name__ == '__main__':
    logger.info("Opening UDP Socket")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = socket.getaddrinfo(config.UDP_ENDPOINT_ADDRESS, config.UDP_ENDPOINT_PORT)[0][-1]
    logger.info("Resolved Address [{}]".format(addr))

    coord = l76.coordinates()
    logger.info("Current Coordinates [{}]".format(coord))
    message = bytearray(16)
    message = fill_bytes(message, 0, 8, coord[0], ValueType.DOUBLE)
    message = fill_bytes(message, 8, 16, coord[1], ValueType.DOUBLE)
    logger.info(
        "Sending UDP message to {}:{} with body {}".format(
            config.UDP_ENDPOINT_ADDRESS,
            config.UDP_ENDPOINT_PORT,
            message))
    s.sendto(message, addr)
    logger.info("Sent UDP Message to the UDP Broker")
    NetworkConnector().disconnect()
    logger.info("Going into deep sleep mode for [{} seconds]".format(config.GPS_TRACKING_INTERVAL_SECONDS))
    machine.deepsleep(config.GPS_TRACKING_INTERVAL_SECONDS * 1000)
