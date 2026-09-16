import time
import asyncio
import argparse
import pandas as pd

from redisai import Client
import redis.asyncio as aredis


async def gather_with_concurrency(n, key_name, *records):
    semaphore = asyncio.Semaphore(n)

    async def load_record(key_name, record):
        async with semaphore:
            client = aredis.Redis(connection_pool=APOOL)
            key = record[key_name]
            record.pop(key_name)
            await client.hset(key, mapping=record)

    await asyncio.gather(*[load_record(key_name, record) for record in records])


async def load_features(df, key_name, workers=10):
    records = df.to_dict(orient="records")
    await gather_with_concurrency(workers, key_name, *records)


async def load_datasets(data_path):
    credit_dataset = pd.read_parquet(f"{data_path}/credit_history.parquet")
    zipcode_dataset = pd.read_parquet(f"{data_path}/zipcode_table.parquet")

    # drop catagorial features and unused features
    zipcode_dataset = zipcode_dataset.drop(
        columns=[
            "city",
            "state",
            "location_type",
            "event_timestamp",
            "created_timestamp",
        ]
    )
    credit_dataset = credit_dataset.drop(
        columns=["event_timestamp", "created_timestamp"]
    )
    await load_features(credit_dataset, "dob_ssn", workers=10)
    await load_features(zipcode_dataset, "zipcode", workers=10)


def load_model(model_path, rai_client):
    with open(model_path, "rb") as f:
        model_bytes = f.read()

    rai_client.modelstore(
        "loan_model", backend="ONNX", device="CPU", data=model_bytes, tag="v1"
    )


def load_script(script_path, rai_client):
    with open(script_path, "r") as f:
        script_bytes = f.read()

    rai_client.scriptstore(
        "get_loan_features",
        device="CPU",
        script=script_bytes,
        entry_points=["enrich_features"],
        tag="v1",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", help="Redis Server Host", type=str, default="127.0.0.1"
    )
    parser.add_argument(
        "-p", "--port", help="Redis Server Port", type=int, default=6379
    )
    parser.add_argument(
        "-d",
        "--data",
        help="Path to the datasets and models",
        type=str,
        default="/data",
    )
    args = parser.parse_args()

    RAI_CLIENT = Client(host=args.host, port=args.port)
    APOOL = aredis.ConnectionPool(host=args.host, port=args.port, max_connections=50)

    try:
        start = time.time()
        print("Loading datasets...")
        asyncio.run(load_datasets(args.data))
        print("Finished loading datasets in {} seconds".format(time.time() - start))
    except Exception as e:
        print("Failed to load datasets")
        raise e

    try:
        start = time.time()
        print("Loading models...")
        load_model(f"{args.data}/loan_model.onnx", RAI_CLIENT)
        load_script(f"./script.py", RAI_CLIENT)
        print("Finished loading models in {} seconds".format(time.time() - start))
    except Exception as e:
        print("Failed to load models")
        raise e
