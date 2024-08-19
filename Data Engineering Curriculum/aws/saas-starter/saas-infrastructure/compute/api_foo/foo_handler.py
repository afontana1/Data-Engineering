from foo_handler_base import FooHandlerBase
from api_utils import api_response, extract_token


class FooHandler(FooHandlerBase):
    def __init__(self):
        super().__init__()
        self.operation_name = "foo"

    def handle_action(self, request_data: dict, event: dict, context: dict):

        # Check signed in and membership status.
        is_signed_in = self.is_signed_in(event)

        # If not member, fail.
        if is_signed_in:
            token = extract_token(event)
            is_account_verified = self.is_account_verified(token)
            is_premium = self.is_premium_member(token)
        else:
            is_premium = False
            is_account_verified = False

        response_payload = {
            "is_signed_in": is_signed_in,
            "is_premium": is_premium,
            "is_account_verified": is_account_verified,
        }

        return api_response(
            200,
            f"Successfully ran foo: {response_payload}",
            response_payload,
        )
