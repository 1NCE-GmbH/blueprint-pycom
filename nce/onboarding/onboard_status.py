# -*- coding: utf-8 -*-


class OnBoardStatus:
    """"
        On boarding statuses
    """

    """"
        Success Status
    """
    ON_BOARD_SUCCESSFUL = "SUCCESSFUL"

    """"
        Error status
    """
    ON_BOARD_FAILED_API_CALL = "API_CALL_FAILED"
    ON_BOARD_FAILED = "FAILED"


class OnBoardStatusResponse:

    def __init__(self, status, data=None, error=None):
        self.status = status
        self.data = data
        self.error = error
