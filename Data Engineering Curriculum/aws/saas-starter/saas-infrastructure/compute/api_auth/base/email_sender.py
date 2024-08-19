import boto3
from typing import List


class EmailSender:

    UTF8 = "UTF-8"

    def __init__(self):
        self.subject: str = "Untitled Email"
        self.source: str = ""
        self.text: str = ""
        self.html: str = ""
        self.reply_to: List[str] = []
        self.to_addresses: List[str] = []

    def send(self):
        client = boto3.client("ses")
        client.send_email(
            Source=self.source,
            Destination={
                "ToAddresses": self.to_addresses,
                "CcAddresses": [],
                "BccAddresses": [],
            },
            Message={
                "Subject": {"Data": self.subject, "Charset": self.UTF8},
                "Body": {
                    "Text": {"Data": self.text, "Charset": self.UTF8},
                    "Html": {"Data": self.html, "Charset": self.UTF8},
                },
            },
            ReplyToAddresses=self.reply_to,
        )
