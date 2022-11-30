from dataclasses import dataclass

from adapters.base import BaseDBClient


@dataclass
class DBService:
    clients: list[BaseDBClient]

    def db_upgrade(self):
        for client in self.clients:
            client.db_upgrade()
