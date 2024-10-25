from sqlmodel import SQLModel
from fastapi import HTTPException
import httpx
import logging
from app import settings

logging.basicConfig(level=logging.INFO)


class DebeziumConnectorConfig(SQLModel):
    name: str
    database_hostname: str
    database_port: int
    database_user: str
    database_password: str
    database_dbname: str
    database_server_name: str
    schema_include: str
    table_include_list: str
    kafka_bootstrap_servers: str
    kafka_schema_topic: str
    topic_prefix: str  # New field added


async def register_connector(config: DebeziumConnectorConfig):
    connector_config = {
        "name": config.name,
        "config": {
            "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
            "tasks.max": "1",
            "database.hostname": config.database_hostname,
            "database.port": str(config.database_port),
            "database.user": config.database_user,
            "database.password": config.database_password,
            "database.dbname": config.database_dbname,
            "database.server.name": config.database_server_name,
            "schema.include": config.schema_include,
            "table.include.list": config.table_include_list,
            "database.history.kafka.bootstrap.servers": config.kafka_bootstrap_servers,
            "database.history.kafka.topic": config.kafka_schema_topic,
            "topic.prefix": config.topic_prefix  # Add this line
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.KAFKA_CONNECT_URL}/connectors", json=connector_config)
        if response.status_code == 201:
            logging.info(f"Connector {config.name} registered successfully.")
        elif response.status_code == 409:
            logging.info(f"Connector {config.name} already exists.")
        else:
            logging.error(f"Failed to register connector: {response.text}")
            raise HTTPException(
                status_code=response.status_code, detail=response.text)


async def debzium_startup_event():
    config = DebeziumConnectorConfig(
        name="book-orders-connector",
        database_hostname=settings.POSTGRES_HOST,
        database_port=settings.POSTGRES_PORT,
        database_user=settings.POSTGRES_USER,
        database_password=str(settings.POSTGRES_PASSWORD),
        database_dbname=settings.POSTGRES_DB,
        database_server_name="dbserver1",
        schema_include="public",
        table_include_list="public.bookorder",  # DBT
        kafka_bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
        kafka_schema_topic=settings.KAFKA_BOOK_ORDER_TOPIC,
        topic_prefix="dbserver2"  # Set an appropriate topic prefix
    )
    await register_connector(config)
