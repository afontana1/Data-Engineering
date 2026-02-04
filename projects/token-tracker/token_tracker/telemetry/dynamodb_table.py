from __future__ import annotations

from decimal import Decimal
import os
from typing import Any, Dict, Optional

import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer


def _to_dynamo_value(value: Any) -> Any:
    if isinstance(value, bool):
        return value
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, list):
        return [_to_dynamo_value(v) for v in value]
    if isinstance(value, dict):
        return {k: _to_dynamo_value(v) for k, v in value.items()}
    return value


class DynamoDBTable:
    """
    Thin wrapper around boto3 DynamoDB client for telemetry writes.
    """

    def __init__(
        self,
        *,
        table_name: str,
        region_name: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
    ):
        self.table_name = table_name
        self._serializer = TypeSerializer()
        self._deserializer = TypeDeserializer()
        client_kwargs: Dict[str, Any] = {
            "region_name": region_name,
            "endpoint_url": endpoint_url,
        }
        # Only pass explicit credentials when both key+secret are present.
        # Otherwise let boto3 resolve credentials from its default chain.
        if aws_access_key_id and aws_secret_access_key:
            client_kwargs["aws_access_key_id"] = aws_access_key_id
            client_kwargs["aws_secret_access_key"] = aws_secret_access_key
            if aws_session_token:
                client_kwargs["aws_session_token"] = aws_session_token

        self._client = boto3.client("dynamodb", **client_kwargs)

    @classmethod
    def from_env(cls, *, table_name: str) -> "DynamoDBTable":
        access_key = os.getenv("AWS_ACCESS_KEY_ID") or os.getenv("AWS_ACCESS_KEY")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY") or os.getenv("AWS_SECRET_KEY")
        return cls(
            table_name=table_name,
            region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1",
            endpoint_url=os.getenv("AWS_DYNAMODB_ENDPOINT_URL"),
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        )

    def put_item(self, *, Item: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        serialized_item = {
            key: self._serializer.serialize(_to_dynamo_value(value))
            for key, value in Item.items()
        }
        return self._client.put_item(
            TableName=self.table_name,
            Item=serialized_item,
            **kwargs,
        )

    def scan(self, *, Limit: Optional[int] = None, **kwargs: Any) -> Dict[str, Any]:
        result = self._client.scan(TableName=self.table_name, Limit=Limit, **kwargs)
        items = [
            {key: self._deserializer.deserialize(value) for key, value in item.items()}
            for item in result.get("Items", [])
        ]
        result["Items"] = items
        return result
