import time
import jwt
import os
import stripe

from api_utils import ApiHandler, ApiException, ApiDatabase, extract_json

from base.input_validator import InputValidator
from base.auth_exceptions import AuthExceptions
from base.email_sender import EmailSender

from model.user import User
from model.otp_token import VerificationToken
from model.token import Token


class AuthHandler(ApiHandler):

    EXPIRY_MINUTES = 60

    def __init__(self):
        super().__init__()

        # Environment load once.
        self.jwt_hash_key: str = os.environ["AUTH_SECRET"]
        self.email_source: str = os.environ["EMAIL_SOURCE"]
        self.endpoint: str = os.environ["ENDPOINT"]
        self.frontend_url: str = os.environ["FRONTEND_URL"]
        self.service_name: str = os.environ["SERVICE_NAME"]

        # Setup Stripe API Key
        stripe.api_key = os.environ["STRIPE_API_KEY"]
        self.stripe_price_id: str = os.environ["STRIPE_PRICE_ID"]

        # Validators.
        self.validator: InputValidator = InputValidator()

        # Set up the user database table.
        self.user_database: ApiDatabase = ApiDatabase.from_env("TABLE_NAME")
        self.user_database_email_index = self.user_database.from_index(
            "email_index", "email"
        )
        self.user_database_token_index = self.user_database.from_index(
            "token_index", "token"
        )
        self.user_database_stripe_customer_index = self.user_database.from_index(
            "stripe_customer_index", "stripe_customer_id"
        )

    def get_stripe(self):
        return stripe

    def new_email_sender(self):
        email_sender = EmailSender()
        email_sender.source = self.email_source
        return email_sender

    def get_user_by_email(self, email: str) -> User:
        try:
            payload = self.user_database_email_index.get_item(email.lower())
            return User().deserialize(payload)
        except ApiException as e:
            raise AuthExceptions.USER_NOT_FOUND if e.status_code == 404 else e

    def get_user_by_id(self, account_id: str) -> User:
        item = self.user_database.get_item_with_keys(account_id, "CREDENTIALS")
        return User().deserialize(item)

    def get_verification_status(self, account_id: str) -> bool:
        auth_user = self.get_user_by_id(account_id)
        return auth_user.verified

    def get_account_id_for_otp_token(self, otp_token: str):
        item = self.user_database_token_index.get_item(otp_token)
        return item["pk"]

    def update_user_verification(self, key: str):
        return self.user_database.update_item(
            pk=key, sk=User().sk, updated_values={"verified": True}
        )

    def is_test_user(self, email: str):
        return email.startswith("test-user")

    def put_verification_token(self, key: str, token: str, expiry_hours: int = 1):
        verification_token = VerificationToken()
        verification_token.pk = key
        verification_token.token = token
        verification_token.with_x_hour_expiry(expiry_hours)
        self.user_database.put_item(verification_token)

    def verify_token(self, event, future_time: int = 0) -> Token:
        try:
            headers = extract_json(event, "headers")
            auth_header = headers["Authorization"]
            token_str = auth_header.split(" ")[1]
        except Exception as e:
            raise AuthExceptions.MISSING_HEADER

        try:
            token = Token.decode(token_str, self.jwt_hash_key)
            self._validate_future_expiry(token, future_time)

        except jwt.ExpiredSignatureError as e:
            raise AuthExceptions.INVALID_TOKEN

        except Exception as e:
            raise AuthExceptions.INVALID_TOKEN

        return token

    def _validate_future_expiry(self, token: Token, future_time: int):
        # Additional check if token has expired: also code to simulate future times.
        if token.expiry_time is not None:
            future_time = max(0, future_time)
            comparison_time = time.time() + future_time
            if token.expiry_time < comparison_time:
                raise AuthExceptions.INVALID_TOKEN
