# -*- coding: utf-8 -*-
from nce.onboarding.onboard_service import OnBoardService
from nce.onboarding.onboard_status import OnBoardStatus
from nce.aws_iot.aws_iot_controller import AwsIotController
from nce.network.network_connector import NetworkConnector

from lib import logging
import config
import machine

logging.basic_config(level=logging.INFO)
logger = logging.get_logger("__main__")

if __name__ == '__main__':
    on_board_service = OnBoardService(endpoint=config.ON_BOARDING_URL,
                                      private_key_path=config.PRIVATE_KEY_PATH,
                                      certificate_pem_path=config.CERTIFICATE_PATH,
                                      root_ca_crt_path=config.ROOT_CA_PATH)
    response = on_board_service.on_board()
    if response.status == OnBoardStatus.ON_BOARD_SUCCESSFUL:
        logger.info("Successful on boarding")
        data = response.data
        controller = AwsIotController(aws_iot_endpoint=data["iotCoreEndpointUrl"],
                                      client_id=data["iccid"],
                                      client_certificate=config.CERTIFICATE_PATH,
                                      private_key=config.PRIVATE_KEY_PATH,
                                      root_ca=config.ROOT_CA_PATH,
                                      conn_disconnect_timeout=config.CONN_DISCONNECTION_TIMEOUT,
                                      mqtt_oper_timeout=config.MQTT_OPERATION_TIMEOUT)
        controller.initialize()
        logger.info("Subscribing to topic [{}]".format(config.MQTT_TOPIC_NAME))
        controller.subscribe(config.MQTT_TOPIC_NAME)
        logger.info("Publishing message to topic [{}]".format(config.MQTT_TOPIC_NAME))
        controller.publish(message='hello-world', topic=config.MQTT_TOPIC_NAME)
        logger.info("Unsubscribing from topic [{}]".format(config.MQTT_TOPIC_NAME))
        controller.unsubscribe(config.MQTT_TOPIC_NAME)
        logger.info("Closing the MQTT connection")
        controller.disconnect()
    else:
        logger.warning("On boarding failed with error: {}.".format(response.error))

    logger.info("Closing the network connection")
    NetworkConnector().disconnect()
    machine.idle()
