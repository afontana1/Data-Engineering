from api_utils import extract_token, api_response
from foo_handler_base import FooHandlerBase
from foo_item import FooItem
import uuid


class FooWritePostHandler(FooHandlerBase):
    def __init__(self):
        super().__init__()
        self.operation_name = "foo_write_post"
        self.schema = {"content"}

    def handle_action(self, request_data: dict, event: dict, context: dict):

        # Get the payload (if authorized/authenticated).
        token = extract_token(event)
        self.verify_token(token)
        payload = self.payload_from_token(token)

        # Organize data to write.
        post_content = request_data["content"]
        flags = request_data["flags"] if "flags" in request_data else []
        should_expire = "TMP" in flags
        account_id = payload["account_id"]

        # Write item to the DB.
        post_id = uuid.uuid4().hex
        post_item = FooItem(post_id, "POST")
        post_item.account_id = account_id
        post_item.primary_value = post_content
        if should_expire:
            post_item.with_1_hour_expiry()

        self.item_database.put_item(post_item)
        response_payload = {"item_key": post_id}

        return api_response(
            200,
            f"Successfully ran my foo_write_post: {response_payload}",
            response_payload,
        )
