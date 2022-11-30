from datetime import datetime

from config.config import SETTINGS
from dataset_loader.dataset_loader import DatasetLoader
from loguru import logger
from utility.utility import get_time
from vertica_python import Connection
from vertica_worker.vertica_worker import VerticaSaver, conn_context_vertica


def transform_data(data):
    res = [(value[0], value[1], value[3], datetime.now()) for value in data]
    return res


@get_time
def load_data_to_vertica(conn: Connection):
    """The main method of loading data from SQLite to Postgres."""

    vertica_saver = VerticaSaver(
        conn,
        SETTINGS.tables,
        SETTINGS.truncate_table,
        SETTINGS.batch_size,
    )

    dataset_loader = DatasetLoader(
        SETTINGS.batch_size,
        SETTINGS.dataset_folder,
        SETTINGS.dataset_file_ext,
        SETTINGS.dataset_data_deliver,
        SETTINGS.dataset_data_skip_row,
    )

    # Create tables
    if SETTINGS.create_table:
        sql = open(SETTINGS.ddl_file, "r").read()
        vertica_saver.execute_sql_command(sql)
        vertica_saver.connection.commit()

    for table_name, value in SETTINGS.tables.items():

        if not dataset_loader.load_one_file(table_name, value['types']):
            logger.error(dataset_loader.error)
            continue

        if SETTINGS.truncate_table:
            if not vertica_saver.truncate_table(table_name):
                break

        batch_data_generator = dataset_loader.load_batch()
        for batch_number, batch_data in enumerate(batch_data_generator, 1):
            data_to_load = transform_data(batch_data)
            logger.info('Пачка №{0} {1}'.format(batch_number, len(batch_data)))
            if not vertica_saver.save_table_to_vertica(table_name, data_to_load):
                logger.error(vertica_saver.error)
                break

    return vertica_saver.sql_time


def main():
    with (
        conn_context_vertica(SETTINGS.vertica.dict()) as connection
    ):
        sql_time = load_data_to_vertica(connection)
        logger.info('Время выполнения SQL: {0}s'.format(sql_time))


if __name__ == '__main__':
    main()
