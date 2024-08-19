import uuid
from api_utils import ApiItem


class OTPToken(ApiItem):
    def __init__(self):
        super().__init__()
        self.pk = uuid.uuid4().hex
        self.sk = "TOKEN.OTP"
        self.token: str = ""

    def serialize(self) -> dict:
        item = {
            "token": self.token,
        }
        item.update(self.basic_keys())
        return item

    def deserialize(self, item: dict) -> "OTPToken":
        self.pk = str(item.get("pk"))
        self.token = str(item.get("token"))
        return self


class AccountResetToken(OTPToken):
    def __init__(self):
        super().__init__()
        self.sk = "TOKEN.RESET"


class VerificationToken(OTPToken):
    def __init__(self):
        super().__init__()
        self.sk = "TOKEN.VERIFY"
