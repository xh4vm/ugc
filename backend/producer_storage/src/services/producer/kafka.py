from confluent_kafka.serialization import Serializer
from confluent_kafka.serializing_producer import SerializingProducer
from pydantic.main import ModelMetaclass

from .base import BaseProducer
from src.core.config import CONFIG, service_logger


def _on_delivery(err, msg) -> None:
    if err is not None:
        service_logger.info(f'[ON DELIVERY] error: "{err}"; msg: "{msg.value()}"')


class KafkaProducer(BaseProducer):
    def __init__(self, key_serializer: Serializer, value_serializer: Serializer,) -> None:
        self.producer = SerializingProducer(
            {
                'bootstrap.servers': CONFIG.KAFKA.SERVERS,
                'key.serializer': key_serializer,
                'value.serializer': value_serializer,
            }
        )

    async def produce(
        self, topic: str, key: str = None, value: ModelMetaclass = None, partition: int = -1, timestamp=0
    ) -> None:

        self.producer.produce(
            topic=topic, key=key, value=value, partition=partition, on_delivery=_on_delivery, timestamp=timestamp
        )
        self.producer.poll()
