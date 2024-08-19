from utils.api_utils import *
import time


def test_sign_in_cooldown():

    # When I sign in fail too many times, I'm blocked for the next attempt.
    user = generate_random_email()
    password = generate_random_password()
    sign_up_test_user(user, password)

    # I can sign in 5 times before it locks.
    # But it MUST lock no later than after 10 times.
    max_attempts_until_locking = 7

    for i in range(max_attempts_until_locking):
        time.sleep(0.1)  # We shouldn't really need to sleep, but just in case.
        print(f"Attempt #{i}")
        sign_in(user, generate_random_password(), 401)


def test_sign_in_cooldown_recovery():
    # After waiting long enough, I should be able to sign in again.
    user = generate_random_email()
    password = generate_random_password()
    sign_up_test_user(user, password)

    # Max out the attempts.
    sign_in_max_attempt(user, generate_random_password(), 401)

    # Validate that it is rejected.
    sign_in(user, generate_random_password(), 401)

    # Sign in and spoof 24h into the future.
    sign_in_future(user, password, 200)


def test_successful_sign_in_resets_cooldown():

    user = generate_random_email()
    password = generate_random_password()
    sign_up_test_user(user, password)

    # Sign in a few times.
    for _ in range(3):
        response = sign_in(user, generate_random_password(), 401)

    # Sign in with the right password. This should show a non-zero attempt.
    response = sign_in(user, password)
    assert response.data["payload"]["attempt"] > 0

    # Sign in again. Attempt should be back at 0.
    response = sign_in(user, password)
    assert response.data["payload"]["attempt"] == 0


def test_token_expiry():
    # A token should expire within X days.

    user = generate_random_email()
    password = generate_random_password()
    sign_up_test_user(user, password)

    response = sign_in(user, password)
    token = response.get_token()
    future_time = 2 * 24 * 3600
    verify_token(token, 401, future_time)
