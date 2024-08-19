import json
import stripe
import time

# This is your real test secret API key.
stripe.api_key = "sk_test_dVPxaaBuDLylUmztkCmomO0p00dyqHOvDf"

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    payload = request.data
    event = json.loads(payload)
    event_type = event["type"]

    # Print the captured event.
    print(event)
    timestamp = int(time.time())
    with open(f"captured_{event_type}_{timestamp}.json", "w") as f:
        json.dump(event, f, indent=2)

    return jsonify(success=True)
