from typing import Generator
from app.helpers.postgres import PostgresSingleton
from app.helpers.fake_header import fake_header
from app.spiders.amazon import get_item


def get_failed_products_generator(
    pid_errors: str = "insertion_errors.log",
) -> Generator[str, None, None]:
    pids = []
    with open(pid_errors, "r", encoding="utf-8") as file:
        for product_id in file:
            product_id = product_id.strip()
            pids.append(product_id)

    return (pid for pid in pids)


def write_errors(line: str):
    print(line)
    with open("errors.log", "w", encoding="utf-8") as f:
        f.write(f"{line}\n")


if __name__ == "__main__":
    failed_pids = get_failed_products_generator()
    count = 1
    for pid in failed_pids:
        try:
            pg = PostgresSingleton()
            pg.insert_item("products", get_item(pid, fake_header()))
            print(
                f"inserted #{count}: {pid}",
            )
            count += 1
        except Exception as e:
            print(e)
            write_errors(f"{pid}")
            continue
