from typing import Tuple, Union
from utils import *
import os
import json

from utils.api_utils import *
import time


def setup():
    pass


def test_create_payment_session():
    token, _ = create_user_token()
    create_payment_session(token)


def test_unpaid_membership_validation_fails():
    token, _ = create_user_token(generate_random_customer_id())
    verify_premium_status(token, 402)


def test_create_portal():
    token, _ = create_user_token()
    create_payment_portal(token)


def test_premium_membership_verification():
    setup_premium_membership()


def test_premium_membership_cancellation():
    token, customer_id = setup_premium_membership()
    trigger_subscription_cancel_at_end_event(customer_id)
    response = verify_premium_status(token, 200)
    assert response.from_payload("auto_renew") is False


def test_premium_membership_deletion():
    token, customer_id = setup_premium_membership()
    trigger_subscription_deleted_event(customer_id)
    response = verify_premium_status(token, 200)
    assert response.from_payload("auto_renew") is False


# =================================================
# Helper functions
# =================================================


def create_user_token(override_customer_id: str = None) -> Tuple[str, dict]:

    # User must be signed-up and signed in to create a payment session.
    user = generate_random_email()
    password = generate_random_password()

    flags = []
    if override_customer_id:
        flags.append(f"OVERRIDE_CUSTOMER_ID:{override_customer_id}")

    sign_up(user, password, 200, flags)
    response = sign_in(user, password, 200)
    return response.get_token(), response.get_token_payload()


def create_payment_session(token: str):
    return (
        new_api_call()
        .with_operation("create_payment_session")
        .with_token(token)
        .with_payload({"return_endpoint": "http://127.0.0.1:8000/app"})
        .post()
    )


def create_payment_portal(token: str):
    return (
        new_api_call()
        .with_operation("create_payment_portal")
        .with_token(token)
        .with_payload({"return_endpoint": "http://127.0.0.1:8000/app"})
        .post()
    )


def verify_premium_status(token: str, expected_status: int = 200):
    return (
        new_api_call()
        .with_operation("verify_premium_status")
        .with_token(token)
        .expect_status(expected_status)
        .post()
    )


def setup_premium_membership() -> Tuple[str, str]:

    customer_id = generate_random_customer_id()
    token, token_payload = create_user_token(customer_id)

    account_id = token_payload["account_id"]
    trigger_checkout_event(account_id)
    response = verify_premium_status(token, 200)

    assert int(response.from_payload("expiry_time")) > time.time()
    assert response.from_payload("auto_renew") is True

    return token, customer_id


# =================================================
# Webhook Helpers
# =================================================


def trigger_checkout_event(account_id: str):
    webhook_event = get_event("checkout.session.completed.json")
    webhook_event["data"]["object"]["client_reference_id"] = account_id
    trigger_event(webhook_event)


def trigger_subscription_deleted_event(customer_id: str):
    webhook_event = get_event("customer.subscription.deleted.json")
    webhook_event["data"]["object"]["cancel_at_period_end"] = True
    webhook_event["data"]["object"]["customer"] = customer_id
    trigger_event(webhook_event)


def trigger_subscription_cancel_at_end_event(customer_id: str):
    webhook_event = get_event("customer.subscription.updated.json")
    webhook_event["data"]["object"]["cancel_at_period_end"] = True
    webhook_event["data"]["object"]["customer"] = customer_id
    trigger_event(webhook_event)


def get_event(file_name: str):
    local_path = os.path.dirname(__file__)
    with open(f"{local_path}/sample_events/{file_name}", "r") as f:
        webhook_event = json.load(f)
    return webhook_event


def trigger_event(webhook_event: dict):
    return ApiCall(STRIPE_WEBHOOK_ENDPOINT).with_payload(webhook_event).post()
