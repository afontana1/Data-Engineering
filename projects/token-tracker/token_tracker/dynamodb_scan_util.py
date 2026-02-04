from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, List

import boto3
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv


def _deserialize_items(raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    deserializer = TypeDeserializer()
    return [
        {k: deserializer.deserialize(v) for k, v in raw_item.items()}
        for raw_item in raw_items
    ]


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    dotenv_candidates = [
        Path.cwd() / ".env",
        script_dir / ".env",
        script_dir.parent / ".env",
    ]
    loaded_env = None
    for candidate in dotenv_candidates:
        if candidate.exists():
            load_dotenv(dotenv_path=candidate)
            loaded_env = candidate
            break

    parser = argparse.ArgumentParser(description="Scan DynamoDB telemetry table and print diagnostics.")
    parser.add_argument("--table", default=os.getenv("TOKEN_TRACKER_DYNAMODB_TABLE", "telemetry"))
    parser.add_argument("--region", default=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1")
    parser.add_argument("--limit", type=int, default=10, help="Max number of items to print")
    parser.add_argument("--endpoint-url", default=os.getenv("AWS_DYNAMODB_ENDPOINT_URL"))
    args = parser.parse_args()

    print(f"Table: {args.table}")
    print(f"Region: {args.region}")
    print(f".env: {loaded_env if loaded_env else 'not found'}")
    if args.endpoint_url:
        print(f"Endpoint URL: {args.endpoint_url}")

    try:
        access_key = os.getenv("AWS_ACCESS_KEY_ID") or os.getenv("AWS_ACCESS_KEY")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY") or os.getenv("AWS_SECRET_KEY")
        session_token = os.getenv("AWS_SESSION_TOKEN")

        client_kwargs: Dict[str, Any] = {
            "region_name": args.region,
            "endpoint_url": args.endpoint_url,
        }
        if access_key and secret_key:
            client_kwargs["aws_access_key_id"] = access_key
            client_kwargs["aws_secret_access_key"] = secret_key
            if session_token:
                client_kwargs["aws_session_token"] = session_token

        print(f"CredentialSource: {'env-explicit' if access_key and secret_key else 'boto3-default-chain'}")
        client = boto3.client("dynamodb", **client_kwargs)

        desc = client.describe_table(TableName=args.table)["Table"]
        print(f"TableStatus: {desc.get('TableStatus')}")
        print(f"ItemCount (approx): {desc.get('ItemCount')}")
        print(f"KeySchema: {json.dumps(desc.get('KeySchema', []), default=str)}")

        resp = client.scan(TableName=args.table, Limit=args.limit)
        items = _deserialize_items(resp.get("Items", []))
        print(f"ScanCount: {resp.get('Count', 0)}")
        print(f"ScannedCount: {resp.get('ScannedCount', 0)}")
        print(f"HasMorePages: {'LastEvaluatedKey' in resp}")
        print("Items:")
        print(json.dumps(items, indent=2, default=str))
        return 0

    except PartialCredentialsError as exc:
        print(f"PartialCredentialsError: {exc}", file=sys.stderr)
        return 2
    except NoCredentialsError as exc:
        print(f"NoCredentialsError: {exc}", file=sys.stderr)
        return 2
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code")
        message = exc.response.get("Error", {}).get("Message")
        print(f"ClientError ({code}): {message}", file=sys.stderr)
        return 3
    except Exception as exc:
        print(f"UnexpectedError: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
