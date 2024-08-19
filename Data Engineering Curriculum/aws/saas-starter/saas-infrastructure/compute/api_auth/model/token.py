import time
from typing import Union
import jwt

"""
Represents an Auth JWT token for a user's login session.
"""


class Token:

    TOKEN_DURATION_IN_HOURS = 24
    TOKEN_DURATION_SECONDS = TOKEN_DURATION_IN_HOURS * 3600

    def __init__(self, hash_key: str) -> None:
        self.hash_key: str = hash_key
        self.account_id: str = ""
        self.email: str = ""
        self.expiry_time: Union[int, None] = None

    def encode(self) -> str:
        token_str = jwt.encode(
            {
                "account_id": self.account_id,
                "email": self.email,
                "exp": int(
                    time.time() + Token.TOKEN_DURATION_SECONDS,
                ),
            },
            self.hash_key,
            algorithm="HS256",
        )
        return token_str

    def serialize(self) -> dict:
        return {
            "account_id": self.account_id,
            "email": self.email,
            "exp": self.expiry_time,
        }

    @staticmethod
    def decode(token_str: str, hash_key: str) -> "Token":
        payload = jwt.decode(token_str, hash_key, algorithms=["HS256"])
        token = Token(hash_key)
        token.account_id = payload.get("account_id")
        token.email = payload.get("email")
        token.expiry_time = int(payload.get("exp")) if "exp" in payload else None
        return token

    def __str__(self):
        return self.encode()
