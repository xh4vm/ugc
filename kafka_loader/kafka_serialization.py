from loguru import logger
from producer.kafka import KafkaProducerWorker

kafka_producer = KafkaProducerWorker()
kafka_producer.produce(
    topic="movie_frame",
    value={"movie_id": "kafka_serialization", "frame_time": 3},
    key='987654321',
)

logger.info('Message published successfully.')
