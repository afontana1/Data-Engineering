from api_utils.api_exception import ApiException
from api_utils.api_response import api_response
from api_utils.handler_event_extractor import *
import traceback


class ApiHandler:
    def __init__(self):
        self.schema: set = set()
        self.operation_name: str = "api_handler"

    def handle_action(self, request_data: dict, event: dict, context: dict):
        raise ApiException(500, "Action not implemented.")

    def handle(self, event, context=None):
        try:
            request_data = self._validate_request(event)
            return self.handle_action(request_data, event, context)
        except ApiException as e:
            return e.as_api_response()
        except Exception as e:
            trackback_message = traceback.format_exc(limit=5)
            return api_response(
                502, f"Unknown server error: {type(e)}: {e} \n\n {trackback_message}"
            )

    def _validate_request(self, event) -> dict:

        if "httpMethod" in event and event["httpMethod"].lower() == "get":
            request_data = extract_query_parameters(event)
        else:
            request_data = extract_json_body(event)

        for key in self.schema:
            if request_data is None or key not in request_data:
                raise ApiException(
                    400,
                    f"Invalid Request. Required key {key} not found in request body.",
                )

        return request_data
