import json
import time

from database import db_echo
from dependencies import get_redis
from fastapi import APIRouter, Depends, HTTPException, Query
from redis.asyncio import Redis
from sqlalchemy.orm import Session

orbit_poincare_view_router = APIRouter(
    prefix="/orbit_poincare_view", tags=["Poincare_view"]
)

from models import OrbitPoincareViewModel, PoincareResponseModel, QueryParamsModel
from repo import ReadRepo
from tables import OrbitPoincareViewTable

OrbitPoincareViewRepo = ReadRepo[OrbitPoincareViewTable, OrbitPoincareViewModel]


def create_orbit_poincare_view_repo() -> OrbitPoincareViewRepo:
    return OrbitPoincareViewRepo(OrbitPoincareViewTable, OrbitPoincareViewModel)


default_sec_key = "nearest_sec:0.0:0.0:x = 0"
default_by_cj_key = "get_by_cj:[{'log_op': 'NONE', 'filters': [{'field': 'orbit_id', 'op': '==', 'value': '1'}, {'field': 'plane', 'op': '==', 'value': 'y = 0'}]}]:None:None"


@orbit_poincare_view_router.get(
    "/get_nearest_section",
    response_model=PoincareResponseModel,
    summary="Получить ближайшее сечение по заданным x, z и плоскости",
)
async def get_near_sec(
    x: float,
    z: float,
    plane: str,
    session: Session = Depends(db_echo.create_session),
    repo: OrbitPoincareViewRepo = Depends(create_orbit_poincare_view_repo),
    redis: Redis = Depends(get_redis),
):
    """
    Возвращает ближайшее сечение Пуанкаре для заданных координат x, z и плоскости сечения\n

    Параметры:\n
    ----------\n
    x : float\n
        Координата X для поиска ближайшего сечения\n
    z : float\n
        Координата Z для поиска ближайшего сечения\n
    plane : str\n
        Плоскость сечения Пуанкаре\n
    session : Session\n
        Сессия SQLAlchemy для подключения к БД, создаётся через зависимость\n
    repo : OrbitPoincareViewRepo\n
        Репозиторий для работы с представлением сечений Пуанкаре и орбит, создаётся через зависимость\n
    redis : Redis\n
        Клиент Redis для кэширования, создаётся через зависимость\n

    Возвращает:\n
    ----------\n
    PoincareResponseModel\n
        Модель ответа, содержащая данные ближайшего сечения Пуанкаре
        для указанных координат и плоскости
    """

    start_time = time.time()
    # --- формируем уникальный ключ кэша ---
    key = f"nearest_sec:{x}:{z}:{plane}"
    # --- пробуем достать данные из кэша ---
    cached = await redis.get(key)
    if cached:
        data = json.loads(cached)
        end_time = time.time()
        print(
            f"DEBUG: GET FROM REDIS /get_nearest_section: {end_time - start_time:.4f} sec"
        )
        return data

    result = repo.get_nearest_section(session, x, z, plane)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"DEBUG: /get_nearest_section: completed for {execution_time:.4f} sec")
    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Not found section for plane: {plane}"
        )
    res = result.model_dump()
    print(f"DEBUG: res  = {res}")
    if key == default_sec_key:
        await redis.set(key, json.dumps(res))
    else:
        await redis.set(key, json.dumps(res), ex=43200)
    print(f"DEBUG: /get_nearest_section SAVED NEW KEY IN REDIS")

    return res


def between(filter_groups, rate):
    filter_groups_json = json.loads(filter_groups)
    filters = filter_groups_json[0]["filters"]
    for i, filter in enumerate(filters):
        if (
            filter.get("field") == "cj"
            and filter.get("op") == "=="
            and "value" in filter
        ):
            original_value = filter["value"]

            del filters[i]

            filters.insert(
                i, {"field": "cj", "op": ">=", "value": original_value - rate}
            )

            filters.insert(
                i + 1, {"field": "cj", "op": "<=", "value": original_value + rate}
            )

            break
    filter_groups_json[0]["filters"] = filters
    return str(filter_groups_json).replace("'", '"')


@orbit_poincare_view_router.get(
    "/get_by_cj",
    response_model=list[PoincareResponseModel],
    summary="Получить координаты сечений согласно точке либрациии и константе якоби",
)
async def get_by_cj(
    filter_groups: str = Query(None),
    limit: int = Query(None),
    offset: int = Query(None),
    rate: float = Query(None),
    session: Session = Depends(db_echo.create_session),
    repo: OrbitPoincareViewRepo = Depends(create_orbit_poincare_view_repo),
    redis: Redis = Depends(get_redis),
):
    """
    Возвращает сечения Пуанкаре, отфильтрованные по константе Якоби и точке либрации\n

    Параметры:\n
    ----------\n
    filter_groups : str, optional\n
        JSON-строка с группами фильтров для выборки данных\n
    limit : int, optional\n
        Максимальное количество записей для возврата\n
    offset : int, optional\n
        Смещение\n
    rate : float, optional\n
        Относительная точность для фильтрации по константе Якоби\n
    session : Session\n
        Сессия SQLAlchemy для подключения к БД, создаётся через зависимость\n
    repo : OrbitPoincareViewRepo\n
        Репозиторий для работы с представлением сечений Пуанкаре и орбит, создаётся через зависимость\n
    redis : Redis\n
        Клиент Redis для кэширования, создаётся через зависимость\n

    Возвращает:\n
    ----------\n
    List[PoincareResponseModel]
    """

    start_time = time.time()
    filter_groups = between(filter_groups, rate)

    # --- формируем уникальный ключ кэша ---
    key = f"get_by_cj:{filter_groups}:{limit}:{offset}"
    # --- пробуем достать данные из кэша ---
    cached = await redis.get(key)
    if cached:
        data = json.loads(cached)
        end_time = time.time()
        print(
            f"DEBUG: GET FROM REDIS /get_by_cj: completed for {end_time - start_time:.4f} sec, get {len(data)} sections"
        )
        return data

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
        f"DEBUG: /get_by_cj: completed for {end_time - start_time:.4f} sec, get {len(result)} sections"
    )
    res = [
        PoincareResponseModel(
            orbit_id=row.orbit_id,
            x=row.x,
            y=row.y,
            z=row.z,
            vx=row.vx,
            vy=row.vy,
            vz=row.vz,
            ax=row.ax,
            ay=row.ay,
            az=row.az,
            dist_primary=row.dist_primary,
            dist_secondary=row.dist_secondary,
            abs_v=row.abs_v,
            x_points=row.x_points,
            y_points=row.y_points,
            z_points=row.z_points,
            vx_points=row.vx_points,
            vy_points=row.vy_points,
            vz_points=row.vz_points,
            points_count=row.points_count,
        ).model_dump()
        for row in result
    ]

    if key == default_by_cj_key:
        await redis.set(key, json.dumps(res))
    else:
        await redis.set(key, json.dumps(res), ex=43200)
    print(f"DEBUG: /get_by_cj SAVED NEW KEY IN REDIS")

    return res
