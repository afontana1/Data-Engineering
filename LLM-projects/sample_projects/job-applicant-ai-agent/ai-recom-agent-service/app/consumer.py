from aiokafka import AIOKafkaConsumer
from confluent_kafka.serialization import SerializationContext, MessageField, StringDeserializer
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer

from app.crewai_agent import get_user_input_and_provide_info

import logging

from app import settings
from app.utils import send_email

from __generated__.schemas import todo_pb2

logging.basicConfig(level=logging.INFO)


async def consume_todo_events():
    # Create a consumer instance.
    protobuf_deserializer = ProtobufDeserializer(
        todo_pb2.Todo, {'use.deprecated.format': False})
    string_deserializer = StringDeserializer('utf8')

    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TODO_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
        group_id=(settings.KAFKA_CONSUMER_TODO_GROUP_ID),
        auto_offset_reset='latest',
        key_deserializer=lambda v: string_deserializer(v),
        value_deserializer=lambda v: protobuf_deserializer(
            v, SerializationContext(settings.KAFKA_TODO_TOPIC, MessageField.VALUE))
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            logging.info(f"Received message: {message} CONTEXT: {
                message.value} on topic {message.topic}")
            # Here you can add code to process each message.
            suggestion = get_user_input_and_provide_info(message.value.content)
            logging.info(f"Suggestion: {suggestion}")

            # Send the email
            send_email(
                email_to=message.key,
                # A first 10 letters subject
                subject= message.value.content[:25] + "..." + message.topic,
                text_content=suggestion
            )
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
