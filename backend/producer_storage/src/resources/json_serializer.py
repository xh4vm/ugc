from typing import Callable, Any
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from pydantic.main import ModelMetaclass
import orjson

from dependency_injector import resources


class JSONSerializerResource(resources.Resource):
    def init(
        self,
        schema: ModelMetaclass,
        registry: SchemaRegistryClient,
        to_dict: Callable[[ModelMetaclass], dict[str, Any]] = None,
    ) -> JSONSerializer:
        return JSONSerializer(schema_str=schema.schema_json(), schema_registry_client=registry, to_dict=to_dict)
