from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)
TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)

KAFKA_BOOTSTRAP_SERVERS = config("KAFKA_BOOTSTRAP_SERVERS", cast=str)
KAFKA_TODO_TOPIC = config("KAFKA_TODO_TOPIC", cast=str)

SCHEMA_REGISTRY_URL = config("SCHEMA_REGISTRY_URL", cast=str)

AUTH_SERVER_URL = config("AUTH_SERVER_URL", cast=str)