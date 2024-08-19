from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import concurrent.futures
import json

import time
import functools
import boto3
import botocore

client_config = botocore.config.Config(
    max_pool_connections=25,
)


def get_from_s3_parralell(record: dict):
    """Get from S3"""
    s3_client = boto3.client("s3", **boto3_config)
    k = record.get("Key")
    if not k.split("/")[-1]:
        return
    data = s3_client.get_object(Bucket=BUCKET, Key=k)
    contents = json.loads(data["Body"].read())
    return contents


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


@timer
def main(entities):
    """
    DOES NOT WORK IN LAMBDA
    """
    results = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        future_data = {
            executor.submit(get_from_s3_parralell, record): record
            for record in entities
        }
        for future in as_completed(future_data):
            try:
                data = future.result()
                # logger.info('%r page is %d bytes' % (future_data[future], len(website_data)))
                results.append(data)
            except Exception as exc:
                logger.info(
                    "%r generated an exception: %s" % (future_data[future], exc)
                )
    return results


@timer
def concurrent_main(entities):
    """
    NO PERFORMANCE GAIN IN LAMBDA
    """
    data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(get_from_s3_parralell, record) for record in entities
        ]
        for future in futures:
            data.append(future.result())
    return data
