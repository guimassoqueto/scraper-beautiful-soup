from typing import Generator


def get_failed_products_generator(
    non_inserted_pids_file: str,
) -> Generator[str, None, None]:
    pids = []
    with open(non_inserted_pids_file, "r", encoding="utf-8") as file:
        for product_id in file:
            product_id = product_id.strip()
            pids.append(product_id)

    return (pid for pid in pids)