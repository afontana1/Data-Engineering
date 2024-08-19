from base.auth_handler import AuthHandler
from base.auth_exceptions import AuthExceptions
from api_utils import api_response
from model.user import User
import time


class VerifyPremiumStatus(AuthHandler):
    def __init__(self):
        super().__init__()
        self.operation_name = "verify_premium_status"

    def handle_action(self, request_data: dict, event: dict, context: dict):

        token = self.verify_token(event)
        user = self.get_user_by_id(token.account_id)
        self._verify_premium_status(user)

        response_payload = {
            "expiry_time": user.premium_expiry_time,
            "auto_renew": user.auto_renew,
        }

        return api_response(
            200,
            f"Successfully verified premium status: {response_payload}",
            response_payload,
        )

    def _verify_premium_status(self, user: User):
        if int(time.time()) > user.premium_expiry_time:
            raise AuthExceptions.MEMBERSHIP_NOT_VALID
