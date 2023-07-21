from app.settings import(
                          RABBITMQ_DEFAULT_HOST, 
                          RABBITMQ_DEFAULT_USER, 
                          RABBITMQ_DEFAULT_PASS, 
                          RABBITMQ_PUBLISHER_QUEUE
                        )
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from json import dumps


class RabbitMQPublisher:
  def __init__(self, queue_name: str = RABBITMQ_PUBLISHER_QUEUE) -> None:
    self.credentials = PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS)
    self.connection = BlockingConnection(ConnectionParameters(RABBITMQ_DEFAULT_HOST,credentials=self.credentials))
    self.channel = self.connection.channel()
    self.queue_name = queue_name
    self.channel.queue_declare(self.queue_name, durable=False)

  def publish_timestamp(self, timestamp: str):
    self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=timestamp)
    self.connection.close()