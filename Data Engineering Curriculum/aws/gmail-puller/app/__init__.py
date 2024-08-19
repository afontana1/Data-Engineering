import get_gmail_messages
from util.bookmark import save_job_run_details, get_job_details, get_job_run_time_range
from get_gmail_messages import get_message_ids, get_messages, write_messages_to_s3
import os


def gmail_ingest_to_s3():
    bucket_name = os.environ.get("BUCKET_NAME")
    folder = os.environ.get("FOLDER")
    job_details = get_job_details("gmail_ingest")
    job_start_time, start_time_epoch, end_time_epoch = get_job_run_time_range(
        job_details
    )
    message_ids = get_message_ids(start_time_epoch, end_time_epoch)

    # Added logic to deal with the scenario of no emails in the given time range.
    if len(message_ids) > 0:
        messages = get_messages(message_ids)
        file_name = write_messages_to_s3(messages, bucket_name, folder)
    else:
        file_name = None
    save_job_run_details(
        job_details,
        job_start_time,
        message_ids,
        start_time_epoch,
        end_time_epoch,
        file_name,
    )


def lambda_handler(event, context):
    gmail_ingest_to_s3()
    return {"statusCode": 200, "body": "Data is loaded successfully"}
