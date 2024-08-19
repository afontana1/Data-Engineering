from base.auth_handler import AuthHandler
import stripe
from api_utils import api_response
import time
from model.user import User


def handle(event, context):
    return StripeWebhookHandler().handle(event, context)


class StripeWebhookHandler(AuthHandler):
    def __init__(self):
        super().__init__()
        self.operation_name = "stripe_webhook"
        stripe.api_key = "sk_test_dVPxaaBuDLylUmztkCmomO0p00dyqHOvDf"

    def handle_action(self, request_data: dict, event: dict, context: dict):

        try:
            stripe_event = stripe.Event.construct_from(request_data, stripe.api_key)
        except ValueError as e:
            # Invalid payload
            return api_response(400, f"Stripe Webhook Failed: {e}")

        print(f"Handling event: {stripe_event.type }")
        stripe_object = stripe_event.data.object
        client_reference_id = None
        new_expiry_time = None

        if stripe_event.type == "payment_intent.succeeded":
            print("Payment intent succeeded received")
        elif stripe_event.type == "payment_method.attached":
            print("Attached")
        elif stripe_event.type == "checkout.session.completed":
            print(f"Checkout complete: {stripe_object}")
            client_reference_id = stripe_object.get("client_reference_id", "unknown")
            new_expiry_time = self.enable_client_subscription(client_reference_id)

        elif stripe_event.type == "customer.subscription.updated":

            customer_id = stripe_object.get("customer", "unknown")
            cancel_at_period_end = stripe_object.get("cancel_at_period_end", False)
            self.update_user_auto_renew(customer_id, not cancel_at_period_end)

        elif stripe_event.type == "customer.subscription.deleted":

            customer_id = stripe_object.get("customer", "unknown")
            self.update_user_auto_renew(customer_id, False)

        elif stripe_event.type == "payment_intent.succeeded":
            print(f"Invoice Paid: {stripe_object}")

        else:
            print("Unhandled event type {}".format(stripe_event.type))

        print(f"Request data: {request_data}")
        response_payload = {
            "event_type": stripe_event.type,
            "client_id": client_reference_id,
            "new_expiry_time": new_expiry_time,
        }

        return api_response(
            200,
            "Stripe Webhook Success",
            response_payload,
        )

    def enable_client_subscription(self, client_reference_id: str):
        membership_days = 32
        days_to_seconds = 86400
        new_expiry_time = int(time.time() + membership_days * days_to_seconds)
        self.update_user_membership(client_reference_id, new_expiry_time)
        return new_expiry_time

    def update_user_membership(self, key: str, new_expiry_time: int):
        return self.user_database.update_item(
            pk=key,
            sk=User().sk,
            updated_values={"premium_expiry_time": new_expiry_time, "auto_renew": True},
        )

    def update_user_auto_renew(self, customer_id: str, active: bool):
        item = self.user_database_stripe_customer_index.get_item(
            customer_id, must_exist=True
        )
        return self.user_database.update_item(
            pk=item["pk"], sk=User().sk, updated_values={"auto_renew": active}
        )
