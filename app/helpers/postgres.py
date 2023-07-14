from typing import List
import psycopg
from app.settings import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER

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
    def __init__(self) -> None:
        self.conninfo = f"dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD} host={POSTGRES_HOST} port={POSTGRES_PORT}"

    async def upsert_item(self, table: str, item: dict) -> None:
        async with await psycopg.AsyncConnection.connect(self.conninfo) as aconn:
            async with aconn.cursor() as cur:
                await cur.execute(upsert_query(table, item))

    def select(self, select_query: str) -> List[tuple]:
        with psycopg.connect(self.conninfo) as conn:
            with conn.cursor() as cur:
                records = cur.execute(select_query).fetchall()
                conn.commit()
                return records