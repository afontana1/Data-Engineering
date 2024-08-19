import boto3
import pickle
import uuid
import pandas as pd
from googleapiclient.discovery import build


def get_creds():
    sm_client = boto3.client("secretsmanager", region_name="us-east-1")

    secret_token = sm_client.get_secret_value(SecretId="gmail_token")["SecretBinary"]
    creds = pickle.loads(secret_token)
    return creds


def get_users():
    creds = get_creds()
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)
    return service.users()


def get_message_ids(start_time_epoch, end_time_epoch):
    users = get_users()

    messages_ids = []
    next_page_token = None

    while True:
        if next_page_token:
            print(
                f"Processing in range between {start_time_epoch} and {end_time_epoch} using token {next_page_token}"
            )
            messages = (
                users.messages()
                .list(
                    userId="me",
                    q=f"after:{start_time_epoch} before:{end_time_epoch}",
                    pageToken=next_page_token,
                )
                .execute()
            )
            if messages.get("messages"):
                messages_ids += messages.get("messages")
            next_page_token = messages.get("nextPageToken")
        else:
            print(
                f"Processing in range between {start_time_epoch} and {end_time_epoch}"
            )
            messages = (
                users.messages()
                .list(
                    userId="me", q=f"after:{start_time_epoch} before:{end_time_epoch}"
                )
                .execute()
            )
            if messages.get("messages"):
                messages_ids = messages.get("messages")
            next_page_token = messages.get("nextPageToken")
        if next_page_token == None:
            break
    return messages_ids


def get_messages(message_ids):
    users = get_users()
    messages = []
    for message_id in message_ids:
        message = users.messages().get(userId="me", id=message_id["id"]).execute()
        messages.append(message)
    return pd.DataFrame(messages)


def write_messages_to_s3(messages_df, s3_bucket, s3_prefix):
    messages_df.to_json(
        f"s3://{s3_bucket}/{s3_prefix}/part-{uuid.uuid1()}.json",
        orient="records",
        lines=True,
    )
    print(
        f"Successfully saved messages to s3://{s3_bucket}/{s3_prefix}/part-{uuid.uuid1()}.json"
    )
