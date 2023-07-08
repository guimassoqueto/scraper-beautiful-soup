import psycopg


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
    def __init__(
        self,
        dbname: str = "postgres",
        dbuser: str = "postgres",
        dbpassword: str = "password",
        dbhost: str = "localhost",
        dbport: str = "5432",
    ) -> None:
        self.conninfo = f"dbname={dbname} user={dbuser} password={dbpassword} host={dbhost} port={dbport}"

    async def upsert_item(self, table: str, item: dict) -> None:
        async with await psycopg.AsyncConnection.connect(self.conninfo) as aconn:
            async with aconn.cursor() as cur:
                await cur.execute(upsert_query(table, item))
