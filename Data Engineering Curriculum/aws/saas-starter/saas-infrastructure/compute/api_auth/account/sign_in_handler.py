from api_utils import api_response
from api_utils.api_exception import ApiException

from model.user import User
from model.sign_in_attempt import SignInAttempt
from base.auth_handler import AuthHandler
from base.auth_exceptions import AuthExceptions

import bcrypt
import time


class SignInHandler(AuthHandler):

    EXPIRY_24_HOURS = 86400
    MAX_SIGN_IN_ATTEMPTS = 5

    def __init__(self):
        super().__init__()
        self.operation_name = "sign_in"
        self.schema = {"email", "password"}

    def handle_action(self, request_data: dict, event: dict, context: dict):

        email = request_data["email"]
        password = request_data["password"]
        flags = request_data["flags"] if "flags" in request_data else []

        # Check if user exists.
        user = self.get_user_by_email(email)

        # Check if the future flag is enabled and usable by a tmp user.
        is_future = "FUTURE" in flags and user.is_temp()

        # Check if sign-in attempts aren't on cooldown.
        attempt = self._get_sign_in_attempt(user.pk)
        current_time = self.get_future_time() if is_future else time.time()
        attempt_count = attempt.attempt

        if current_time < attempt.next_attempt_time:
            raise AuthExceptions.TOO_MANY_FAILED_ATTEMPTS.with_appended_message(
                f" Future status: {is_future}, {flags}, {user.is_temp}"
            )
        else:
            # Reset the attempt count.
            if attempt_count >= self.MAX_SIGN_IN_ATTEMPTS:
                attempt_count = 0

        # Check if passwords match.
        is_valid = bcrypt.checkpw(
            str.encode(password), str.encode(user.hashed_password)
        )

        # If they don't, throw an Auth Failure, and update the sign-in attempts.
        if not is_valid:
            # Artificially max out the attempt count if flagged.
            if "MAX_ATTEMPT" in flags:
                attempt_count = self.MAX_SIGN_IN_ATTEMPTS
            self._validate_sign_in_attempts(user, attempt_count)
        else:
            # A valid sign-in attempt should reset the attempt count.
            self._reset_sign_in_attempts(user)

        # If they do, create a JWT and send it back.
        token = user.get_token(self.jwt_hash_key)
        response_payload = {"token": token, "attempt": attempt_count}

        return api_response(
            200,
            f"Successfully process sign-in request for {user} id {user.pk}"
            f"and token {token}. ",
            response_payload,
        )

    def _get_sign_in_attempt(self, key: str) -> SignInAttempt:
        try:
            item = self.user_database.get_item(SignInAttempt(key))
            return SignInAttempt().deserialize(item)
        except ApiException as e:
            if e.status_code == 404:
                return SignInAttempt()
            else:
                raise e

    def _reset_sign_in_attempts(self, user: User):
        self._put_sign_in_attempt(user, 0)

    def _validate_sign_in_attempts(self, user: User, attempt_count: int):
        current_attempt = attempt_count + 1
        remaining_attempts = self.MAX_SIGN_IN_ATTEMPTS - current_attempt

        self._put_sign_in_attempt(user, current_attempt)

        if remaining_attempts <= 3:

            if remaining_attempts == 1:
                message_override = "You have 1 attempt remaining."
            elif remaining_attempts <= 0:
                message_override = (
                    "Too many failed sign-in attempts. Please wait before trying again."
                )
            else:
                message_override = f"You have {remaining_attempts} attempts remaining."

            raise AuthExceptions.AUTH_FAILURE.with_appended_message(message_override)
        else:
            raise AuthExceptions.AUTH_FAILURE

    def _put_sign_in_attempt(self, user: User, attempt_count: int):

        attempt = SignInAttempt()
        attempt.pk = user.pk
        attempt.attempt = attempt_count
        attempt.next_attempt_time = self._get_sign_in_cooldown_expiry_seconds(
            attempt_count
        )
        attempt.with_24_hour_expiry()
        self.user_database.put_item(attempt)

    def _get_sign_in_cooldown_expiry_seconds(self, attempts: int):
        if attempts < self.MAX_SIGN_IN_ATTEMPTS:
            return 0
        return self.EXPIRY_24_HOURS

    def get_future_time(self):
        # Timestamp 7 days in the future.
        return time.time() + 7 * self.EXPIRY_24_HOURS
