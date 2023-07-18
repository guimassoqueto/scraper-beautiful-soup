from app.settings import TIMESTAMP_FILE
from app.helpers.fake_header import fake_header
from app.helpers.database.postgres import PostgresDB
from app.helpers.database.database_queries.queries import basic_select_query
from app.helpers.rabbitmq.publisher import RabbitMQPublisher
from app.helpers.rabbitmq.receiver import receiver
from app.helpers.utils.timestamp_from_file import get_date_string
from app.spiders.amazon_scraper import amazon_scraper
from asyncio import Semaphore, gather, create_task
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic
from pika.spec import BasicProperties
from asyncio import run
from json import loads


async def main(non_inserted_pids: list):
    limit = Semaphore(8)
    tasks = []
    for pid in non_inserted_pids:
        task = create_task(amazon_scraper(pid, fake_header(), limit))
        tasks.append(task)
    result = await gather(*tasks)
    return result


def message_handler(
    channel: BlockingChannel, 
    method: Basic.Deliver, 
    properties: BasicProperties, 
    body: bytes
):
    non_inserted_pids = loads(body)
    print(f"{len(non_inserted_pids)} pids received...")
    result = run(main(non_inserted_pids))
    if (result):
        pg = PostgresDB()
        pids = pg.select(basic_select_query(get_date_string(TIMESTAMP_FILE)))
        publisher = RabbitMQPublisher()
        publisher.publish_pids([pid[0] for pid in pids])
        channel.basic_ack(delivery_tag=method.delivery_tag) # message acknowledgement



if __name__ == "__main__":
    try:
        receiver(message_handler)
    except KeyboardInterrupt:
        print('Interrupted')