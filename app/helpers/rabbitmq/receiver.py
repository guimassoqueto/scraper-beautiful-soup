from pika import PlainCredentials, BlockingConnection, ConnectionParameters
from app.settings import (
                      RABBITMQ_DEFAULT_HOST, 
                      RABBITMQ_DEFAULT_USER, 
                      RABBITMQ_DEFAULT_PASS, 
                      RABBITMQ_RECEIVER_QUEUE
                    )

"""
This code follows the basic RabbitMQ tutorial:
https://rabbitmq.com/tutorials/tutorial-one-python.html
"""


def receiver(message_handler):
  credentials = PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS)
  connection = BlockingConnection(ConnectionParameters(RABBITMQ_DEFAULT_HOST,
                                                                 credentials=credentials))
  channel = connection.channel()
  channel.queue_declare(RABBITMQ_RECEIVER_QUEUE, durable=False)

  # consumer
  channel.basic_consume(
    queue=RABBITMQ_RECEIVER_QUEUE,
    auto_ack=False, # message acknoledgement
    on_message_callback=message_handler
  )
  channel.start_consuming()