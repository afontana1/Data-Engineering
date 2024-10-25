from aiokafka import AIOKafkaConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from google.protobuf import descriptor_pb2
from google.protobuf.message_factory import MessageFactory
from google.protobuf.descriptor_pool import DescriptorPool
import requests

SCHEMA_REGISTRY_URL = "http://host.docker.internal:8081"
TOPIC_NAME = "todos"

def fetch_schema_from_registry(subject_name: str):
    response = requests.get(f"{SCHEMA_REGISTRY_URL}/subjects/{subject_name}/versions/latest")
    response.raise_for_status()
    schema_data = response.json()
    schema_string = schema_data["schema"]

    descriptor_proto = descriptor_pb2.FileDescriptorSet()
    descriptor_proto.MergeFromString(bytes(schema_string, 'utf-8'))

    pool = DescriptorPool()
    for file_descriptor_proto in descriptor_proto.file:
        pool.Add(file_descriptor_proto)

    file_descriptor = pool.FindFileByName(descriptor_proto.file[0].name)
    message_descriptor = file_descriptor.message_types_by_name['Todo']
    message_factory = MessageFactory(pool)
    return message_factory.GetPrototype(message_descriptor)

async def consume():
    schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    # Fetch the latest schema
    todo_message_class = fetch_schema_from_registry("todo-value")

    # Define the ProtobufDeserializer
    protobuf_deserializer = ProtobufDeserializer(
        todo_message_class, schema_registry_client, {'use.deprecated.format': False})

    consumer_conf = {
        'bootstrap.servers': 'broker:19092',
        'group.id': 'my-group',
        'value.deserializer': protobuf_deserializer,
        'schema.registry.url': SCHEMA_REGISTRY_URL
    }
    consumer = AIOKafkaConsumer(
        TOPIC_NAME, **consumer_conf)
    await consumer.start()

    try:
        async for msg in consumer:
            todo = msg.value
            print(f"Received message: {todo}")
    finally:
        await consumer.stop()

# Run the consumer
import asyncio
asyncio.run(consume())
