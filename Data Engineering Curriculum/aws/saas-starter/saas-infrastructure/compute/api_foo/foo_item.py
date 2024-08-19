from api_utils import ApiItem
import uuid
import time


class FooItem(ApiItem):
    def __init__(self, pk: str = "", sk: str = "item"):
        super().__init__()
        self.pk = uuid.uuid4().hex if pk is None else pk
        self.sk = sk
        self.account_id: str = ""
        self.primary_value = None

    def serialize(self) -> dict:
        timestamp = int(time.time())
        compound_key = f"{self.sk}-{self.account_id}"

        item = {
            "account_id": self.account_id,
            "compound_key": compound_key,
            "updated_time": timestamp,
            "primary_value": self.primary_value,
        }
        item.update(self.basic_keys())
        return item

    def deserialize(self, item: dict) -> "FooItem":
        self.pk = str(item.get("pk"))
        self.sk = str(item.get("sk"))
        self.account_id = str(item.get("account_id"))
        self.primary_value = item.get("primary_value")
        return self
