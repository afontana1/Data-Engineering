from account import *
from account_reset import *
from verification import *
from premium_status import *
from payment import *
from api_utils import ApiEntrypoint


def handler(event, context=None):

    entry_point = (
        ApiEntrypoint()
        .with_handler(SignUpHandler())
        .with_handler(SignUpTestUserHandler())
        .with_handler(SignInHandler())
        .with_handler(VerifyTokenHandler())
        .with_handler(GetVerificationStatusHandler())
        .with_handler(VerifyAccountHandler())
        .with_handler(RequestAccountVerificationHandler())
        .with_handler(ResetAccountHandler())
        .with_handler(RequestAccountResetHandler())
        .with_handler(VerifyPremiumStatus())
        .with_handler(CreatePaymentSessionHandler())
        .with_handler(CreatePaymentPortalHandler())
    )

    return entry_point.handle(event, context)
