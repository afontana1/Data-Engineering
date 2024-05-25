#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


def purchase_sword_event_schema():
    return StructType(
        [
            StructField("Accept", StringType(), True),
            StructField("Host", StringType(), True),
            StructField("User-Agent", StringType(), True),
            StructField(
                "attributes",
                StructType(
                    [
                        StructField("price", StringType(), True),
                        StructField("color", StringType(), True),
                        StructField("hit_points", StringType(), True),
                    ]
                ),
            ),
            StructField("event_type", StringType(), True),
            StructField("remote_addr", StringType(), True),
        ]
    )


def join_a_guild_event_schema():
    return StructType(
        [
            StructField("Accept", StringType(), True),
            StructField("Host", StringType(), True),
            StructField("User-Agent", StringType(), True),
            StructField(
                "attributes",
                StructType(
                    [
                        StructField("level", StringType(), True),
                        StructField("color", StringType(), True),
                    ]
                ),
            ),
            StructField("event_type", StringType(), True),
            StructField("remote_addr", StringType(), True),
        ]
    )


def get_coins_event_schema():
    return StructType(
        [
            StructField("Accept", StringType(), True),
            StructField("Host", StringType(), True),
            StructField("User-Agent", StringType(), True),
            StructField(
                "attributes", StructType([StructField("coins", StringType(), True)])
            ),
            StructField("event_type", StringType(), True),
            StructField("remote_addr", StringType(), True),
        ]
    )


@udf("boolean")
def is_sword_purchase(event_as_json):
    """udf for filtering events"""
    event = json.loads(event_as_json)
    if event["event_type"] == "purchase_sword":
        return True
    return False


@udf("boolean")
def is_join_a_guild(event_as_json):
    """udf for filtering events"""
    event = json.loads(event_as_json)
    if event["event_type"] == "join_a_guild":
        return True
    return False


@udf("boolean")
def is_coins(event_as_json):
    """udf for filtering events"""
    event = json.loads(event_as_json)
    if event["event_type"] == "get_coins":
        return True
    return False


def main():
    """main"""
    spark = SparkSession.builder.appName("ExtractEventsJob").getOrCreate()

    raw_events = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka:29092")
        .option("subscribe", "userItems")
        .load()
    )

    sword_purchases = (
        raw_events.filter(is_sword_purchase(raw_events.value.cast("string")))
        .select(
            raw_events.value.cast("string").alias("raw_event"),
            raw_events.timestamp.cast("string"),
            from_json(
                raw_events.value.cast("string"), purchase_sword_event_schema()
            ).alias("json"),
        )
        .select("raw_event", "timestamp", "json.*")
    )

    join_a_guild = (
        raw_events.filter(is_join_a_guild(raw_events.value.cast("string")))
        .select(
            raw_events.value.cast("string").alias("raw_event"),
            raw_events.timestamp.cast("string"),
            from_json(
                raw_events.value.cast("string"), join_a_guild_event_schema()
            ).alias("json"),
        )
        .select("raw_event", "timestamp", "json.*")
    )

    get_coins = (
        raw_events.filter(is_join_a_guild(raw_events.value.cast("string")))
        .select(
            raw_events.value.cast("string").alias("raw_event"),
            raw_events.timestamp.cast("string"),
            from_json(raw_events.value.cast("string"), get_coins_event_schema()).alias(
                "json"
            ),
        )
        .select("raw_event", "timestamp", "json.*")
    )

    sink1 = (
        sword_purchases.writeStream.format("parquet")
        .option("checkpointLocation", "/tmp/checkpoints_for_sword_purchases")
        .option("path", "/tmp/sword_purchases")
        .trigger(processingTime="10 seconds")
        .start()
    )

    sink2 = (
        join_a_guild.writeStream.format("parquet")
        .option("checkpointLocation", "/tmp/checkpoints_for_join_guild")
        .option("path", "/tmp/join_guild")
        .trigger(processingTime="10 seconds")
        .start()
    )

    sink3 = (
        get_coins.writeStream.format("parquet")
        .option("checkpointLocation", "/tmp/checkpoints_for_get_coins")
        .option("path", "/tmp/get_coins")
        .trigger(processingTime="10 seconds")
        .start()
    )

    sink1.awaitTermination()
    sink2.awaitTermination()
    sink3.awaitTermination()


if __name__ == "__main__":
    main()
