from confluent_kafka import Consumer, KafkaError
import logging
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)

###########
# KAFKA SETUP CONFIG
###########

# Kafka broker address and port - it's present in compose.yml
bootstrap_servers = 'broker:19092' # for internal communication between containers we use the service name and port

# You have to manually create this topic using Kafka UI
topic = 'purchases'  

# A random group id for Consumer
group_id = 'my-consumer-group'

# Initialize the Kafka consumer
consumer_config = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)
consumer.subscribe([topic])

async def consume_kafka():
    while True:
        msgs = consumer.consume(num_messages=10, timeout=1.0)
        for msg in msgs:
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    
                    logging.info('End of partition reached {0}/{1}'.format(msg.topic(), msg.partition()))
                else:
                    
                    logging.error('Error occurred: {0}'.format(msg.error().str()))
            else:
                logging.info('Received message: {0}'.format(msg.value().decode('utf-8')))
        await asyncio.sleep(0.1)  # Adding sleep to avoid busy waiting
