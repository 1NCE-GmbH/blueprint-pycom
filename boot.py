# -*- coding: utf-8 -*-
from nce.network.network_connector import NetworkConnector
from lib import logging

""""

    Initial boot script, which starts the LTE connection on the device
    
"""

logging.basic_config(level=logging.INFO)

connector = NetworkConnector()
connector.connect()
