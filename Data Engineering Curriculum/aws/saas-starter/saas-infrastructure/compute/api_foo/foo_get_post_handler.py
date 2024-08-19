from api_utils import api_response
from foo_handler_base import FooHandlerBase


class FooGetPostHandler(FooHandlerBase):
    def __init__(self):
        super().__init__()
        self.operation_name = "foo_get_post"
        self.schema = {"key"}

    def handle_action(self, request_data: dict, event: dict, context: dict):

        item_key = request_data["key"]

        # Get the item from table.
        item = self.item_database.get_item_with_keys(pk=item_key, sk="POST")
        processed_items = [
            {
                "content": item["primary_value"],
                "account_id": item["account_id"],
                "key": item["pk"],
            }
        ]

        response_payload = {"items": processed_items}

        return api_response(
            200,
            f"Successfully ran my foo_get_post: {response_payload}",
            response_payload,
        )
