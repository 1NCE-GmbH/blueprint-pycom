# -*- coding: utf-8 -*-
from nce.onboarding.onboard_status import OnBoardStatusResponse, OnBoardStatus
from nce.onboarding.helper.file_helper import FileHelper
from nce.onboarding.download_root_ca import RootCaDownloader

from lib import logging, urequests as requests
import ujson as json


class OnBoardService:

    def __init__(self, endpoint, private_key_path, certificate_pem_path, root_ca_crt_path):
        self.logger = logging.get_logger(__name__)
        self.endpoint = endpoint
        self.private_key_path = private_key_path
        self.certificate_pem_path = certificate_pem_path
        self.root_ca_crt_path = root_ca_crt_path

    def on_board(self):
        """
            On boards the device, by loading and saving the needed data

        :return:OnboardStatusResponse Status of the on boarding
        """
        self.logger.info("Starting with on boarding of the device.")
        try:
            response = self._get_device_information()
        except BaseException as e:
            return OnBoardStatusResponse(OnBoardStatus.ON_BOARD_FAILED_API_CALL,
                                         error="An error occurred while performing an on board API call",
                                         data=e)
        if response.status_code != 200:
            return OnBoardStatusResponse(OnBoardStatus.ON_BOARD_FAILED,
                                         error="On boarding request failed, with status code {}.".format(
                                             response.status_code),
                                         data=response.content)
        self.logger.info("Successfully retrieved device information.")
        response_body = json.loads(response.content)
        if response_body.get("certificate") is None or response_body.get("privateKey") is None or \
                response_body.get("amazonRootCaUrl") is None or  \
                response_body.get("iotCoreEndpointUrl") is None or response_body.get("iccid") is None:
            self.logger.error("Required parameters are missing to perform on boarding.")
            return OnBoardStatusResponse(OnBoardStatus.ON_BOARD_FAILED,
                                         error="Required parameters are missing to perform on boarding.",
                                         data=response_body)

        try:
            root_ca = RootCaDownloader(response_body["amazonRootCaUrl"]).download()
        except BaseException as e:
            self.logger.error("Error while downloading the Root CA.", e)
            return OnBoardStatusResponse(OnBoardStatus.ON_BOARD_FAILED,
                                         error="Error while downloading the Root CA",
                                         data=e)
        self.logger.info("Successfully downloaded the root CA certificate.")
        self._save_data(private_key=response_body["privateKey"],
                        certificate=response_body["certificate"],
                        root_ca=root_ca)
        self.logger.info("Successfully saved all certificates and keys to the device.")
        return OnBoardStatusResponse(OnBoardStatus.ON_BOARD_SUCCESSFUL, data=response_body)

    def _get_device_information(self):
        """"
            Gets the device information.
        """
        return requests.get(self.endpoint, headers={})

    def _save_data(self, private_key, certificate, root_ca):
        """"
            Saves data to the device storage
        """
        self._save_private_key(private_key)
        self._save_certificate_pem(certificate)
        self._save_root_ca_crt(root_ca)

    def _save_private_key(self, data):
        """
            Saves the private key

        :param data: Private key data
        """
        FileHelper.write_file(data, self.private_key_path)

    def _save_certificate_pem(self, data):
        """
            Saves the certificate PEM

        :param data: Certificate data
        """
        FileHelper.write_file(data, self.certificate_pem_path)

    def _save_root_ca_crt(self, data):
        """
            Saves the Root CA certificate

        :param data: Root CA Certificate data
        """
        FileHelper.write_file(data, self.root_ca_crt_path)
