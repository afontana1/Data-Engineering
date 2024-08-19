from typing import Dict
from api_utils.api_handler import ApiHandler
from api_utils.api_exception import ApiException


class ApiEntrypoint(ApiHandler):
    def __init__(self):
        self.schema = {"operation": True}
        self.operation_map: Dict[str, ApiHandler] = {}

    def with_operation(self, operation: str, handler: ApiHandler) -> "ApiEntrypoint":
        self.operation_map[operation] = handler
        return self

    def with_handler(self, handler: ApiHandler) -> "ApiEntrypoint":
        return self.with_operation(handler.operation_name, handler)

    def handle_action(self, request_data: dict, event: dict, context: dict):
        operation = request_data["operation"]
        if operation not in self.operation_map.keys():
            raise ApiException(400, f"Unknown operation: {operation}")

        operation_handler = self.operation_map[operation]
        return operation_handler.handle(event, context)
