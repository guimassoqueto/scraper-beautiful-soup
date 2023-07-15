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


basic_select_query = """
select * from products
where category ilike any (ARRAY['%higiene', '%alimentos%', '%automotivo%','%bolsas%', '%casa%', '%jardim%', '%limpeza%', '%games%', '%consoles%', '%kindle%', '%echo%', '%smartphone%', '%informática%', '%computador%'])
and reviews > 50
and discount > 20
order by discount asc;
"""
