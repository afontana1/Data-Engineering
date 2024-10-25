from starlette.config import Config
from starlette.datastructures import Secret


try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

KAFKA_BOOTSTRAP_SERVER = config("KAFKA_BOOTSTRAP_SERVER", cast=str)
KAFKA_BOOK_ORDER_TOPIC = config("KAFKA_BOOK_ORDER_TOPIC", cast=str)
KAFKA_CONSUMER_BOOK_GROUD_ID = config("KAFKA_CONSUMER_BOOK_GROUD_ID", cast=str)
KAFKA_FOOD_ORDER_TOPIC = config("KAFKA_FOOD_ORDER_TOPIC", cast=str)

DATABASE_URL = config("DATABASE_URL", cast=Secret)

TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)

POSTGRES_HOST = config("POSTGRES_HOST", cast=str)
POSTGRES_PORT = config("POSTGRES_PORT", cast=int)
POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_DB = config("POSTGRES_DB", cast=str)

KAFKA_CONNECT_URL = config("KAFKA_CONNECT_URL", cast=str)
