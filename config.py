# -*- coding: utf-8 -*-
""""
    On boarding Configuration
"""
ON_BOARDING_URL = "https://device.connectivity-suite.cloud/device-api/onboarding"

""""
    Iot Core Configuration
"""
# Connection timeout in seconds
CONN_DISCONNECTION_TIMEOUT = 10
# MQTT Operation timeout in seconds
MQTT_OPERATION_TIMEOUT = 5

""""
    File location configuration
"""
# Private key file location on the PyCom device
PRIVATE_KEY_PATH = '/flash/client.private.key'
# Certificate file location on the PyCom device
CERTIFICATE_PATH = '/flash/client.cert.pem'
# Root CA file location on the PyCom device
ROOT_CA_PATH = '/flash/root-CA.crt'

""""
    UDP Endpoint configuration
"""
UDP_ENDPOINT_IP = "udp.connectivity-suite.cloud"
UDP_ENDPOINT_PORT = 4445
