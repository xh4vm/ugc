import json

from config.base import CLICKHOUSE_CONFIG
from config.nodes import NODES
from clickhouse_initer import ClickhouseIniter

if __name__ == '__main__':
    
    for NODE in NODES:
        ch_initer = ClickhouseIniter(host=NODE.HOST, port=NODE.PORT)
        ch_initer.create(ddl_file=f'./mapping/{NODE.SCHEMA_NAME}')
