import os
import boto3
import email
import re
import urllib3
import time
import json


def handle(event, context):
    EmailValidator().handle(event, context)


class EmailValidator:

    NEW_PASSWORD = "myAutoResetPasswordAB12!"

    def __init__(self):
        self.api_endpoint = os.getenv("API_ENDPOINT")

    def handle(self, event, context):
        print(f"Event Received: {event}")
        print(event)

        download_directory = os.getenv("FOLDER", "/test-downloads")
        bucket = os.getenv("BUCKET", "auth.bucket")

        key = self.extract_message_id(event)
        local_file = self.download_mail(bucket, key, download_directory)

        time.sleep(2)  # Give the DDB a bit of time to propagate.
        self.process_mail_body(local_file)

        return {"message": "Success!"}

    def extract_message_id(self, event):
        ses_notification = event["Records"][0]["ses"]
        return ses_notification["mail"]["messageId"]

    def download_mail(self, bucket: str, key: str, destination_folder: str):

        local_path = os.path.join(destination_folder, key)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder, exist_ok=True)

        s3_client = boto3.client("s3")
        s3_client.download_file(bucket, key, local_path)
        return local_path

    def process_mail_body(self, local_file: str):

        # Get the message body.
        body = self.get_message_body(local_file)
        print("Got Body: " + body)

        # Get the URL from the message body.
        urls = self.find_urls(body)
        print(f"Got URLS: {urls}")

        # Click each URL in the link.
        transformed_urls = [self.transform_api_url(x) for x in urls]
        transformed_urls = [x for x in transformed_urls if x is not None]
        print(f"Transformed URLS: {transformed_urls}")
        self.activate_urls(transformed_urls)
        print("Email Processing Completed")

    def get_message_body(self, local_email_file: str):
        with open(local_email_file, "r") as f:
            message = email.message_from_file(f)
        if message.is_multipart():
            parts = []
            for part in message.walk():
                if part.get_content_type() in ("text/plain"):
                    parts.append(part.get_payload())
            body = "".join(parts)
        else:
            body = message.get_payload()
        return body

    def find_urls(self, body: str):
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, body)
        return [x[0] for x in url]

    def activate_urls(self, urls: str):
        http = urllib3.PoolManager()
        for url in urls:
            response = http.request("GET", url)
            print(f"URL Response {url}: {response.status}")
            response_data = json.loads(response.data.decode("utf-8"))
            print(response_data)

    def transform_api_url(self, url: str):
        # Transforms the API URL to something our validator can click to simulate the operation.
        # This is hard-coded and depends on the APIs defined in the compute folder.

        if "reset_password" in url:
            return self.transform_reset_account_url(url)

        if "verify_account" in url:
            return self.transform_verify_account_url(url)

        return None

    def transform_reset_account_url(self, url: str):

        # Extract URL parameters to a map.
        params_map = self.extract_params(url)
        key = params_map["key"]
        new_url = f"https://{self.api_endpoint}/auth?operation=reset_account&reset_token={key}&new_password={self.NEW_PASSWORD}"
        return new_url

    def transform_verify_account_url(self, url: str):

        # Extract URL parameters to a map.
        params_map = self.extract_params(url)
        key = params_map["key"]
        new_url = f"https://{self.api_endpoint}/auth?operation=verify_account&verification_token={key}"
        return new_url

    def extract_params(self, url: str):
        # Extract URL parameters to a map.
        params_list = url.split("?")[1].split("&")
        params_map = {x.split("=")[0]: x.split("=")[1] for x in params_list}
        return params_map
