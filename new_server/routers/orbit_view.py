import json
import time

from database import db
from dependencies import get_redis
from fastapi import APIRouter, Depends, Query
from redis.asyncio import Redis
from sqlalchemy.engine.cursor import ResultProxy
from sqlalchemy.orm import Session

orbit_view_router = APIRouter(prefix="/orbit_view", tags=["Orbit_view"])

from models import (
    BrouckeResponseModel,
    FamilyParamResponseModel,
    MapResponseModel,
    OneOrbitResponseModel,
    OrbitViewModel,
    QueryParamsModel,
)
from repo import ReadRepo
from tables import OrbitViewTable

OrbitViewRepo = ReadRepo[OrbitViewTable, OrbitViewModel]


def create_orbit_view_repo() -> OrbitViewRepo:
    return OrbitViewRepo(OrbitViewTable, OrbitViewModel)


default_map_key = "map:[{'log_op':'NONE', 'filters':[{'field':'lib_point','op':'like','value':'L1'}]},{'log_op':'OR','filters':[{'field':'family_tag','op':'like','value':'L'},{'field':'family_tag','op':'like','value':'V'},{'field':'family_tag','op':'like','value':'L.2P1'},{'field':'family_tag','op':'like','value':'L.3P1'},{'field':'family_tag','op':'like','value':'L.4P1'},{'field':'family_tag','op':'like','value':'L.2P1.2P1'},{'field':'family_tag','op':'like','value':'L.2P1.3P1'},{'field':'family_tag','op':'like','value':'L.2P1.3P2'},{'field':'family_tag','op':'like','value':'H.2P1'},{'field':'family_tag','op':'like','value':'H.2P2'},{'field':'family_tag','op':'like','value':'H.2P3'},{'field':'family_tag','op':'like','value':'H.3P1'},{'field':'family_tag','op':'like','value':'H.3P2'},{'field':'family_tag','op':'like','value':'H.3P3'},{'field':'family_tag','op':'like','value':'H.4P1'},{'field':'family_tag','op':'like','value':'Q'},{'field':'family_tag','op':'like','value':'H_s'},{'field':'family_tag','op':'like','value':'H_n'}]}]:None:None"

default_next_key = "next_orbit:L1:H_s:1"

default_prev_key = "prev_orbit:L1:H_s:1"

default_near_key = "nearest:0.0:0.0"

default_fam_param_key = "family_param:L1:L:t:cj:ax"

default_broucke_key = "get_Broucke:[{'log_op':'AND', 'filters':[{'field':'lib_point', 'op':'like', 'value':'L1'},      {'field':'family_tag', 'op':'like', 'value':'L'}]}]:None:None"


@orbit_view_router.get(
    "/get_map",
    response_model=list[MapResponseModel],
    summary="Получить данные для карты начальных условий",
)
async def get_map(
    filter_groups: str = Query(None),
    limit: int = Query(None),
    offset: int = Query(None),
    session: Session = Depends(db.create_session),
    repo: OrbitViewRepo = Depends(create_orbit_view_repo),
    redis: Redis = Depends(get_redis),
):
    """
    Возвращает данные орбит для построения карты начальных условий\n

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
    repo : OrbitViewRepo\n
        Репозиторий для работы с представлениями орбит, создаётся через зависимость\n
    redis : Redis\n
        Клиент Redis для кэширования, создаётся через зависимость\n

    Возвращает:\n
    ----------\n
    List[MapResponseModel]\n
        Отсортированный по orbit_id список моделей данных орбит, содержащих информацию
        для построения карты начальных условий
    """

    start_time = time.time()
    # --- формируем уникальный ключ кэша ---
    key = f"map:{filter_groups}:{limit}:{offset}"
    # --- пробуем достать данные из кэша ---
    cached = await redis.get(key)
    if cached:
        data = json.loads(cached)
        end_time = time.time()
        print(
            f"DEBUG: GET FROM REDIS /get_map: {end_time - start_time:.4f} sec, get {len(data)} orbits"
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
        f"DEBUG: /get_map: request to DB {end_time - start_time:.4f} sec, get {len(result)} orbits"
    )
    res = [
        MapResponseModel(
            orbit_id=row.orbit_id,
            x=row.x,
            z=row.z,
            vy=row.vy,
            abs_v=row.abs_v,
            stable=row.stable,
            stability_ind_1=row.stability_ind_1,
            stability_ind_2=row.stability_ind_2,
            stability_ind_3=row.stability_ind_3,
            dist_primary=row.dist_primary,
            dist_secondary=row.dist_secondary,
            cj=row.cj,
            ax=row.ax,
            ay=row.ay,
            az=row.az,
            family_tag=row.family_tag,
            lib_point=row.lib_point,
        ).model_dump()
        for row in result
    ]
    res = sorted(res, key=lambda orbit: orbit["orbit_id"])
    if key == default_map_key:
        await redis.set(key, json.dumps(res))
    else:
        await redis.set(key, json.dumps(res), ex=43200)
    print(f"DEBUG: /get_map SAVED NEW KEY IN REDIS")
    return res


@orbit_view_router.get(
    "/get_count",
    response_model=int,
    summary="Получить количество орбит согласно фильтрам",
)
async def get_count(
    filter_groups: str = Query(None),
    limit: int = Query(None),
    offset: int = Query(None),
    session: Session = Depends(db.create_session),
    repo: OrbitViewRepo = Depends(create_orbit_view_repo),
):
    start_time = time.time()
    result = repo.get_count(
        session,
        QueryParamsModel(
            filter_groups=json.loads(filter_groups) if filter_groups else [],
            limit=limit,
            offset=offset,
        ),
    )
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"get_count: Функция выполнилась за {execution_time:.4f} секунд")
    return result


@orbit_view_router.get(
    "/get_nearest_orbit",
    response_model=OneOrbitResponseModel,
    summary="Получить ближайшую орбиту по заданным x и z",
)
async def get_nearest_orbit(
    x: float,
    z: float,
    session=Depends(db.create_session),
    repo: OrbitViewRepo = Depends(create_orbit_view_repo),
    redis: Redis = Depends(get_redis),
):
    """
    Возвращает данные орбиты, наиболее близкой к заданным координатам x и z\n

    Параметры:\n
    ----------\n
    x : float\n
        Координата X для поиска ближайшей орбиты\n
    z : float\n
        Координата Z для поиска ближайшей орбиты\n
    session : Session\n
        Сессия SQLAlchemy для подключения к БД, создаётся через зависимость\n
    repo : OrbitViewRepo\n
        Репозиторий для работы с представлением орбит, создаётся через зависимость\n
    redis : Redis\n
        Клиент Redis для кэширования, создаётся через зависимость\n

    Возвращает:\n
    ----------\n
    OneOrbitResponseModel\n
        Модель ответа, содержащая данные ближайшей к заданным координатам орбиты
    """

    start_time = time.time()
    # ----- Создаём ключ кэша -----
    key = f"nearest:{x}:{z}"
    # ----- Пробуем достать из Redis -----
    cached = await redis.get(key)
    if cached:
        data = json.loads(cached)
        end_time = time.time()
        print(f"DEBUG: GET FROM REDIS /get_map: {end_time - start_time:.4f} sec")
        return data

    # ----- Запрос в базу -----

    row = repo.get_nearest_orbit(session, x, z)
    end_time = time.time()
    print(f"DEBUG: /get_nearest_orbit: completed for {end_time - start_time:.4f} sec")

    # ----- Собираем модель -----
    result = OneOrbitResponseModel(
        orbit_id=row.orbit_id,
        x=row.x,
        z=row.z,
        ax=row.ax,
        ay=row.ay,
        az=row.az,
        vy=row.vy,
        t=row.t,
        cj=row.cj,
        dist_primary=row.dist_primary,
        dist_secondary=row.dist_secondary,
        lib_point=row.lib_point,
        family_tag=row.family_tag,
        stable=row.stable,
    ).model_dump()

    # ----- Пишем в кэш -----
    if key == default_near_key:
        await redis.set(key, json.dumps(result))
    else:
        await redis.set(key, json.dumps(result), ex=43200)
    print(f"DEBUG: /get_nearest_orbit SAVED NEW KEY IN REDIS")
    return result


@orbit_view_router.get(
    "/get_next_orbit",
    response_model=OrbitViewModel,
    summary="Получить ближайшую орбиту по заданным x и z",
)
async def get_next_orbit(
    lib_point: str,
    family_tag: str,
    id: int,
    session: Session = Depends(db.create_session),
    repo: OrbitViewRepo = Depends(create_orbit_view_repo),
    redis: Redis = Depends(get_redis),
):
    """
    Возвращает следующую орбиту в указанном семействе относительно заданного идентификатора\n

    Параметры:\n
    ----------\n
    lib_point : str\n
        Точка либрации\n
    family_tag : str\n
        Тег семейства орбит\n
    id : int\n
        Идентификатор текущей орбиты, относительно которой ищется следующая\n
    session : Session\n
        Сессия SQLAlchemy для подключения к БД, создаётся через зависимость\n
    repo : OrbitViewRepo\n
        Репозиторий для работы с представлениями орбит, создаётся через зависимость\n
    redis : Redis\n
        Клиент Redis для кэширования, создаётся через зависимость\n

    Возвращает:\n
    ----------\n
    OrbitViewModel\n
        Модель ответа, содержащая данные следующей орбиты в указанном семействе
    """

    start_time = time.time()

    # --- формируем уникальный ключ кэша ---
    key = f"next_orbit:{lib_point}:{family_tag}:{id}"
    # --- пробуем достать данные из кэша ---
    cached = await redis.get(key)
    if cached:
        data = json.loads(cached)
        end_time = time.time()
        print(f"DEBUG: GET FROM REDIS /get_next_orbit: {end_time - start_time:.4f} sec")
        return data

    result = repo.get_next_orbit_by_id(session, id, family_tag, lib_point)
    end_time = time.time()
    print(f"DEBUG: /get_next_orbit: {end_time - start_time:.4f} sec")
    res = result.model_dump()
    if key == default_next_key:
        await redis.set(key, json.dumps(res))
    else:
        await redis.set(key, json.dumps(res), ex=43200)
    print(f"DEBUG: /get_next_orbit SAVED NEW KEY IN REDIS")

    return res


@orbit_view_router.get(
    "/get_prev_orbit",
    response_model=OrbitViewModel,
    summary="Получить ближайшую орбиту по заданным x и z",
)
async def get_prev_orbit(
    lib_point: str,
    family_tag: str,
    id: int,
    session: Session = Depends(db.create_session),
    repo: OrbitViewRepo = Depends(create_orbit_view_repo),
    redis: Redis = Depends(get_redis),
):
    """
    Возвращает предыдущую орбиту в указанном семействе относительно заданного идентификатора\n

    Параметры:\n
    ----------\n
    lib_point : str\n
        Точка либрации\n
    family_tag : str\n
        Тег семейства орбит\n
    id : int\n
        Идентификатор текущей орбиты, относительно которой ищется следующая\n
    session : Session\n
        Сессия SQLAlchemy для подключения к БД, создаётся через зависимость\n
    repo : OrbitViewRepo\n
        Репозиторий для работы с представлениями орбит, создаётся через зависимость\n
    redis : Redis\n
        Клиент Redis для кэширования, создаётся через зависимость\n

    Возвращает:\n
    ----------\n
    OrbitViewModel\n
        Модель ответа, содержащая данные предыдущей орбиты в указанном семействе
    """

    start_time = time.time()

    # --- формируем уникальный ключ кэша ---
    key = f"prev_orbit:{lib_point}:{family_tag}:{id}"
    # --- пробуем достать данные из кэша ---
    cached = await redis.get(key)
    if cached:
        data = json.loads(cached)
        end_time = time.time()
        print(f"DEBUG: GET FROM REDIS /get_prev_orbit: {end_time - start_time:.4f} sec")
        return data

    result = repo.get_prev_orbit_by_id(session, id, family_tag, lib_point)
    end_time = time.time()
    print(f"DEBUG: /get_prev_orbit: {end_time - start_time:.4f} sec")
    res = result.model_dump()
    if key == default_prev_key:
        await redis.set(key, json.dumps(res))
    else:
        await redis.set(key, json.dumps(res), ex=43200)
    print(f"DEBUG: /get_prev_orbit SAVED NEW KEY IN REDIS")

    return res


@orbit_view_router.get(
    "/get_family_param",
    response_model=list[FamilyParamResponseModel],
    summary="Получить параметры семейства орбит",
)
async def get_family_param(
    lib_point: str,
    family_tag: str,
    param_name_x: str,
    param_name_y: str,
    param_name_z: str,
    session: Session = Depends(db.create_session),
    repo: OrbitViewRepo = Depends(create_orbit_view_repo),
    redis: Redis = Depends(get_redis),
):
    """
    Возвращает параметры орбит указанного семейства для трёхмерной визуализации\n

    Параметры:\n
    ----------\n
    lib_point : str\n
        Точка либрации\n
    family_tag : str\n
        Тег семейства орбит\n
    param_name_x : str\n
        Название параметра, который будет использоваться в качестве координаты X\n
    param_name_y : str\n
        Название параметра, который будет использоваться в качестве координаты Y\n
    param_name_z : str\n
        Название параметра, который будет использоваться в качестве координаты Z\n
    session : Session\n
        Сессия SQLAlchemy для подключения к БД, создаётся через зависимость\n
    repo : OrbitViewRepo\n
        Репозиторий для работы с представлением орбит, создаётся через зависимость\n
    redis : Redis\n
        Клиент Redis для кэширования, создаётся через зависимость\n

    Возвращает:\n
    ----------\n
    list[FamilyParamResponseModel]\n
        Список моделей, содержащих выбранные параметры орбит указанного семейства
    """

    start_time = time.time()

    # --- формируем уникальный ключ кэша ---
    key = f"family_param:{lib_point}:{family_tag}:{param_name_x}:{param_name_y}:{param_name_z}"
    print(f"DEBUG: KEY = {key}")
    # --- пробуем достать данные из кэша ---
    cached = await redis.get(key)
    if cached:
        data = json.loads(cached)
        end_time = time.time()
        print(
            f"DEBUG: GET FROM REDIS /get_family_param: completed for {end_time - start_time:.4f} sec, get {len(data)} records"
        )
        return data

    result = repo.get_family_param(
        session, lib_point, family_tag, param_name_x, param_name_y, param_name_z
    )
    print(f"DEBUG: result = {len(result)}")
    end_time = time.time()
    print(
        f"DEBUG: /get_family_param: completed for {end_time - start_time:.4f} sec, get {len(result)} records"
    )
    res = [
        FamilyParamResponseModel(
            orbit_id=row.orbit_id,
            param_x=row.param_x,
            param_y=row.param_y,
            param_z=row.param_z,
            x=row.x,
            z=row.z,
            cj=row.cj,
        ).model_dump()
        for row in result
    ]
    res.sort(key=lambda x: x["orbit_id"])
    if key == default_fam_param_key:
        await redis.set(key, json.dumps(res))
    else:
        await redis.set(key, json.dumps(res), ex=3)
    print(f"DEBUG: /get_family_param SAVED NEW KEY IN REDIS")
    print(f"DEBUG: RESULT = {len(res)}")
    return res


@orbit_view_router.get(
    "/get_Broucke",
    response_model=list[BrouckeResponseModel],
    summary="Получить данные для диаграммы Брука",
)
async def get_Broucke(
    filter_groups: str = Query(None),
    limit: int = Query(None),
    offset: int = Query(None),
    session: Session = Depends(db.create_session),
    repo: OrbitViewRepo = Depends(create_orbit_view_repo),
    redis: Redis = Depends(get_redis),
):
    """
    Возвращает данные орбит для построения диаграммы Брука\n

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
    repo : OrbitViewRepo\n
        Репозиторий для работы с представлениями орбит, создаётся через зависимость\n
    redis : Redis\n
        Клиент Redis для кэширования, создаётся через зависимость\n

    Возвращает:\n
    ----------\n
    List[BrouckeResponseModel]\n
        Отсортированный по orbit_id список моделей данных орбит, содержащих информацию
        для построения диаграммы Брука
    """

    start_time = time.time()

    # --- формируем уникальный ключ кэша ---
    key = f"get_Broucke:{filter_groups}:{limit}:{offset}"
    # --- пробуем достать данные из кэша ---
    cached = await redis.get(key)
    if cached:
        data = json.loads(cached)
        end_time = time.time()
        print(
            f"DEBUG: GET FROM REDIS /get_Broucke: completed for {end_time - start_time:.4f} sec, get {len(data)} records"
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
        f"DEBUG: /get_Broucke: completed for {end_time - start_time:.4f} sec, get {len(result)} records"
    )

    res = [
        BrouckeResponseModel(
            orbit_id=row.orbit_id,
            x=row.x,
            z=row.z,
            vy=row.vy,
            t=row.t,
            ax=row.ax,
            ay=row.ay,
            az=row.az,
            cj=row.cj,
            dist_primary=row.dist_primary,
            dist_secondary=row.dist_secondary,
            stable=row.stable,
            family_tag=row.family_tag,
            lib_point=row.lib_point,
            alpha=row.alpha,
            beta=row.beta,
        ).model_dump()  # Добавляем преобразование в словарь
        for row in result
    ]

    # Сортируем список словарей по orbit_id
    res = sorted(res, key=lambda orbit: orbit["orbit_id"])
    if key == default_broucke_key:
        await redis.set(key, json.dumps(res))
    else:
        await redis.set(key, json.dumps(res), ex=43200)
    print(f"DEBUG: /get_Broucke SAVED NEW KEY IN REDIS")

    return res
