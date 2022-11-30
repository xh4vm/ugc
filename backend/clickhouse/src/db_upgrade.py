from settings import ch_settings
from adapters.clickhouse.client import ClickHouseClient

from services import DBService

node_prefix = ch_settings.CH_NODE_PREFIX
node_ports = ch_settings.CH_NODE_PORTS
local_mode = ch_settings.CH_LOCAL_MODE

db_service = DBService(
    clients=[
        ClickHouseClient(
            host="localhost" if local_mode else f"{node_prefix}{i+1}",
            port=node_ports[i] if local_mode else None,
            cluster_name=ch_settings.CH_CLUSTER_NAME,
            db_name=ch_settings.CH_DB_NAME if i % 2 == 0 else ch_settings.CH_REPLICA_DB_NAME,
        )
        for i in range(ch_settings.CH_NODE_NUM)
    ]
)

if __name__ == "__main__":
    db_service.db_upgrade()
