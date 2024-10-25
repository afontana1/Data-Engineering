from behave import given, when, then
import requests

BASE_URL = "http://host.docker.internal:9900"


@given('the user exists with username "{username}" and password "{password}"')
def step_impl(context, username, password):
    data = {
    "username": username,
    "password": password
    }

    response = requests.post(f"{BASE_URL}/login", data=data)
    assert response.status_code == 200


@when('the user logs in with username "{username}" and password "{password}"')
def step_impl2(context, username, password):
    data = {
        "username": username,
        "password": password
        }
    response = requests.post(
        f"{BASE_URL}/login", data=data)
    context.token = response.json().get("access_token")
    assert response.status_code == 200


@then('the user should receive a token')
def step_impl3(context):
    assert context.token is not None
