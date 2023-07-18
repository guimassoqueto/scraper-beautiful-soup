from os import getenv
from dotenv import load_dotenv

load_dotenv()

POSTGRES_PORT = getenv("POSTGRES_PORT") or 5432
POSTGRES_DB = getenv("POSTGRES_DB") or "postgres"
POSTGRES_USER = getenv("POSTGRES_USER") or "postgres"
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD") or "password"
POSTGRES_HOST = getenv("POSTGRES_HOST") or "127.0.0.1"
RABBITMQ_DEFAULT_USER = getenv("RABBITMQ_DEFAULT_USER") or "user"
RABBITMQ_DEFAULT_PASS = getenv("RABBITMQ_DEFAULT_PASS") or "password"
RABBITMQ_DEFAULT_HOST = getenv("RABBITMQ_DEFAULT_HOST") or "localhost"
RABBITMQ_RECEIVER_QUEUE = getenv("RABBITMQ_RECEIVER_QUEUE") or "scrapy-soup"
RABBITMQ_PUBLISHER_QUEUE = getenv("RABBITMQ_PUBLISHER_QUEUE") or "soup-puppet"
TIMESTAMP_FILE = getenv("TIMESTAMP_FILE") or "timestamp"
