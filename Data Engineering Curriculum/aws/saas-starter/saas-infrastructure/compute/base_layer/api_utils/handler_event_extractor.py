import json
from api_utils.api_exception import ApiException


def extract_json_body(event):
    return extract_json(event, "body")


def extract_json(event, key: str):
    try:
        event_body = event[key]
        json_body = json.loads(event_body) if type(event_body) is str else event_body
    except Exception as e:
        raise ApiException(400, f"Unable to parse JSON data of {key}: {e}")
    return json_body


def extract_query_parameters(event):
    try:
        query_params = event["queryStringParameters"]
    except Exception as e:
        raise ApiException(400, f"Unable to parse query params: {e}")
    return query_params


def extract_token(event):
    try:
        headers = extract_json(event, "headers")
        auth_header = headers["Authorization"]
        return auth_header.split(" ")[1]
    except Exception as e:
        raise ApiException(401, "Missing Authorization header.")
