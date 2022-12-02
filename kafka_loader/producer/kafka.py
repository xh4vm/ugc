import logging

from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.serializing_producer import SerializingProducer

from .base import BaseProducer

logging.basicConfig(level=logging.INFO)

KAFKA_BROKER = ['172.27.0.7:9092', '172.27.0.5:9092', '172.27.0.6:9092', ]


def _on_delivery(err, msg) -> None:
    if err is not None:
        logging.info(f'[ON DELIVERY] error: "{err}"; msg: "{msg.value()}"')


class KafkaProducerWorker(BaseProducer):

    def __init__(self) -> None:
        self.producer = SerializingProducer({
            'bootstrap.servers': KAFKA_BROKER,
            'key.serializer': StringSerializer,
            'value.serializer': JSONSerializer,
        })

    def produce(
        self,
        topic: str,
        key: str = None,
        value: dict = None,
        partition: int = -1,
        timestamp=0
    ) -> None:

        self.producer.produce(
            topic=topic,
            key=key,
            value=value,
            partition=partition,
            on_delivery=_on_delivery,
            timestamp=timestamp
        )
        self.producer.poll()
