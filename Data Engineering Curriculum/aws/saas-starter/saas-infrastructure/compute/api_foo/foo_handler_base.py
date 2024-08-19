from api_utils import (
    ApiHandler,
    ApiDatabase,
    ApiRequest,
    ApiException,
    ApiDatabaseProjection,
    extract_token,
)

import os
import jwt


class FooHandlerBase(ApiHandler):
    def __init__(self):
        super().__init__()
        maybe_auth_endpoint = os.getenv("AUTH_ENDPOINT")
        assert maybe_auth_endpoint is not None
        self.auth_endpoint: str = maybe_auth_endpoint

        self.item_database: ApiDatabase = ApiDatabase.from_env("TABLE_NAME")
        self.type_index: ApiDatabaseProjection = self.item_database.from_index(
            "sk_index", "sk"
        )
        self.item_table = None

    def get_latest_items(self, count: int = 1):
        return self.type_index.get_items("POST", limit=count, reverse=True)

    def payload_from_token(self, token: str):
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload

    def is_signed_in(self, event: dict):
        try:
            token = extract_token(event)
            self.verify_token(token)
            return True
        except ApiException as e:
            return False

    def verify_token(self, token: str):
        response = (
            self.new_auth_request()
            .with_operation("verify_token")
            .with_token(token)
            .get()
        )

        if response.status != 200:
            raise ApiException(response.status, "Unable to validate account.")

        return response

    def validate_premium(self, token: str):
        if not self.is_premium_member(token):
            raise ApiException(403, "Not a member.")

    def is_premium_member(self, token: str):
        response = (
            self.new_auth_request()
            .with_operation("verify_premium_status")
            .with_token(token)
            .get()
        )
        return response.status == 200

    def is_account_verified(self, token: str):
        response = (
            self.new_auth_request()
            .with_operation("get_verification_status")
            .with_token(token)
            .get()
        )
        return response.status == 200 and response.from_payload("verified") is True

    def new_auth_request(self) -> ApiRequest:
        return ApiRequest(self.auth_endpoint)
