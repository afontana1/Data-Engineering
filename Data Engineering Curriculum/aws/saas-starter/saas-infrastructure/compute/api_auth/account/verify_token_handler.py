from base.auth_handler import AuthHandler
from api_utils import api_response


class VerifyTokenHandler(AuthHandler):
    def __init__(self):
        super().__init__()
        self.operation_name = "verify_token"

    def handle_action(self, request_data: dict, event: dict, _context: dict):
        future_time = int(request_data.get("future_time", 0))
        token = self.verify_token(event, future_time)
        return api_response(
            200,
            f"Successfully verified token: {token.serialize()}",
            token.serialize(),
        )
