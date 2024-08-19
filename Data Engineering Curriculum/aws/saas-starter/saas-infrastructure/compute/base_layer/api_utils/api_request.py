from typing import Union, Set, List
import json
import urllib3
from api_utils.api_request_response import ApiRequestResponse


class ApiRequest:
    def __init__(self, endpoint: str) -> None:
        self.operation: str = ""
        self.expected_status_codes: Set[int] = {200}
        self.payload = {}
        self.extra_flags = []
        self.token: Union[None, str] = None
        self.endpoint: str = endpoint

    def with_operation(self, operation: str) -> "ApiRequest":
        self.operation = operation
        return self

    def with_token(self, token: str) -> "ApiRequest":
        self.token = token
        return self

    def with_payload(self, payload: dict) -> "ApiRequest":
        self.payload = payload
        return self

    def with_extra_flags(self, extra_flags: List[str]) -> "ApiRequest":
        self.extra_flags = extra_flags
        return self

    def expect_status(self, *status_codes: int) -> "ApiRequest":
        self.expected_status_codes = set(status_codes)
        return self

    def post(self) -> ApiRequestResponse:
        return self.call("POST")

    def get(self) -> ApiRequestResponse:
        return self.call("GET")

    def call(self, method: str) -> ApiRequestResponse:
        response = self.generic_request(
            endpoint=self.endpoint,
            method=method,
            operation=self.operation,
            payload=self.payload,
            token=self.token,
            extra_flags=self.extra_flags,
        )
        # assert response.status in self.expected_status_codes
        return response

    @staticmethod
    def generic_request(
        endpoint: str,
        method: str,
        operation: str,
        payload: dict = {},
        token: str = None,
        extra_flags: list = [],
    ) -> ApiRequestResponse:
        request_data = {
            "operation": operation,
            **payload,
            "flags": ["TMP"] + extra_flags,
        }

        if token:
            headers = {"Authorization": f"Bearer {token}"}
        else:
            headers = None

        http = urllib3.PoolManager()
        if method == "GET":
            response = http.request(
                method, endpoint, fields=request_data, headers=headers
            )
        else:
            encoded_request_data = json.dumps(request_data)
            print(f"Sending request {method} with data {encoded_request_data}.")
            response = http.request(
                method, endpoint, body=encoded_request_data, headers=headers
            )

        status = response.status
        response_data = json.loads(response.data.decode("utf-8"))
        print("Response:", status, response_data)
        return ApiRequestResponse(status, response_data)
