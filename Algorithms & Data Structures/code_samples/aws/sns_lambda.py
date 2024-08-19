import json
import logging
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

logger = logging.getLogger(__name__)


class Publish(object):
    def __init__(self, sns_arn: str):
        self.sns_client = boto3.client("sns")
        self.arn = sns_arn

    def publish_message_sns(
        self,
        source: str,
        message: str,
        severity: str,
        attributes: dict = {},
        *args,
        **kwargs
    ) -> bool:
        """Publishes messages to SNS.
        Args:
            message (str): error message to be emailed
            severity (str): HIGH, MEDIUM, LOW
        EXAMPLE:
            mesg = json.dumps({
                "default": "default",
                "body": "this is a test"
            })

            response = client.publish(
                TopicArn='',
                Message=mesg,
                MessageStructure='json',
                MessageAttributes={
                    'color': {
                        'DataType': 'String',
                        'StringValue': 'blue',
                    }
                }
            )
        """
        att_dict = {}
        if attributes:
            for key, value in attributes.items():
                if isinstance(value, str):
                    att_dict[key] = {"DataType": "String", "StringValue": value}
                elif isinstance(value, bytes):
                    att_dict[key] = {"DataType": "Binary", "BinaryValue": value}
        try:
            output = {
                "message_length": len(message),
                "received_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "message": message,
                "severity": severity,
                "source": source,
            }
            output.update(kwargs)

            response = self.sns_client.publish(
                TopicArn=self.arn,
                Message=json.dumps({"default": json.dumps(output)}),
                Subject="ALERT",
                MessageStructure="json",
                MessageAttributes=att_dict,
            )
            message_id = response["MessageId"]

        except ClientError:
            logger.exception("Couldn't publish message to topic %s.", self.arn)
            raise
        else:
            return message_id


def lambda_handler(event, context):
    # TODO: Schema Validation
    ARN = ""

    print(event)
    publisher = Publish(sns_arn=ARN)
    message = "This is a test notification"

    try:
        message_id = publisher.publish_message_sns(**event)
    except Exception as e:
        logger.exception("Error publishing")
        return {"status": 204}

    return {"status": 200, "message_id": message_id}
