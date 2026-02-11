from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()


KAFKA_BOOTSTRAP_SERVER = config("KAFKA_BOOTSTRAP_SERVERS", cast=str)
KAFKA_TODO_TOPIC = config("TODO_TOPIC", cast=str)
KAFKA_CONSUMER_TODO_GROUP_ID = config("KAFKA_CONSUMER_TODO_GROUP_ID", cast=str)

OPENAI_API_KEY = config("OPENAI_API_KEY", cast=Secret)
SERPER_API_KEY = config("SERPER_API_KEY", cast=Secret)

SMTP_HOST = config("SMTP_HOST", cast=str)
SMTP_USER = config("SMTP_USER", cast=str)
SMTP_PASSWORD = config("SMTP_PASSWORD", cast=str)
EMAILS_FROM_EMAIL = config("EMAILS_FROM_EMAIL", cast=str)
SMTP_TLS = config("SMTP_TLS", cast=str)
SMTP_SSL = config("SMTP_SSL", cast=str)
SMTP_PORT = config("SMTP_PORT", cast=str)
EMAILS_FROM_NAME = config("EMAILS_FROM_NAME", cast=str)
emails_enabled = True
EMAILS_FROM_EMAIL = "mr.junaid@gmail.com"
