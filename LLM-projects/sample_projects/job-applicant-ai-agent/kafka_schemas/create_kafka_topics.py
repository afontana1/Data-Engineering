import asyncio
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.errors import KafkaError, TopicAlreadyExistsError, KafkaConnectionError

KAFKA_KAFKA_BOOTSTRAP_SERVERS = "kafka-1:19092,kafka-2:19092,kafka-3:19092"
KAFKA_TOPICS = ["todo", "recommendation"]
NUM_PARTITIONS = 3
REPLICATION_FACTOR = 3
RETRY_INTERVAL = 2.5  # seconds
MAX_RETRIES = 5

async def create_topic(admin_client, topic_name):
    topic = NewTopic(name=topic_name, num_partitions=NUM_PARTITIONS,
                     replication_factor=REPLICATION_FACTOR)
    try:
        await admin_client.create_topics([topic])
        print(f"Topic {topic_name} created")
    except TopicAlreadyExistsError:
        print(f"Topic {topic_name} already exists")
    except KafkaError as e:
        print(f"Failed to create topic {topic_name}: {e}")

async def main():
    for attempt in range(MAX_RETRIES):
        try:
            admin_client = AIOKafkaAdminClient(
                bootstrap_servers=KAFKA_KAFKA_BOOTSTRAP_SERVERS)
            await admin_client.start()
            try:
                tasks = [create_topic(admin_client, topic) for topic in KAFKA_TOPICS]
                await asyncio.gather(*tasks)
            finally:
                await admin_client.close()
            print("All topics created.")
            break  # Exit the loop if successful
        except KafkaConnectionError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying in {RETRY_INTERVAL} seconds...")
                await asyncio.sleep(RETRY_INTERVAL)
            else:
                print("Max retries reached. Exiting.")
                raise

if __name__ == "__main__":
    asyncio.run(main())
