import re
from api_utils import ApiException


class InputValidator:
    def __init__(self):
        pass

    def password(self, x: str):
        self._password_length(x)
        self._password_strength(x)

    def email(self, x: str):
        self._email_length(x)
        self.email_regex(x)

    def email_regex(self, email: str):
        regex = "[^@]+@[^@]+\.[^@]+"
        if not re.search(regex, email):
            self._fail(f"The email '{email}' is not a valid address.")

    def _password_length(self, x: str):
        min_length = 4
        max_length = 64

        if len(x) < min_length:
            self._fail(f"Password must be at least {min_length} characters.")

        if len(x) > max_length:
            self._fail(f"Password cannot be greater than {max_length} characters.")

    def _password_strength(self, x: str):

        has_digit = re.search(r"\d", x) is not None
        has_upper = re.search(r"[A-Z]", x) is not None
        has_lower = re.search(r"[a-z]", x) is not None

        if not (has_digit and has_upper and has_lower):
            self._fail(
                "Password not strong enough. It must contain at least one number, one lower-case, and one upper-case character."
            )

    def _email_length(self, x: str):
        min_length = 4
        max_length = 64

        if len(x) < min_length:
            self._fail(f"Email must be at least {min_length} characters.")

        if len(x) > max_length:
            self._fail(f"Email cannot be greater than {max_length} characters.")

    def _fail(self, reason: str):
        raise ApiException(400, reason)
