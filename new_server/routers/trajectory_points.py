import json
import time

from database import db
from dependencies import get_redis
from fastapi import APIRouter, Depends, Query
from redis.asyncio import Redis
from sqlalchemy.orm import Session

trajectory_points_router = APIRouter(
    prefix="/trajectory_points", tags=["Trajectory points"]
)

from models import QueryParamsModel, TrajectoryPointModel, TrajectoryPointResponseModel
from repo import ReadRepo
from tables import TrajectoryPointsTable

TrajectoryRepo = ReadRepo[TrajectoryPointsTable, TrajectoryPointModel]


def create_trajectory_repo() -> TrajectoryRepo:
    return TrajectoryRepo(TrajectoryPointsTable, TrajectoryPointModel)


default_traj_key = "trajectory:[{'log_op':'NONE', 'filters':[{'field':'orbit_id','op':'==', 'value': 1}]}]:None:None"


@trajectory_points_router.get(
    "/get_chunk",
    response_model=list[TrajectoryPointResponseModel],
    summary="Получить точки траектории согласно фильтрам",
)
async def get_chunk(
    filter_groups: str = Query(None),
    limit: int = Query(None),
    offset: int = Query(None),
    session=Depends(db.create_session),
    repo: TrajectoryRepo = Depends(create_trajectory_repo),
    redis: Redis = Depends(get_redis),
):
    """
    Возвращает фрагмент данных о точках траекторий\n

    Параметры:\n
    ----------\n
    filter_groups : str, optional\n
        JSON-строка с группами фильтров для выборки данных\n
    limit : int, optional\n
        Максимальное количество записей для возврата\n
    offset : int, optional\n
        Смещение\n
    session : Session\n
        Сессия SQLAlchemy для подключения к БД, создаётся через зависимость\n
    repo : TrajectoryRepo\n
        Репозиторий для работы с данными траекторий, создаётся через зависимость\n
    redis : Redis\n
        Клиент Redis для кэширования, создаётся через зависимость\n

    Возвращает:\n
    ----------\n
    List[TrajectoryPointResponseModel]\n
        Список моделей точек траектории, соответствующих заданным фильтрам и пагинации\n
    """

    start_time = time.time()
    # ----- Формируем уникальный ключ кэша -----
    key = f"trajectory:{filter_groups}:{limit}:{offset}"
    # ----- Проверяем кэш -----
    cached = await redis.get(key)
    if cached:
        data = json.loads(cached)
        end_time = time.time()
        print(
            f"DEBUG: GET FROM REDIS /get_chunk: {end_time - start_time:.4f} sec, get {len(data)} trajectory points"
        )
        return data

    # ----- Выполняем запрос в БД -----

    result = repo.get_chunk(
        session,
        QueryParamsModel(
            filter_groups=json.loads(filter_groups) if filter_groups else [],
            limit=limit,
            offset=offset,
        ),
    )
    end_time = time.time()
    print(
        f"DEBUG: /get_chunk: request to DB {end_time - start_time:.4f} sec, get {len(result)} trajectory points"
    )

    # ----- Формируем список pydantic-моделей -----
    res = [
        TrajectoryPointResponseModel(
            id=row.id,
            orbit_id=row.orbit_id,
            x=row.x,
            y=row.y,
            z=row.z,
            vx=row.vx,
            vy=row.vy,
            vz=row.vz,
            t=row.t,
            abs_v=row.abs_v,
        ).model_dump()
        for row in result
    ]
    res = sorted(res, key=lambda point: point["id"])
    # ----- Сохраняем в кэш (TTL = 20 сек) -----
    if key == default_traj_key:
        await redis.set(key, json.dumps(res))
    else:
        await redis.set(key, json.dumps(res), ex=43200)
    print(f"DEBUG: /get_chunk SAVED NEW KEY IN REDIS")
    return res
