import datetime
import time
import boto3


def get_job_details(job_name):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("gmail_jobs")
    job_details = table.get_item(Key={"job_id": job_name})["Item"]
    return job_details


def get_job_run_time_range(job_details):
    job_start_time = int(time.mktime(datetime.datetime.now().timetuple()))
    if job_details.get("job_run_bookmark_details"):
        job_run_bookmark_details = job_details.get("job_run_bookmark_details")
        last_run_end_time_epoch = int(
            job_run_bookmark_details["last_run_end_time_epoch"]
        )
        last_run_diff = (
            datetime.datetime.now().date()
            - datetime.datetime.fromtimestamp(last_run_end_time_epoch).date()
        )
        if last_run_diff.days > 1:
            start_time_epoch = last_run_end_time_epoch
            end_time = datetime.datetime.fromtimestamp(
                last_run_end_time_epoch
            ).date() + datetime.timedelta(days=1)
            end_time_epoch = int(time.mktime(end_time.timetuple()))
        else:
            start_time_epoch = last_run_end_time_epoch
            end_time_epoch = int(time.mktime(datetime.datetime.now().timetuple()))
    else:
        baseline_days = int(job_details["baseline_days"])
        start_time = datetime.datetime.now().date() - datetime.timedelta(
            days=int(baseline_days)
        )
        end_time = start_time + datetime.timedelta(days=1)
        start_time_epoch = int(time.mktime(start_time.timetuple()))
        end_time_epoch = int(time.mktime(end_time.timetuple()))
    return job_start_time, start_time_epoch, end_time_epoch


def save_job_run_details(
    job_details,
    job_start_time,
    message_ids,
    start_time_epoch,
    end_time_epoch,
    file_name,
):
    dynamodb = boto3.resource("dynamodb")
    message_count = len(message_ids)
    if job_details.get("job_run_bookmark_details"):
        max_message_id = job_details.get("job_run_bookmark_details").get(
            "last_run_max_message_id"
        )
    if len(message_ids) > 0:
        max_message_id = max([message_id["id"] for message_id in message_ids])
    job_run_details_item = {
        "job_id": job_details["job_id"],
        "job_run_time": job_start_time,
        "job_run_bookmark_details": {
            "max_message_id": max_message_id,
            "start_time_epoch": start_time_epoch,
            "end_time_epoch": end_time_epoch,
        },
        "rows_processed": message_count,
        "file_name": file_name,
    }
    job_run_details_table = dynamodb.Table("gmail_job_run_details")
    job_run_details_table.put_item(Item=job_run_details_item)

    job_details_table = dynamodb.Table("gmail_jobs")
    job_details["job_run_bookmark_details"] = {
        "last_run_max_message_id": max_message_id,
        "last_run_start_time_epoch": start_time_epoch,
        "last_run_end_time_epoch": end_time_epoch,
    }
    job_details_table.put_item(Item=job_details)
