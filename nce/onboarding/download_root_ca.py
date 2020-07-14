# -*- coding: utf-8 -*-
from lib import logging, urequests as requests


class RootCaDownloader:

    def __init__(self, root_ca_url):
        self.logger = logging.get_logger(__name__)
        self.root_ca_url = root_ca_url

    def download(self):
        """
            Downloads the Amazon Root Certificate
        """
        return requests.get(self.root_ca_url).content
