import psycopg2
from threading import Lock


def upsert_query(table: str, item: dict) -> str:
    insert = f"INSERT INTO {table}("
    values = "VALUES("
    on_conflict = "ON CONFLICT (id)\nDO UPDATE SET "
    for key, value in item.items():
        insert += f"{key},"

        if isinstance(value, str):
            values += f"'{value}',"
            on_conflict += f"{key} = '{value}',"
        else:
            values += f"{value},"
            on_conflict += f"{key} = {value},"

    insert += "updated_at)\n"
    values += f"NOW())\n"
    on_conflict += f"updated_at = NOW();"
    return insert + values + on_conflict


class PostgresDB:
    def __init__(self, host: str, user: str, password: str, dbname: str):
        # Create/Connect to database
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=dbname,
        )

        # Create cursor, used to execute commands
        self.cur = self.connection.cursor()

    def insert_item(self, table: str, item: dict) -> None:
        self.cur.execute(upsert_query(table, item))
        self.connection.commit()


class SingletonMetaThreadSafe(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class PostgresSingletonSafe(metaclass=SingletonMetaThreadSafe):
    def __init__(self):
        self.connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="password",
            dbname="postgres",
        )

        self.cur = self.connection.cursor()

    def insert_item(self, table: str, item: dict) -> None:
        self.cur.execute(upsert_query(table, item))
        self.connection.commit()


class SingletonMetaThreadUnsafe(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class PostgresSingleton(metaclass=SingletonMetaThreadUnsafe):
    def __init__(self):
        self.connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="password",
            dbname="postgres",
        )

        self.cur = self.connection.cursor()

    def insert_item(self, table: str, item: dict) -> None:
        self.cur.execute(upsert_query(table, item))
        self.connection.commit()
