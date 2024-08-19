from typing import Optional
from api_utils.api_response import api_response


class ApiException(Exception):
    def __init__(self, status_code: int, message: str, payload: Optional[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.payload = payload

    def as_api_response(self):
        return api_response(self.status_code, self.message, self.payload)

    def with_appended_message(self, extra_message: str):
        appended_message = " ".join([self.message, extra_message])
        return ApiException(self.status_code, appended_message, self.payload)

    def with_message(self, new_message: str):
        return ApiException(self.status_code, new_message, self.payload)

    def with_status(self, new_status: int):
        return ApiException(new_status, self.message, self.payload)
