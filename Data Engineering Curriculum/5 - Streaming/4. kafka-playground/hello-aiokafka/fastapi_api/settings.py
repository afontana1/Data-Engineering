import asyncio

KAFKA_BOOTSTRAP_SERVERS = "broker:19092"
KAFKA_TOPIC = "hello-topic"
KAFKA_CONSUMER_GROUP = "a-random-group-id"
loop = asyncio.get_event_loop()
