from base.auth_handler import AuthHandler
from api_utils import api_response, ApiException
import urllib.parse


class CreatePaymentSessionHandler(AuthHandler):
    def __init__(self):
        super().__init__()
        self.operation_name = "create_payment_session"
        self.schema = {"return_endpoint"}

    def handle_action(self, request_data: dict, event: dict, context: dict):

        token = self.verify_token(event)
        account_id = token.account_id
        user = self.get_user_by_id(account_id)

        if user.stripe_customer_id is None:
            raise ApiException(404, "Payment customer ID not found for this customer!")

        return_endpoint = request_data.get("return_endpoint", None)
        if return_endpoint is None:
            return_endpoint = self.frontend_url

        # success_url = urllib.parse.urljoin(
        #     return_endpoint, f"premium_success?session_id={'{CHECKOUT_SESSION_ID}'}"
        # )

        profile_url = urllib.parse.urljoin(return_endpoint, "profile")

        checkout_session = self.get_stripe().checkout.Session.create(
            success_url=profile_url,
            cancel_url=profile_url,
            client_reference_id=account_id,
            customer=user.stripe_customer_id,
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": self.stripe_price_id,
                    "quantity": 1,
                }
            ],
        )

        response_payload = {"session_id": checkout_session["id"]}

        return api_response(
            200,
            "Successfully created payment session.",
            response_payload,
        )
