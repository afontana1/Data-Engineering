from abc import ABC, abstractmethod
from typing import Union
from api_utils.api_exception import ApiException
import time


class ApiItem(ABC):
    def __init__(self):
        self.pk: str = "PK"
        self.sk: str = "SK"
        self.expiry_time: Union[int, None] = None
        self.last_activity: Union[int, None] = None

    @abstractmethod
    def serialize(self) -> dict:
        raise ApiException(500, f"Item serialization not implemented for {self}")

    @abstractmethod
    def deserialize(self, item: dict) -> "ApiItem":
        pass

    def with_expiry_time(self, expiry_time: int):
        self.expiry_time = expiry_time
        return self

    def with_1_hour_expiry(self):
        return self.with_x_hour_expiry(1)

    def with_24_hour_expiry(self):
        return self.with_x_hour_expiry(24)

    def with_x_hour_expiry(self, hours: int):
        self.expiry_time = int(time.time() + hours * 3600)
        return self

    def basic_keys(self) -> dict:
        basic_keys = {"pk": self.pk, "sk": self.sk, "last_activity": int(time.time())}
        if self.expiry_time is not None:
            basic_keys["expiry_time"] = self.expiry_time
        return basic_keys
