from base.auth_handler import AuthHandler
import secrets


def request_account_verification(
    auth_handler: AuthHandler, email: str, account_key: str
):
    # Operation
    token = secrets.token_hex()
    auth_handler.put_verification_token(account_key, token)
    confirm_url: str = (
        f"{auth_handler.endpoint}?operation=verify_account&verification_token={token}"
    )
    confirm_frontend_url: str = f"{auth_handler.frontend_url}verify_account?key={token}"

    # Fire off the email.
    email_sender = auth_handler.new_email_sender()
    email_sender.subject = f"Confirm your account at {auth_handler.service_name}"
    email_sender.text = (
        f"Please click here to confirm your account: {confirm_frontend_url}"
    )
    email_sender.html = f"<div>Please click here to confirm your account: <a href='{confirm_frontend_url}'>Confirm Account</a></div>"
    email_sender.to_addresses = [email]
    email_sender.reply_to = []
    email_sender.send()

    return token, confirm_url
