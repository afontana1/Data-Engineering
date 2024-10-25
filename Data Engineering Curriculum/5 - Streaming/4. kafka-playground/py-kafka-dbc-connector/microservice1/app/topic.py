from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.errors import KafkaError, TopicAlreadyExistsError
import logging

from app import settings

# Logging configuration
logging.basicConfig(level=logging.INFO)

# NOTE: This function is not used in the current implementation
# KAFKABROKER VERSION COMPATIBILITY ISSUE
# ERROR: IncompatibleBrokerVersion: Kafka broker does not support the 'CreateTopicsRequest_v0' Kafka protocol.
# GOOD THING IS THAT PRODUCER / CONSUMER AUTO CREATES TOPIC
async def startup_topic_event():
    admin_client = AIOKafkaAdminClient(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER)
    try:
        topic1 = NewTopic(
            name="PET",
            num_partitions=3,
            replication_factor=1,
        )
        # Create topic if it doesn't exist
        await admin_client.create_topics(
            new_topics=[topic1], validate_only=False
        )
        logging.info(f"Topic '{"PET"}' created successfully.")
    except TopicAlreadyExistsError:
        logging.info(f"Topic '{"PET"}' already exists.")
    except KafkaError as e:
        logging.error(f"Failed to create topic '{"PET"}': {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        await admin_client.close()


