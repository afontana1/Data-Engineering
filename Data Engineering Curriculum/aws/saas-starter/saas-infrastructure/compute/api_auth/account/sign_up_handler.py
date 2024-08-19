import bcrypt
import time

from typing import List
from payment.create_stripe_customer import create_stripe_customer
from verification.request_account_verification import request_account_verification
from api_utils import api_response, ApiException
from base.auth_handler import AuthHandler, User
from base.auth_exceptions import AuthExceptions


class SignUpHandler(AuthHandler):
    def __init__(self):
        super().__init__()
        self.operation_name = "sign_up"
        self.schema = {"email", "password"}

    def handle_action(self, request_data: dict, event: dict, context: dict):

        # Username/email should not be case sensitive.
        email = str(request_data["email"]).lower()
        password = request_data["password"]
        flags: List[str] = request_data["flags"] if "flags" in request_data else []

        # Validate at this user and password can be created.
        self.validator.email(email)
        self._validate_user_does_not_exist(email)
        self.validator.password(password)

        # Be careful with security because users can game these flags.
        should_expire = "TMP" in flags
        should_verify = "AUTO_VERIFY" in flags
        should_be_member = "AUTO_MEMBER" in flags

        user = User()
        user.email = email
        user.hashed_password = self._hashed_password(password)
        user.verified = should_verify
        user.stripe_customer_id = self._get_stripe_customer_id(user.pk, email, flags)
        user.premium_expiry_time = (
            int(time.time() + 3000) if should_be_member else int(0)
        )

        # Set expiry time if needed.
        if should_expire:
            user.with_1_hour_expiry()

        # Save user to DB.
        self.user_database.put_item(user)

        # Create verification token (if it's not auto-verified).
        if not should_verify:
            request_account_verification(self, email, user.pk)

        # Prepare the response.
        token = user.get_token(self.jwt_hash_key)
        response_payload = {"token": token}

        return api_response(
            200,
            f"Successfully process sign-up request for {user} and {user.hashed_password}"
            f"and token {token}. "
            f"Should the user expire: {should_expire}",
            response_payload,
        )

    def _get_stripe_customer_id(self, user_key: str, email: str, flags: List[str]):
        override_customer_id = None
        for flag in flags:
            if flag.startswith("OVERRIDE_CUSTOMER_ID"):
                override_customer_id = flag.split(":")[1]

        # Also create a Stripe customer to go with it.
        if override_customer_id:
            return override_customer_id
        else:
            return create_stripe_customer(user_key, email)

    def _validate_user_does_not_exist(self, email: str):
        try:
            self.get_user_by_email(email)
        except ApiException as e:
            if e.status_code == 404:
                return
        raise AuthExceptions.USER_ALREADY_EXISTS

    def _hashed_password(self, password: str) -> str:
        hashed_password = bcrypt.hashpw(str.encode(password), salt=bcrypt.gensalt())
        hashed_password_str = hashed_password.decode("utf-8")
        return hashed_password_str
