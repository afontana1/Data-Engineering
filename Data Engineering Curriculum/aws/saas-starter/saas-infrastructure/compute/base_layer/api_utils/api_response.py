import json


def api_response(status_code: int, message: str, payload: dict = None):

    response_body = {"message": message}
    if payload is not None:
        response_body["payload"] = payload

    response_body_str = json.dumps(response_body)
    return {
        "statusCode": status_code,
        "body": response_body_str,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
    }
