#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import udf


@udf("string")
def munge_event(event_as_json):
    event = json.loads(event_as_json)
    event["Host"] = "Local"
    event["Cache-Control"] = "no-cache"
    return json.dumps(event)


def main():
    """main"""
    spark = SparkSession.builder.appName("ExtractEventsJob").getOrCreate()

    raw_events = (
        spark.read.format("kafka")
        .option("kafka.bootstrap.servers", "kafka:29092")
        .option("subscribe", "userItems")
        .option("startingOffsets", "earliest")
        .option("endingOffsets", "latest")
        .load()
    )

    munged_events = raw_events.select(
        raw_events.value.cast("string").alias("raw"),
        raw_events.timestamp.cast("string"),
    ).withColumn("munged", munge_event("raw"))
    munged_events.show()

    extracted_events = munged_events.rdd.map(
        lambda r: Row(timestamp=r.timestamp, **json.loads(r.munged))
    ).toDF()
    extracted_events.show()

    extracted_events.write.mode("overwrite").parquet("/tmp/extracted_events")

    default_hits = extracted_events.filter(extracted_events.event_type == "default")
    default_hits.show()

    default_hits.write.mode("overwrite").parquet("/tmp/default_hits")

    purchase_sword = extracted_events.filter(
        extracted_events.event_type == "purchase_sword"
    )
    purchase_sword.show()

    purchase_sword.write.mode("overwrite").parquet("/tmp/purchase_sword")

    join_guild = extracted_events.filter(extracted_events.event_type == "join_guild")
    join_guild.show()

    join_guild.write.mode("overwrite").parquet("/tmp/join_guild")

    coins = extracted_events.filter(extracted_events.event_type == "get_coins")
    coins.show()

    coins.write.mode("overwrite").parquet("/tmp/coins")


if __name__ == "__main__":
    main()
