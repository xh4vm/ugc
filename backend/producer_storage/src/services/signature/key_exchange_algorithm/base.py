from abc import ABC, abstractmethod


class BaseKeyExchangeAlgorithm(ABC):

    @abstractmethod
    def generate_primitives(self):
        """Генерируем базу"""

    @abstractmethod
    def get_public_key(self):
        """Генерирует публичный ключ"""

    @abstractmethod
    def get_private_key(self):
        """Генерирует приватный ключ"""

    @abstractmethod
    def key_derivation(self):
        """KDF - вытягивание общего секретного ключа"""
