# -*- coding: utf-8 -*-
""""
    On boarding Configuration
"""
ON_BOARDING_URL = 'https://device.connectivity-suite.cloud/device-api/onboarding'

""""
    Iot Core Configuration
"""
# Connection timeout in seconds
CONN_DISCONNECTION_TIMEOUT = 5
# MQTT Operation timeout in seconds
MQTT_OPERATION_TIMEOUT = 5
#Topic Name
MQTT_TOPIC_NAME = 'hello-world'

""""
    File location Configuration
"""
# Private key file location on the PyCom device
PRIVATE_KEY_PATH = '/flash/client.private.key'
# Certificate file location on the PyCom device
CERTIFICATE_PATH = '/flash/client.cert.pem'
# Root CA file location on the PyCom device
ROOT_CA_PATH = '/flash/root-CA.crt'

""""
    UDP Endpoint Configuration
"""
UDP_ENDPOINT_ADDRESS = 'udp.connectivity-suite.cloud'
UDP_ENDPOINT_PORT = 4445

""""
    CoAP Server Configuration
"""
COAP_SERVER_PORT = 5683
COAP_POST_POLL_TIME = 2000

""""
    CoAP Endpoint Configuration
"""
COAP_ENDPOINT_ADDRESS = 'coap.connectivity-suite.cloud'
COAP_ENDPOINT_PORT = 5683
COAP_TOPIC_NAME = 'hello-world'
COAP_ENDPOINT_PATH = '/'

""""
    Translation Location
"""
GPS_TRANSLATION_DATA_PATH = '/flash/nce/translator/gps_data.txt'
ENV_DATA_COLLECTOR_TRANSLATION_DATA_PATH = '/flash/nce/translator/env_data_coll_data.txt'

""""
    Message Interval
"""
MESSAGE_INTERVAL_SECONDS = 60

""""
    GPS Tracking Configuration
"""
GPS_TRACKING_INTERVAL_SECONDS = 300
