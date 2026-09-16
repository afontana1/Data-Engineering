import json
import requests

SERVER_ADDR = "127.0.0.1:8877"

request_features = {
    "zipcode": "12542",
    "dob_ssn": "19510613_1349",
    "age": 29,
    "income": 100000,
    "emp_length": 3,
    "loan_amount": 10000000,
    "int_rate": 7.2,
}
response = requests.post(
    f"http://{SERVER_ADDR}/v1/loan/predict", data=json.dumps(request_features)
)
data = json.loads(response.text)
print(
    "\nDecision: ",
    data["loan_decision"],
    "\n" "Probabilities",
    data["probabilities"],
    "\n",
)
