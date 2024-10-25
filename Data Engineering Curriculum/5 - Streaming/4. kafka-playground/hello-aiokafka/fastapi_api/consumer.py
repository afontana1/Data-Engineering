import logging
from aiokafka import AIOKafkaConsumer 
from fastapi_api.settings import loop, KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP, KAFKA_TOPIC

logging.basicConfig(level=logging.INFO)

async def consume():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id=KAFKA_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            logging.info(f"MSG: {msg}")
            logging.info(f"Consumed message: {msg.value.decode('utf-8')}")
    finally:
        await consumer.stop()
