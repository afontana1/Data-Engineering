from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()
    
KAFKA_BOOTSTRAP_SERVER = config("KAFKA_BOOTSTRAP_SERVER", cast=str)
KAFKA_BOOK_ORDER_TOPIC = config("KAFKA_BOOK_ORDER_TOPIC", cast=str)
KAFKA_CONSUMER_BOOK_GROUD_ID = config("KAFKA_CONSUMER_BOOK_GROUD_ID", cast=str)