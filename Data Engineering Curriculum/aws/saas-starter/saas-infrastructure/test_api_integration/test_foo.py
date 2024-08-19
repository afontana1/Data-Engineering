from utils.api_utils import *

FOO_ENDPOINT = f"https://api.{DOMAIN}/foo"


def new_foo_call():
    return ApiCall(FOO_ENDPOINT)


def test_foo():
    response = new_foo_call().with_operation("foo").expect_status(200).post()
    assert response.from_payload("is_signed_in") is False
    assert response.from_payload("is_premium") is False
    assert response.from_payload("is_account_verified") is False


def test_foo_signed_in():
    token = create_user_token()
    response = (
        new_foo_call().with_operation("foo").with_token(token).expect_status(200).post()
    )
    assert response.from_payload("is_signed_in") is True
    assert response.from_payload("is_premium") is False
    assert response.from_payload("is_account_verified") is True


def test_foo_member():
    token = create_user_token(is_member=True)
    response = (
        new_foo_call().with_operation("foo").with_token(token).expect_status(200).post()
    )
    assert response.from_payload("is_signed_in") is True
    assert response.from_payload("is_premium") is True
    assert response.from_payload("is_account_verified") is True


def test_foo_write_and_get_posts():
    token = create_user_token()
    random_content = f"Hello Random Content {uuid.uuid4().hex[:6]}"

    write_response = (
        new_foo_call()
        .with_operation("foo_write_post")
        .with_token(token)
        .with_payload({"content": random_content})
        .post()
    )

    assert write_response.from_payload("item_key") is not None
    item_key = write_response.from_payload("item_key")

    # Now try to get the same item.
    item_response = new_foo_call().with_operation("foo_get_posts").get()

    # Check it is returned in the batch.
    posts = item_response.from_payload("items")
    latest_post = posts[0]
    assert latest_post["content"] == random_content

    # Check that we can get the item directly.
    item_response = (
        new_foo_call()
        .with_operation("foo_get_post")
        .with_payload({"key": item_key})
        .get()
    )
    posts = item_response.from_payload("items")
    latest_post = posts[0]
    assert latest_post["content"] == random_content


def test_foo_non_member_cannot_post():
    random_content = f"Hello Random Content {uuid.uuid4().hex[:6]}"
    (
        new_foo_call()
        .with_operation("foo_write_post")
        .with_payload({"content": random_content})
        .expect_status(401)
        .post()
    )


# =================================================
# Helper functions
# =================================================


def create_user_token(is_member: bool = False):
    # User must be signed-up and signed in to create a payment session.
    user = generate_random_email()
    password = generate_random_password()

    if is_member:
        sign_up_test_user_as_member(user, password)
    else:
        sign_up_test_user(user, password)

    sign_in_response = sign_in(user, password)
    token = sign_in_response.get_token()
    return token
