# Saas Server Code and Infrastructure

This repository contains server-side code for a boilerplate SaaS project (including most of the AWS infrastructure). The service has basic authentication, authorisation, CRUD and payment functionality. It is intended to act as a stub for more complex projects.

See the live example here: [SaaS Starter Stack](https://saas-starter-stack.com/)

### Content

* [Capabilities](#capabilities)
* [API Overview](#api-overview)
* [Testing](#testing)
* [Developing](#developing)
* [Deployment](#deployment)

### Capabilities

* 🔒Custom built auth: users can sign-up, sign-in, reset password.
* 💳 Users can pay for a premium subscription via Stripe.
* 💬 Users can read and view Twitter-like posts.
* ✨ Service can check the status (verified, premium membership, validity) of a user's token (JWT).

### Production Considerations

Before you use this for production, please do a security review on all of the **auth** functionality. It was implemented as an example, and I'm sure there's still gaps in its security. Also make sure that your secret keys and API keys are not committed publicly with the code.

## API Overview

The service has three API endpoints.

* `auth`: Anything to do with user sign-ups, sign-ins, verification and payments.
* `foo`: An arbitrary CRUD API (which interacts with the `auth` service) acting as a stub for the actual service code.
* `stripe`: A Stripe webhook for payment functionality. Not intended to be called directly.

A base Lambda layer is included in all of these APIs. It contains some shared utility code, and installed libraries such as `jwt` and `bcrypt`.

### API Architecture

The APIs are serverless Python REST APIs, hosted as Lambda functions. They are integrated with an API Gateway. This will allow them to scale to usage.

For development simplicity and code-re-use, each API may be overloaded with multiple operations. For example, the same `auth` Lambda function handles both `sign_in` and `sign_up` operations. 

There is an 'entrypoint' Python script that delegates the request to the appropriate handler.

### API Operations

The `auth` and `foo` API expect the payload body of the request to contain the `operation` field, which specifies exactly which sub-handler will be executed. Each operation in turn will expect certain fields to exist in the payload.

#### Auth API Schema

| Operation Name                 | Request Schema                | Response Schema             |
| ------------------------------ | ----------------------------- | --------------------------- |
| `sign_up`                      | `{email, password}`           | `{token}`                   |
| `sign_up_test_user`            | `{email, password}`           | `{token}`                   |
| `sign_in`                      | `{email, password}`           | `{token, attempt}`          |
| `verify_token`                 | N/A                           | N/A                         |
| `get_verification_staus`       | N/A                           | `{account_id, verified}`    |
| `verify_account`               | `{verification_token}`        | `{account_id, verified}`    |
| `request_account_verification` | `{account_id}`                | N/A                         |
| `reset_account`                | `{reset_token, new_password}` | N/A                         |
| `request_account_reset`        | `{email}`                     | N/A                         |
| `verify_premium_status`        | N/A                           | `{expiry_time, auto_renew}` |
| `create_payment_session`       | `{return_endpoint}`           | `{session_id}`              |
| `create_payment_portal`        | `{return_endpoint}`           | `{session_url}`             |

Foo API Schema

| Operation Name   | Request Schema | Response Schema                                   |
| ---------------- | -------------- | ------------------------------------------------- |
| `foo`            | N/A            | `{is_signed_in, is_premium, is_account_verified}` |
| `foo_write_post` | `{content}`    | `{item_key}`                                      |
| `foo_get_post`   | `{key}`        | `[{key, content, account_id}]`                    |
| `foo_get_posts`  | N/A            | `[{key, content, account_id}, ...]`               |

### Database

Each API has a single DynamoDB database which it uses as persistent data-storage. The single table is overloaded with multiple "Global Secondary Indexes" for faster look-up. This database is fine for simple CRUD operations, and most auth operations, but not ideal for anything that has complex relationships. 

If we want to maintain a serverless architecture, we may need to consider something like [Fauna DB](https://fauna.com/) or [AWS Aurora](https://aws.amazon.com/rds/aurora).

## Development

#### Cloud Prerequisites

* Have [Node](https://nodejs.org/en/), npm, [Docker](https://www.docker.com/) and [Python](https://www.python.org/) set up on your machine.
* Setup an [AWS Account](https://aws.amazon.com/). 
* Install the AWS [CLI](https://aws.amazon.com/cli/) and [CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) (including [bootstrapping](https://docs.aws.amazon.com/cdk/latest/guide/bootstrapping.html) it against your account).
* Get [safe-listed for production traffic in SES](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html) in `us-east-1` (the default deployment region) for email functionality.
* [Register](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-register.html) a domain.
* Verify the domain in SES.
* Have a [Stripe](https://stripe.com) account set up (for payment integration). You will need a Stripe secret key (development) and a Price ID.

#### IDE Setup

I used VSCode to write this project, so it should mostly work out of the box. For Python's auto-complete, you might want to add these paths to the VSCode source paths:

```json
"python.analysis.extraPaths": [
    "./compute/auth",
    "./compute/base_layer"
]
```

#### Service Configuration

The configuration of the service is consolidated into one file, `service.config.json`. 

```json
{
  "name": "BoneService",
  "awsAccount": "535707483867",
  "awsRegion": "us-east-1",
  "domain": "bonestack.com",
  "prefix": "bonestack",
  "frontendUrl": "https://bonestack.com/app/",
  "stripeKey": "sk_test_dVPxaaBuDLylUmztkCmomO0p00dyqHOvDf",
  "stripePriceId": "price_1Ipw2ECCoJYujIqgPAGPkuYZ"
}

```

The `stripeKey` and `stripePriceId` are things you **don't want exposed** in a public repository, so if you are going to use this for production, I recommend finding a better way to manage those keys. In fact, its probably best to ignore this file in `git` and have it versioned some other way.

## Deployment

To deploy the infrastructure, you should be able to use the deployment script:

```bash
./deploy_cdk.sh
```

It will build the 'base layer' Lambda image, and then deploy everything else on top of that. You can also do those two things separately.

```bash
# First make sure the Dockerfile is up to date.
(cd ./compute/base_layer && ./generate_base_layer.sh)

# Then deploy the CDK application.
cdk deploy
```

### Docker Base Layer

The base layer `Dockerfile` sets up a container with Python, then installs the shared dependencies (and copies shared utility files) into the environment. It then zips up that environment as a `.zip` file for CDK to use as a base Lambda layer (so we don't have to package the dependency with each function separately).

## Testing

#### Running Integration Tests

This project doesn't use unit tests. Instead, it just skips straight to integration tests, which should offer a greater degree of confidence that the service is working.

This is implemented under `./test_api_integration/` as Python tests. You can run them (as a suite, or individually) with [pytest](https://docs.pytest.org/en/6.2.x/):

```bash
# Run all tests.
python -m pytest -s test_api_integration/*

# Run a test class.
python -m pytest -s test_api_integration/test_auth.py

# Run a specific test case.
python -m pytest -s test_api_integration/test_auth.py::test_sign_up
```

#### Testing Stripe Webhook

To trigger webhook events during testing, we basically just send a mock payload to the actual endpoint. In order to model the data, there is a script to capture and store the response received by the webhook for any event you are interested in.

First, run the response captor server (this will record and save the event payloads as a `json` file).

```bash
cd ./test_api_integration/stripe_webhook_response_captor
python -m flask run
```

Attach stripe to the app.

```bash
stripe listen --forward-to localhost:5000/webhook
```

Now trigger a Stripe event.

```bash
stripe trigger customer.subscription.updated
```

Now you can find the captured `json` response in the same folder, and copy it over to `sample_events` to be used as input for the integration tests.

**Note**: You will also need to configure the webhook on your Stripe dashboard, and specify which type of events it can listen for. Pass in the deployed Stripe API endpoint (typically `https://api.<yourservice>.com/stripe`) to the webhook.

References: [Stripe webhooks](https://stripe.com/docs/webhooks) | [Type of events](https://stripe.com/docs/api/events/types)

#### Email Auto-Validator

The email auto-validator is a Lambda function connected to your domain, used as part of testing to automatically interact with verification emails sent to a particular address (e.g. `test-user@auth.myservice.com`). It is deployed as part of the stack.

When you create an account whose domain matches the `VALIDATION_EMAIL`, the `email-validator` function will receive the email and automatically engage with the links within that email (e.g. to verify the account or reset the password).

This is purely to facilitate easier integration testing.

##### Additional Setup Required

Once the email validator Lambda is deployed, you also need to add a rule in the SES console to write
emails to the correct bucket, and to invoke the appropriate Lambda function.

* The recipient should be whatever is specified in the `api_utils.py` integration tests' `VALIDATION_EMAIL`. It is by default `auth.<your-service.com>`.
* The S3 bucket should be whatever was created by the `create-email-validator` function.
* The Lambda function should be the one created by `create-email-validator` function.
* Once you run the `test_auth.py` tests again, the tests requiring email validation should work.
