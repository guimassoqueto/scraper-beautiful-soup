from app.helpers.fake_header import fake_header
from app.helpers.database.postgres import PostgresDB
from app.helpers.database.database_queries.queries import basic_select_query
from app.spiders.amazon_scraper import amazon_scraper
from asyncio import Semaphore, gather, create_task
from pika import PlainCredentials, BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic
from pika.spec import BasicProperties
from asyncio import run
from json import loads
from app.helpers.rabbitmq.publisher import RabbitMQPublisher
from app.settings import (
                            RABBITMQ_DEFAULT_HOST, 
                            RABBITMQ_DEFAULT_USER, 
                            RABBITMQ_DEFAULT_PASS, 
                            RABBITMQ_RECEIVER_QUEUE
                         )


def write_errors(line: str):
    print(line)
    with open("errors.log", "w", encoding="utf-8") as f:
        f.write(f"{line}\n")


async def main(non_inserted_pids: list):
    limit = Semaphore(8)
    tasks = []
    for pid in non_inserted_pids:
        task = create_task(amazon_scraper(pid, fake_header(), limit))
        tasks.append(task)
    result = await gather(*tasks)
    return result


def callback(
    channel: BlockingChannel, 
    method: Basic.Deliver, 
    properties: BasicProperties, 
    body: bytes
):
    non_inserted_pids = loads(body)
    print(body)
    print(f"{len(non_inserted_pids)} pids received...")
    result = run(main(non_inserted_pids))
    if (result):
        pg = PostgresDB()
        pids = pg.select(basic_select_query)
        publisher = RabbitMQPublisher()
        publisher.publish_pids([pid[0] for pid in pids])


def receiver():
    credentials = PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS)
    connection = BlockingConnection(ConnectionParameters(RABBITMQ_DEFAULT_HOST,
                                                        credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(RABBITMQ_RECEIVER_QUEUE)

    # consumer
    channel.basic_consume(
        queue=RABBITMQ_RECEIVER_QUEUE,
        auto_ack=True,
        on_message_callback=callback
    )

    print('Waiting for new messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    try:
        receiver()
    except KeyboardInterrupt:
        print('Interrupted')