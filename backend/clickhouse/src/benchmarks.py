import datetime
from pathlib import Path

from adapters.clickhouse.client import ClickHouseClient

ROOT_DIR = Path(__file__).resolve().parent.parent

db_client = ClickHouseClient(host="localhost", port="9000")


def run_query(query):
    print(query)
    start = datetime.datetime.now()
    r = db_client.execute(query)
    print("result:", r)
    print("time:", datetime.datetime.now() - start, '\n')


run_query(
    """SELECT COUNT(*) FROM views_progress"""
)
run_query(
    """SELECT movie_id, COUNT(*) movie_count FROM views_progress GROUP BY movie_id ORDER BY movie_count DESC LIMIT 20"""
)
run_query(
    """SELECT COUNT(*) FROM (SELECT movie_id, COUNT(*) movie_count FROM views_progress GROUP BY movie_id) as view_movie_counter WHERE movie_count<10"""
)
run_query(
    """SELECT movie_id, sum(movie_frame) as sum_movie_frame FROM views_progress GROUP BY movie_id ORDER BY sum_movie_frame DESC LIMIT 20"""
)
run_query(
    """SELECT user_id, count(*) as movies_count FROM (SELECT DISTINCT user_id, movie_id FROM views_progress GROUP BY user_id, movie_id) as view_user_movie GROUP BY user_id ORDER BY movies_count DESC LIMIT 20"""
)
run_query(
    """SELECT user_id, SUM(max_user_movie_frame) as total_user_movies_frame FROM (SELECT DISTINCT user_id, movie_id, MAX(movie_frame) as max_user_movie_frame FROM views_progress GROUP BY user_id, movie_id) as view_user_movie GROUP BY user_id ORDER BY total_user_movies_frame DESC LIMIT 20"""
)
