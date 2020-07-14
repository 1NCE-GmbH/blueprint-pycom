# -*- coding: utf-8 -*-
from nce.onboarding.onboard_service import OnBoardService
from nce.onboarding.onboard_status import OnBoardStatus
from nce.aws_iot.aws_iot_controller import AwsIotController

from lib import logging
import config
import time

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
        controller.subscribe("hello-world")
        while 1:
            time.sleep(5.0)
    else:
        logger.warning("On boarding failed with error: {}.".format(response.error))
