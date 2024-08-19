from api_utils import ApiException


class AuthExceptions:

    # 401
    AUTH_FAILURE = ApiException(401, "Incorrect password or email.")
    INVALID_TOKEN = ApiException(
        401, "Authentication token is invalid or has expired. Please sign in again."
    )
    MISSING_HEADER = ApiException(401, "Missing authentication header.")

    # 402
    MEMBERSHIP_NOT_VALID = ApiException(402, "Is not a premium member.")

    MEMBERSHIP_EXPIRED = ApiException(402, "Membership has expired.")

    # 404

    USER_NOT_FOUND = ApiException(404, "This email account does not exist.")
    KEY_NOT_FOUND = ApiException(404, "Items key not found in database.")
    TOKEN_NOT_FOUND = ApiException(
        404,
        "This token no longer or exists or has expired. Please request a new token.",
    )

    # 500

    DUPLICATE_ENTRIES_FOUND = ApiException(
        500, "Unexpected duplicate entries were found for this key."
    )

    # 400

    INVALID_EMAIL = ApiException(
        400, "This email is invalid. Please enter a valid email address."
    )
    USER_ALREADY_EXISTS = ApiException(
        400, "This email account has already been registered."
    )

    # 429
    TOO_MANY_FAILED_ATTEMPTS = ApiException(
        429,
        "Too many failed sign-in attempts. Please wait up to 24 hours before trying again.",
    )
