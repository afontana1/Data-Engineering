import bcrypt
from base.auth_handler import AuthHandler
from api_utils import api_response
from model.user import User
from model.otp_token import AccountResetToken


class ResetAccountHandler(AuthHandler):
    def __init__(self):
        super().__init__()
        self.operation_name = "reset_account"
        self.schema = {"reset_token", "new_password"}

    def handle_action(self, request_data: dict, event: dict, context: dict):

        otp_token = request_data.get("reset_token")
        new_password = request_data.get("new_password")
        assert otp_token is not None
        assert new_password is not None

        # Validator
        self.validator.password(new_password)

        # Update the hashed password.
        account_id = self.get_account_id_for_otp_token(otp_token)
        hashed_password = bcrypt.hashpw(str.encode(new_password), salt=bcrypt.gensalt())
        hashed_password_str = hashed_password.decode("utf-8")

        self.user_database.update_item(
            account_id, User().sk, {"hashed_password": hashed_password_str}
        )
        self.user_database.delete_item_with_keys(otp_token, AccountResetToken().sk)

        return api_response(
            200,
            f"Password reset success for [{account_id}]",
            {},
        )
