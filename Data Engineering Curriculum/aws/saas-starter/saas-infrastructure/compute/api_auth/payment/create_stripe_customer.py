import stripe


def create_stripe_customer(key: str, email: str):
    stripe.api_key = "sk_test_dVPxaaBuDLylUmztkCmomO0p00dyqHOvDf"
    customer = stripe.Customer.create(description=key, email=email)
    return customer.id
