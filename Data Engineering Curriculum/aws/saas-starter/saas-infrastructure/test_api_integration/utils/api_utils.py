import json
import uuid
from typing import Union, Set
from utils.api_response import ApiResponse
from utils.api_call import ApiCall


# Load the config JSON from root directory.
with open("./service.config.json", "r") as f:
    config_data = json.load(f)


DOMAIN = config_data["domain"]
API_ENDPOINT = f"https://api.{DOMAIN}/auth"
STRIPE_WEBHOOK_ENDPOINT = f"https://api.{DOMAIN}/stripe"

VALIDATION_EMAIL = f"auth.{DOMAIN}"  # Emails sent here get auto-validated.
AUTO_RESET_PASSWORD = "myAutoResetPasswordAB12!"

############################################
# API/Supporting functions
############################################


def new_api_call():
    return ApiCall(API_ENDPOINT)


def sign_up(
    email: str,
    password: str,
    expected_status: Union[int, Set[int], None] = 200,
    extra_flags: list = [],
):
    response = post_request(
        operation="sign_up",
        payload={"email": email, "password": password},
        extra_flags=extra_flags,
    )
    return assert_status(response, expected_status)


def sign_in(
    email: str,
    password: str,
    expected_status: Union[int, Set[int], None] = 200,
    flags: list = [],
):
    response = post_request(
        operation="sign_in",
        payload={"email": email, "password": password},
        extra_flags=flags,
    )
    return assert_status(response, expected_status)


def sign_up_test_user(user: str, password: str, expected_status: int = 200):
    return (
        new_api_call()
        .with_operation("sign_up_test_user")
        .with_payload({"email": user, "password": password})
        .expect_status(expected_status)
        .post()
    )


def sign_up_test_user_as_member(user: str, password: str, expected_status: int = 200):
    return (
        new_api_call()
        .with_operation("sign_up_test_user")
        .with_payload({"email": user, "password": password})
        .expect_status(expected_status)
        .with_extra_flags(["AUTO_MEMBER"])
        .post()
    )


def sign_in_future(
    email: str, password: str, expected_status: Union[int, Set[int], None] = 200
):
    # Sign in, but X days into the future (to test lock-out cooldown).
    return sign_in(email, password, expected_status, ["FUTURE"])


def sign_in_max_attempt(
    user: str, password: str, expected_status: Union[int, Set[int], None] = 200
):
    # Sign in, but X days into the future (to test lock-out cooldown).
    return sign_in(user, password, expected_status, ["MAX_ATTEMPT"])


def get_verification_status(
    token: str,
    expected_status: Union[int, Set[int], None] = 200,
    flags: list = [],
):
    response = post_request(
        operation="get_verification_status", payload={}, extra_flags=flags, token=token
    )
    return assert_status(response, expected_status)


def assert_status(
    response: ApiResponse, expected_status: Union[int, Set[int], None] = 200
):
    if expected_status is None:
        return response

    if type(expected_status) is int:
        assert response.status == expected_status
    elif type(expected_status) is Set:
        assert response.status in expected_status

    return response


def verify_token(
    token: str, expected_status: Union[int, Set[int], None] = 200, future_time: int = 0
):
    response = get_request(
        operation="verify_token", token=token, payload={"future_time": future_time}
    )
    return assert_status(response, expected_status)


def request_account_verification(
    account_id: str, expected_status: Union[int, Set[int], None] = 200
):
    payload = {"account_id": account_id}
    response = post_request(operation="request_account_verification", payload=payload)
    return assert_status(response, expected_status)


def request_account_reset(
    email: str, expected_status: Union[int, Set[int], None] = 200
):
    payload = {"email": email}
    response = post_request(operation="request_account_reset", payload=payload)
    return assert_status(response, expected_status)


def reset_account(
    reset_token: str,
    new_password: str,
    expected_status: Union[int, Set[int], None] = 200,
):
    payload = {"reset_token": reset_token, "new_password": new_password}
    response = post_request(operation="reset_account", payload=payload)
    return assert_status(response, expected_status)


def get_request(
    operation: str, payload: dict = {}, token: str = None, extra_flags: list = []
):
    return ApiCall.generic_request(
        API_ENDPOINT, "GET", operation, payload, token, extra_flags
    )


def post_request(
    operation: str, payload: dict = {}, token: str = None, extra_flags: list = []
):
    return ApiCall.generic_request(
        API_ENDPOINT, "POST", operation, payload, token, extra_flags
    )


def generate_random_email(base_domain: str = "no-op-test-email.com"):
    return f"test-user-{uuid.uuid4().hex[:12]}@{base_domain}"


def generate_random_password():
    return f"test-pass-1A-{uuid.uuid4().hex[:12]}"


def generate_random_customer_id():
    return f"cus_rand_{uuid.uuid4().hex[:12]}"
