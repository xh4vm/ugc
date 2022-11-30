import csv
import datetime
import random
from pathlib import Path

from loguru import logger

from adapters.clickhouse.client import ClickHouseClient

ROOT_DIR = Path(__file__).resolve().parent.parent

db_client = ClickHouseClient(host="localhost", port="9000")


def insert_to_db(values):
    query = f"INSERT INTO default.views_progress (id, user_id, movie_id, rating, movie_frame, created) VALUES {values}"
    start = datetime.datetime.now()
    db_client.execute(query)
    return datetime.datetime.now() - start


BENCH_SIZE = 1000000
FILE_NAME = "ratings.csv"

start = datetime.datetime.now()
sql_duration = datetime.timedelta(0)
total_rows = 1
total_benches = 0
with open(ROOT_DIR / "fake_data" / FILE_NAME, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",", quotechar="|")
    next(reader)

    field_values = ""
    current_bench_size = 0
    bench_start = datetime.datetime.now()
    for row in reader:
        frame = random.randint(1, 7200)
        field_values += f"({total_rows}, {row[0]}, {row[1]}, {row[2]}, {frame}, now()), "
        if current_bench_size == BENCH_SIZE - 1:
            bench_sql_duration = insert_to_db(field_values[:-2])
            bench_end = datetime.datetime.now()
            logger.info(f'Total rows: {total_rows}. Bench: {bench_end - bench_start}; Only SQL: {bench_sql_duration}')
            sql_duration += bench_sql_duration
            current_bench_size = 0
            total_benches += 1
            field_values = ""
            bench_start = datetime.datetime.now()

        current_bench_size += 1
        total_rows += 1

    if field_values:
        insert_to_db(field_values[:-2])

end = datetime.datetime.now()
delta = end-start
print("Всего пачек:", total_benches)
print("Всего строк:", total_rows)
print(f'Общее время выполнения: {delta}')
print(f'Только SQL: {sql_duration}')
