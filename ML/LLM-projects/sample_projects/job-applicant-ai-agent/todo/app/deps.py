from sqlmodel import Session
from aiokafka import AIOKafkaProducer
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from typing import Annotated, Any

from confluent_kafka.serialization import SerializationContext, MessageField, StringSerializer
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient

from app import settings
from app.db_eng import engine
from app.core import requests
from __generated__.schemas import todo_pb2

# Schema Registry configuration
schema_registry_conf = {'url': settings.SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Protobuf Serializer
protobuf_serializer = ProtobufSerializer(
    todo_pb2.Todo, schema_registry_client, {'use.deprecated.format': False})
string_serializer = StringSerializer('utf8')


# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        key_serializer=string_serializer,
        value_serializer=lambda v: protobuf_serializer(
            v, SerializationContext(settings.KAFKA_TODO_TOPIC, MessageField.VALUE))
    )
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

TodoProducerDep = Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]

def get_session():
    with Session(engine) as session:
        yield session

DBSessionDep = Annotated[Session, Depends(get_session)]

#####################
# Dependency Injection for Current Student
#####################

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user_dep(token: Annotated[str | None, Depends(oauth2_scheme)]):
    print(f"Token: {token}")
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = requests.get_current_user(token)
    return user

GetCurrentUserDep = Annotated[ Any, Depends(get_current_user_dep)]

def get_login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return requests.login_for_access_token(form_data)

LoginForAccessTokenDep = Annotated[dict, Depends(get_login_for_access_token)]
