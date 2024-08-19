from api_utils import api_response
from foo_handler_base import FooHandlerBase


class FooGetPostsHandler(FooHandlerBase):
    def __init__(self):
        super().__init__()
        self.operation_name = "foo_get_posts"

    def handle_action(self, request_data: dict, event: dict, context: dict):

        # Write item to the DB.
        items = self.type_index.get_items("POST", limit=5, reverse=True)

        processed_items = []
        for item in items:
            processed_items.append(
                {
                    "content": item["primary_value"],
                    "account_id": item["account_id"],
                    "key": item["pk"],
                }
            )

        response_payload = {"items": processed_items}

        return api_response(
            200,
            f"Successfully ran my foo_get_posts: {response_payload}",
            response_payload,
        )
