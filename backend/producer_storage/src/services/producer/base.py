from abc import ABC, abstractmethod
from pydantic.main import ModelMetaclass


class BaseProducer(ABC):
    
    @abstractmethod
    def produce(self, **kwargs) -> None:
        '''Публикование данных в хранилище'''
