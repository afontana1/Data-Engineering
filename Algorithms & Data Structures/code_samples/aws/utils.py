import requests
import collections
import functools
import boto3
from datetime import datetime, timedelta
from typing import Any, Callable, TypeVar, Optional, Callable
from concurrent.futures import as_completed
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import threading
import multiprocessing
import boto3
import logging as logger
import time
import botocore
from functools import wraps

config = {"aws_region": "", "aws_access_key_id": "", "aws_secret_access_key": ""}
BUCKET_NAME = ""

client_config = botocore.config.Config(
    max_pool_connections=25,
)

T = TypeVar("T")


def retry(exceptions, total_tries=4, initial_wait=0.5, backoff_factor=2):
    """
    calling the decorated function applying an exponential backoff.
    Args:
        exceptions: Exception(s) that trigger a retry, can be a tuple
        total_tries: Total tries
        initial_wait: Time to first retry
        backoff_factor: Backoff multiplier (e.g. value of 2 will double the delay each retry).
        logger: logger to be used, if none specified print
    """

    def retry_decorator(f):
        @wraps(f)
        def func_with_retries(*args, **kwargs):
            _tries, _delay = total_tries + 1, initial_wait
            while _tries > 1:
                try:
                    print(f"{total_tries + 2 - _tries}. try:", kwargs)
                    return f(*args, **kwargs)
                except exceptions as e:
                    _tries -= 1
                    print_args = args if args else "no args"
                    if _tries == 1:
                        msg = str(
                            f"Function: {f.__name__}\n"
                            f"Failed despite best efforts after {total_tries} tries.\n"
                            f"args: {print_args}, kwargs: {kwargs}"
                        )
                        print(msg)
                        raise
                    msg = str(
                        f"Function: {f.__name__}\n"
                        f"Exception: {e}\n"
                        f"Retrying in {_delay} seconds!, args: {print_args}, kwargs: {kwargs}\n"
                    )
                    print(msg)
                    time.sleep(_delay)
                    _delay *= backoff_factor

        return func_with_retries

    return retry_decorator


def cache(
    seconds: int, maxsize: int = 128, typed: bool = False
) -> Callable[..., Callable[..., T]]:
    def wrapper_cache(func: Any) -> Any:
        func = functools.lru_cache(maxsize=maxsize, typed=typed)(func)
        func.delta = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.delta

        @functools.wraps(func)
        def wrapped_func(*args: Any, **kwargs: Any) -> Any:
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.delta

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


@retry(Exception, total_tries=4, initial_wait=20)
def retry_requests(query_string: str, prod: bool = False):
    """Used in unpack_records to deal with occasional network issues"""
    try:
        r = requests.get(query_string, headers={})
        r.raise_for_status()
    except Exception as e:
        r = ""

    return r


@cache(seconds=3600)
def request(query_string: str, prod: bool = False) -> requests.models.Response:
    try:
        r = requests.get(query_string, headers={})
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        r = ""
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        r = ""
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        r = ""
    except requests.exceptions.RequestException as err:
        print("Something Else:", err)
        r = ""
    return r


def recurse(
    obj: dict, parent_key: bool = False, separator: str = "."
) -> collections.abc.Generator[str, str]:
    """Recurse through nested record, identify href for additional call.

    args:
        obj (dict): key-value mapping, complex object
    yield:
        new_key,value: new key of the nested record and corresponding object.
    """
    for key, value in obj.items():
        new_key = str(parent_key) + separator + key if parent_key else key
        if isinstance(value, dict):
            yield from recurse(value, new_key, separator)
        elif isinstance(value, (tuple, list)):
            for idx, x in enumerate(value):
                if isinstance(x, dict):
                    yield from recurse(x, new_key, separator)
                else:
                    yield (new_key + "." + str(idx), x)
        else:
            yield (new_key, value)


def get_all_s3_objects(s3, **base_kwargs):
    """Return metadata for all S3 objects in a bucket/path.

    Args:
        s3 (boto3 client): s3 client
        Bucket (str): S3 bucket
        Key (str): path to file
    Yield:
        Generator that returns S3 metadata
    """
    continuation_token = None
    while True:
        list_kwargs = dict(MaxKeys=1000, **base_kwargs)
        if continuation_token:
            list_kwargs["ContinuationToken"] = continuation_token
        response = s3.list_objects_v2(**list_kwargs)
        yield from response.get("Contents", [])
        if not response.get("IsTruncated"):
            break
        continuation_token = response.get("NextContinuationToken")


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer


def get_from_s3_parallel():
    pass


def put_s3_object_parallel():
    pass


@timer
def download_files_parallel(args):
    """
    Massive performance gain.
    """
    records = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2000) as executor:
        tracker_futures = []
        for arg in args:
            tracker_futures.append(
                executor.submit(lambda a: get_from_s3_parallel(*a), arg)
            )

    for future in concurrent.futures.as_completed(tracker_futures):
        records.append(future.result())
        tracker_futures.remove(future)
        del future

    return records


@timer
def upload_files_parallel(args):
    """Parallel upload to S3.

    Args:
        args(tuple): Body, Bucket, Key
    """
    records = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2000) as executor:
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


class S3Bucket:
    def __init__(self, list_to_send):
        self.list_to_send = list_to_send
        self.thread_local = threading.local()
        self.cpuCount = multiprocessing.cpu_count()

    def writeToS3(self, data):
        """Write payload to S3
        SCHEMA:
            {
                'folderName': "",
                'fileName': "",
                'fileContents': ""
            }
        """
        folderName = data.get("folderName")
        fileName = data.get("fileName")
        fileContents = data.get("fileContents")

        try:
            s3_client = boto3.resource("s3", **config)
            s3_object = s3_client.Object(BUCKET_NAME, folderName + "/" + fileName)
            s3_object.put(Body=fileContents)
        except Exception as e:
            logger.error("Failed to write to aws s3 bucket")
            logger.error(e)
        else:
            logger.info("Successfully wrote to aws s3 bucket")

    # thread pool for creating incidents via http request
    def send_all_files_to_s3(self):
        with ThreadPoolExecutor(max_workers=self.cpuCount) as executor:
            executor.map(self.writeToS3, self.list_to_send)
