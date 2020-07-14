# -*- coding: utf-8 -*-
from nce.lte.network_connector import NetworkConnector
from lib import logging

""""

    Initial boot script, which starts the LTE connection on the device
    
"""

logging.basic_config(level=logging.INFO)

# Setup network connector
connector = NetworkConnector()
# Connect to 1nce LTE network
connector.connect()
