# -*- coding: utf-8 -*-
import machine
import ujson as json
import usocket as socket

import config
from lib import logging
from lib.microcoapy import coap_macros
from nce.coap.coap_service import CoapService
from nce.network.network_connector import NetworkConnector

logging.basic_config(level=logging.INFO)
logger = logging.get_logger("__main__")


def received_message_callback(packet, sender):
    logger.info('Message received: {}, from: {}'.format(packet.to_string(), sender))
    logger.info('Message payload: {}'.format(packet.payload.decode('unicode_escape')))


if __name__ == '__main__':
    connector = NetworkConnector()

    message = json.dumps({
        "test_message": "hello-world"
    })

    logger.info("Performing DNS Resolution for the CoAP endpoint [{}]".format(config.COAP_ENDPOINT_ADDRESS))
    address = socket.getaddrinfo(config.COAP_ENDPOINT_ADDRESS, config.COAP_ENDPOINT_PORT)[0][-1][0]

    client = CoapService()
    client.initialize(received_message_callback)
    message_id = client.post(address=address,
                             port=config.COAP_ENDPOINT_PORT,
                             path=config.COAP_ENDPOINT_PATH,
                             message=message,
                             query_options="?t={}".format(config.COAP_TOPIC_NAME),
                             content_format=coap_macros.COAP_CONTENT_FORMAT.COAP_APPLICATION_JSON)
    logger.info("Message ID [{}]".format(message_id))
    logger.info("Polling for new incoming messages on the CoAP Client")
    client.poll(config.COAP_POST_POLL_TIME)

    logger.info("Closing the network connection")
    connector.disconnect()
    machine.idle()
