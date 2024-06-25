import os
from abc import ABC, abstractmethod

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from litescribe_shared.dto import TranscriptionRequest
from litescribe_shared.serialization import deserialize_transcription_request
from litescribe_worker.gateway_client import GatewayClient
from litescribe_worker.transcriber import Transcriber


class BaseConsumer(ABC):
    queue_name: str
    consumer_id: str
    connection: pika.BlockingConnection
    channel: BlockingChannel

    def __init__(self, rabbitmq_url: str, queue_name: str, consumer_id: str):
        self.queue_name = queue_name
        self.consumer_id = consumer_id

        self.connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
        self.channel = self.connection.channel()

    def setup_queue(self):
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=1)

    def consume(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message_callback)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            raise
        finally:
            self.connection.close()

    @abstractmethod
    def on_message_callback(
        self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes
    ): ...


class TranscribeConsumer(BaseConsumer):
    transcriber: Transcriber
    gateway_client: GatewayClient

    def __init__(
        self,
        rabbitmq_url: str,
        queue_name: str,
        consumer_id: str,
        transcriber: Transcriber,
        gateway_client: GatewayClient,
    ):
        super().__init__(rabbitmq_url, queue_name, consumer_id)
        self.transcriber = transcriber
        self.gateway_client = gateway_client

    def on_message_callback(
        self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes
    ) -> None:
        transcription_request: TranscriptionRequest = deserialize_transcription_request(body)
        transcription = self.transcriber.transcribe_to_string(transcription_request.fp)
        self.gateway_client.post_transcription_result(transcription_request.request_id, transcription)
        channel.basic_ack(delivery_tag=method.delivery_tag)
        os.remove(transcription_request.fp)
