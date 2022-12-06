from typing import Optional

import backoff
from config.base import BACKOFF_CONFIG
from config.logger import logger
from clickhouse_driver import Client as Clickhouse


def ch_conn_is_alive(ch_conn: Clickhouse) -> bool:
    """Функция для проверки работоспособности Clickhouse"""
    try:
        return ch_conn.execute('SHOW DATABASES')
    except Exception:
        return False


class ClickhouseIniter:
    def __init__(self, host: str, port: int, conn: Optional[Clickhouse] = None) -> None:
        self._conn: Clickhouse = conn
        self._host: str = host
        self._port: int = port

    @property
    def conn(self) -> Clickhouse:
        if self._conn is None or not ch_conn_is_alive(self._conn):
            self._conn = self._reconnection()

        return self._conn

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def _reconnection(self) -> Clickhouse:
        logger.info(f'Reconnection clickhouse node "{self._host}:{self._port}" ...')

        if self._conn is not None:
            logger.info('Closing already exists clickhouse connector...')
            self._conn.disconnect()

        return Clickhouse(host=self._host, port=self._port)

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def create(self, ddl_file: str):
        logger.info(f'[*] Initialized clickhouse node: "{self._host}:{self._port}"')
        logger.info(f'[*] Reading schema from file: "{ddl_file}"')

        with open(ddl_file, 'r') as fd:
            schema = fd.read()

        for command in schema.split(';'):
            command = command.strip()

            if len(command) == 0:
                continue

            logger.info(f'[*] Command: "{command}"')
            self.conn.execute(command)
