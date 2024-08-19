from base.auth_handler import AuthHandler
from account.sign_up_handler import SignUpHandler


class SignUpTestUserHandler(AuthHandler):
    def __init__(self):
        super().__init__()
        self.operation_name = "sign_up_test_user"
        self.schema = {"email", "password"}

    def handle_action(self, request_data: dict, event: dict, context: dict):
        sign_up_handler = SignUpHandler()

        # Force add TMP and CONFIRMED flags.
        request_data["flags"] += ["TMP", "AUTO_VERIFY"]
        return sign_up_handler.handle_action(request_data, event, context)
