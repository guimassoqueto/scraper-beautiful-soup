from os import getenv
from dotenv import load_dotenv

load_dotenv()

POSTGRES_PORT = getenv("POSTGRES_PORT") or 5432
POSTGRES_DB = getenv("POSTGRES_DB") or "postgres"
POSTGRES_USER = getenv("POSTGRES_USER") or "postgres"
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD") or "password"
POSTGRES_HOST = getenv("POSTGRES_HOST") or "127.0.0.1"

NON_INSERTED_PIDS_FOLDER = getenv("NON_INSERTED_PIDS_FOLDER") or "./non_inserted_pids"