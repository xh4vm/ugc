from abc import ABC, abstractmethod


class BaseSignature(ABC):

    @abstractmethod
    def sig(self, data: str) -> str:
        """Метод подписи данных"""

    @abstractmethod
    def verify(self, data: str, sig: str) -> bool:
        """Метод проверки подписи"""
