import boto3
import urllib3
from botocore.exceptions import ClientError
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import concurrent.futures
import botocore

import shutil
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from config import config, config_no_verify


client_config = botocore.config.Config(
    max_pool_connections=25,
)


def download_object(version):
    """Downloads an object from S3 to local."""
    try:
        vers = version.get()
    except ClientError as e:
        print(e)
        return False

    path = version.object_key
    last_modified = vers.get("LastModified")
    version_id = vers.get("VersionId")
    date = f"{last_modified.year}.{last_modified.month}.{last_modified.day}"
    filename = path.rsplit("/")[-1]
    if not filename.endswith(".csv.gz"):
        return False

    file_directory = filename.split(".")[0]
    if not os.path.exists(f"backfill\\{file_directory}\\"):
        os.makedirs(f"backfill\\{file_directory}\\")

    with open(
        f"backfill\\{file_directory}\\{date}-{version_id}-{filename}", "wb"
    ) as fout:
        try:
            shutil.copyfileobj(vers.get("Body"), fout)
        except ClientError as e:
            print(e)
            print(f"version_id: {version_id}; last_modified: {date}; path: {filename}")

    return "Success"


def put_s3_object_parallel(path_to_file: bytes, Bucket: str, Key: str):
    """Put object in S3.

    Args:
        s3 (boto3 client): s3 client
        Body (bytes): bytes representation of data
        Bucket (str): S3 bucket
        Key (str): path to file
    Return:
        response
    """
    session = boto3.session.Session(**config_no_verify)
    s3 = session.client("s3", config=client_config, verify=False)
    with open(path_to_file, "rb") as f:
        response = s3.put_object(Body=f, Bucket=Bucket, Key=Key)
    return response


def download_parallel_multiprocessing(filename=""):
    s3 = boto3.resource("s3", **config)
    bucket = s3.Bucket(BUCKET)
    versions = bucket.object_versions.filter(Prefix=PATH + filename)

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_key = {
            executor.submit(download_object, version): version for version in versions
        }

        for future in futures.as_completed(future_to_key):
            key = future_to_key[future]
            exception = future.exception()

            if not exception:
                yield key, future.result()
            else:
                yield key, exception


def upload_files_parallel(args):
    """Parallel upload to S3.

    Args:
        args(tuple): Body, Bucket, Key
    """
    records = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        tracker_futures = []
        for arg in args:
            tracker_futures.append(
                executor.submit(lambda a: put_s3_object_parallel(*a), arg)
            )

        for future in concurrent.futures.as_completed(tracker_futures):
            records.append(future.result())
            tracker_futures.remove(future)
            del future

    return records


if __name__ == "__main__":
    ## for key, result in download_parallel_multiprocessing():
    ##     print(f"{key}: {result}")

    ##### set file_name = "" for processing all
    BUCKET = ""
    PATH = ""
    PATH_TO_UPLOAD = ""
    file_name = "{}.csv.gz"

    download_parallel_multiprocessing(filename=file_name)

    backfill_folder = "{}/"

    REQUIRED_TABLES = ["{}"]
    # Adjust the table parameter to backfill different folders or loop through a list

    for tab in REQUIRED_TABLES:
        table = f"{tab}/"
        path_to_local = backfill_folder + table

        arguments = []
        for fname in os.listdir(path_to_local):
            full_path_to_local = path_to_local + fname
            path_to_s3 = PATH_TO_UPLOAD + table + fname
            arguments.append((full_path_to_local, BUCKET, path_to_s3))
