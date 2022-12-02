from kafka import KafkaProducer
from loguru import logger


def publish_message(producer_instance: KafkaProducer, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        logger.info('Message published successfully.')
    except Exception as ex:
        logger.error('Exception in publishing message. {0}'.format(str(ex)))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['172.27.0.7:9092', '172.27.0.5:9092', '172.27.0.6:9092', ])
    except Exception as ex:
        logger.error('Exception while connecting Kafka. {0}'.format(str(ex)))
    finally:
        return _producer


kafka_producer = connect_kafka_producer()

if kafka_producer is not None:
    publish_message(kafka_producer, 'movie_frame', '123456789', '{"movie_id": "kafka_loader", "frame_time": 1}')
    kafka_producer.close()
