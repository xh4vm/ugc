from modules.auth.src.payloads.fastapi import UserAccessRequired

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Body

from src.containers.movie import ServiceContainer
from src.services.producer.kafka import KafkaProducer
from src.core.config import CONFIG
from src.utils.error_dependency_handler import auth_dependency_handler

from src.models.movie import MovieFrame


router = APIRouter(prefix='/movie', tags=['Movies'])
URL = f'{CONFIG.APP.HOST}:{CONFIG.APP.PORT}{CONFIG.APP.API_PATH}/{CONFIG.APP.API_VERSION}/movie/frame'


@router.post(path='/frame', name='Produce storage user data')
@inject
async def movie_frame(
    _dependency_handler: None = Depends(auth_dependency_handler),
    frame: MovieFrame = Body(title='MovieFrame', alias='movie_frame'),
    sig: str = Body(title='Signature'),
    user_id: str = Depends(UserAccessRequired(permissions={URL: 'POST'})),
    kafka_producer: KafkaProducer = Depends(Provide[ServiceContainer.kafka_producer])
) -> None:

    await kafka_producer.produce(topic=CONFIG.KAFKA.TOPICS.MOVIE_FRAME, key=user_id, value=frame)
