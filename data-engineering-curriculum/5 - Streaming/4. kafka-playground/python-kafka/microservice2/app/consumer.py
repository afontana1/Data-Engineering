from aiokafka import AIOKafkaConsumer
import logging
from app import settings

logging.basicConfig(level=logging.INFO)


async def consumer_book_order():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_BOOK_ORDER_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        value_deserializer=lambda v: v.decode('utf-8') if v else None,
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            logging.info(
                "{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(
                    msg.topic, msg.partition, msg.offset, msg.key, msg.value,
                    msg.timestamp)
            )
    finally:
        await consumer.stop()