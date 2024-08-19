from typing import Union
import uuid
from api_utils import ApiItem
from model.token import Token


class User(ApiItem):
    def __init__(self):
        super().__init__()
        self.pk = uuid.uuid4().hex
        self.sk = "CREDENTIALS"
        self.email: str = ""
        self.hashed_password: str = ""
        self.verified: bool = False
        self.stripe_customer_id: Union[str, None] = None
        self.premium_expiry_time: int = 0
        self.auto_renew: bool = False

    def is_temp(self):
        return self.expiry_time is not None

    def serialize(self) -> dict:
        item = {
            "email": self.email,
            "hashed_password": self.hashed_password,
            "stripe_customer_id": self.stripe_customer_id,
            "verified": self.verified,
            "premium_expiry_time": self.premium_expiry_time,
            "auto_renew": self.auto_renew,
        }
        item.update(self.basic_keys())
        return item

    def deserialize(self, item: dict) -> "User":
        self.pk = str(item.get("pk"))
        self.email = str(item.get("email"))
        self.hashed_password = str(item.get("hashed_password"))
        self.verified = bool(item.get("verified"))
        self.stripe_customer_id = item.get("stripe_customer_id")
        self.premium_expiry_time = int(item.get("premium_expiry_time", 0))
        self.auto_renew = item.get("auto_renew", False)
        return self

    def get_token(self, hash_key: str) -> str:
        token = Token(hash_key)
        token.account_id = self.pk
        token.email = self.email
        return token.encode()
