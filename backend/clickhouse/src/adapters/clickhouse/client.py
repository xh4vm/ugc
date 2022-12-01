import time
from dataclasses import dataclass
from typing import Type

import backoff
from clickhouse_driver import Client
from loguru import logger

from adapters import models
from adapters.base import BaseDBClient, Model
from adapters.enums import DBDialects


@dataclass
class ClickHouseClient(BaseDBClient):
    dialect: str = DBDialects.CLICKHOUSE

    def connect(self):
        self.connection = Client(host=self.host, port=self.port)

    @property
    def uri(self):
        port = f":{self.port}" if self.port else ""
        return f"{self.host}{port}"

    def db_exists(self):
        for item in self.execute("SHOW DATABASES") or []:
            if len(item) > 0 and item[0] == self.db_name:
                return True
        return False

    def db_healthy(self, timeout: int = 15):
        logger.info("Waiting for db '%s' on host '%s'" % (self.db_name, self.uri))
        n = 0
        while not self.db_exists() and n < timeout:
            time.sleep(1)
            n += 1
        return n < timeout or self.db_exists()

    def db_upgrade(self):
        if self.db_healthy():
            logger.info("DB '%s' is available on host '%s'" % (self.db_name, self.uri))
            self.create_table(self.db_name, models.View)
            self.create_table("default", models.DistributedView)
        else:
            logger.error(
                "Database '%s' is unavailable on '%s'" % (self.db_name, self.uri)
            )

    def create_table(self, db: str, table: Type[Model]):
        table_instance = table()
        query = (
            """CREATE TABLE IF NOT EXISTS {db}.{table} {fields} {extra_args};""".format(
                db=db,
                table=table.__tablename__,
                fields=table_instance.get_sql_fields(self.dialect),
                extra_args=table_instance.get_sql_args(self.cluster_name),
            )
        )
        self.execute(query)
