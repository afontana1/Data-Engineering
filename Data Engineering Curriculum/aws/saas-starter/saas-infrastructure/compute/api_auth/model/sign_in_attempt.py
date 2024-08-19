import time
from api_utils import ApiItem


class SignInAttempt(ApiItem):
    def __init__(self, pk: str = ""):
        super().__init__()
        self.pk = pk
        self.sk = "SIGN_IN_ATTEMPT"
        self.attempt: int = 0
        self.next_attempt_time: int = int(time.time())

    def serialize(self) -> dict:
        item = {
            "attempt": self.attempt,
            "next_attempt_time": self.next_attempt_time,
        }
        item.update(self.basic_keys())
        return item

    def deserialize(self, item: dict) -> "SignInAttempt":
        self.pk = str(item.get("pk"))
        self.sk = str(item.get("sk"))
        self.attempt = int(item.get("attempt", 0))
        self.next_attempt_time = int(item.get("next_attempt_time", 0))
        return self
