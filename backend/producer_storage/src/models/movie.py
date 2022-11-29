from fastapi import Query
from pydantic import Field
from .base import JSONModel


class MovieFrame(JSONModel):
    movie_id: str
    frame_time: int
