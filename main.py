from app.helpers.postgres import PostgresDB
from app.helpers.get_failed_products_generator import get_failed_products_generator
from app.helpers.fake_header import fake_header
from app.spiders.amazon_scraper import amazon_scraper
from app.settings import NON_INSERTED_PIDS_FOLDER
from asyncio import Semaphore, run, gather, create_task
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from os import remove, mkdir
from os.path import exists


def write_errors(line: str):
    print(line)
    with open("errors.log", "w", encoding="utf-8") as f:
        f.write(f"{line}\n")


async def main(non_inserted_pids_file: str):
    limit = Semaphore(8)
    tasks = []
    failed_pids = get_failed_products_generator(non_inserted_pids_file)
    remove(non_inserted_pids_file)
    for pid in failed_pids:
        task = create_task(amazon_scraper(pid, fake_header(), limit))
        tasks.append(task)
    result = await gather(*tasks)
    return result


class FolderScanner(FileSystemEventHandler):
    def on_created(self, event):
        print(f"File created: {event.src_path}")
        async_result = run(main(event.src_path))
        if async_result:
            print("All insertions Complete.")
            


if __name__ == "__main__":
    if (not exists(NON_INSERTED_PIDS_FOLDER)): mkdir(NON_INSERTED_PIDS_FOLDER)

    print(f"Scanning ./{NON_INSERTED_PIDS_FOLDER} folder...")

    try:
        observer = Observer()
        event_handler = FolderScanner()
        observer.schedule(event_handler, NON_INSERTED_PIDS_FOLDER, recursive=False)
        observer.start()
    except Exception as e:
        print(e)
        observer.stop()
    observer.join()
