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


def basic_select_query(timestamp: str):
    return f"""
        WITH pt AS
        (
            SELECT * FROM products WHERE category ILIKE ANY (ARRAY['%eletrônico%', '%tecnologia%', '%pet shop%', '%cozinha%', '%alimentos%', '%automotivo%','%bolsas%', '%casa%', '%jardim%', '%limpeza%', '%games%', '%consoles%', '%echo%', '%smartphone%', '%informática%', '%computador%'])
            AND reviews > 100
            AND discount >= 20
            UNION
            SELECT * FROM products  WHERE category ILIKE ANY (ARRAY['%beleza%', '%bebê%', '%higiene%'])
            AND reviews > 100
            AND discount >= 10
        )
        SELECT id FROM pt
        WHERE created_at BETWEEN '{timestamp}' AND NOW()
        ORDER BY reviews DESC LIMIT 100;
    """
