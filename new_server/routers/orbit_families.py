import json
import time

from database import db
from dependencies import get_redis
from fastapi import APIRouter, Depends, Query
from redis.asyncio import Redis
from sqlalchemy.orm import Session

orbit_families_router = APIRouter(prefix="/orbit_families", tags=["Orbit_families"])

from models import OrbitFamilyModel, QueryParamsModel
from repo import ReadRepo
from tables import OrbitFamiliesTable

OrbitFamilyRepo = ReadRepo[OrbitFamiliesTable, OrbitFamilyModel]


def create_orbit_family_repo() -> OrbitFamilyRepo:
    return OrbitFamilyRepo(OrbitFamiliesTable, OrbitFamilyModel)


default_fam_key = "family:[{'log_op':'NONE', 'filters':[{'field':'lib_point','op':'like','value':'L1'}]},{'log_op':'OR','filters':[{'field':'family_tag','op':'like','value':'L'},{'field':'family_tag','op':'like','value':'V'},{'field':'family_tag','op':'like','value':'L.2P1'},{'field':'family_tag','op':'like','value':'L.3P1'},{'field':'family_tag','op':'like','value':'L.4P1'},{'field':'family_tag','op':'like','value':'L.2P1.2P1'},{'field':'family_tag','op':'like','value':'L.2P1.3P1'},{'field':'family_tag','op':'like','value':'L.2P1.3P2'},{'field':'family_tag','op':'like','value':'H.2P1'},{'field':'family_tag','op':'like','value':'H.2P2'},{'field':'family_tag','op':'like','value':'H.2P3'},{'field':'family_tag','op':'like','value':'H.3P1'},{'field':'family_tag','op':'like','value':'H.3P2'},{'field':'family_tag','op':'like','value':'H.3P3'},{'field':'family_tag','op':'like','value':'H.4P1'},{'field':'family_tag','op':'like','value':'Q'},{'field':'family_tag','op':'like','value':'H_s'},{'field':'family_tag','op':'like','value':'H_n'}]}]:None:None"


@orbit_families_router.get(
    "/get_families",
    response_model=list[OrbitFamilyModel],
    summary="Получить параметры семейства орбит",
)
async def get_families(
    filter_groups: str = Query(None),
    limit: int = Query(None),
    offset: int = Query(None),
    session: Session = Depends(db.create_session),
    repo: OrbitFamilyRepo = Depends(create_orbit_family_repo),
    redis: Redis = Depends(get_redis),
):
    """
    Возвращает фрагмент данных о семействах орбит\n

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
    repo : OrbitFamilyRepo\n
        Репозиторий для работы с данными семейств орбит, создаётся через зависимость\n
    redis : Redis\n
        Клиент Redis для кэширования, создаётся через зависимость\n

    Возвращает:\n
    ----------\n
    List[OrbitFamilyModel]
        Список моделей семейств орбит, соответствующих заданным фильтрам и пагинации
    """

    start_time = time.time()
    # ----- Формируем уникальный ключ кэша -----
    key = f"family:{filter_groups}:{limit}:{offset}"
    # ----- Проверяем кэш -----
    cached = await redis.get(key)
    if cached:
        data = json.loads(cached)
        end_time = time.time()
        print(
            f"DEBUG: GET FROM REDIS /get_families: {end_time - start_time:.4f} sec, get {len(data)} families"
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
        f"DEBUG: /get_families: request to DB {end_time - start_time:.4f} sec, get {len(result)} families"
    )

    res = [
        OrbitFamilyModel(
            id=row.id,
            lib_point=row.lib_point,
            family_tag=row.family_tag,
            min_x=row.min_x,
            max_x=row.max_x,
            min_y=row.min_y,
            max_y=row.max_y,
            min_z=row.min_z,
            max_z=row.max_z,
            min_vx=row.min_vx,
            max_vx=row.max_vx,
            min_vy=row.min_vy,
            max_vy=row.max_vy,
            min_vz=row.min_vz,
            max_vz=row.max_vz,
            min_abs_v=row.min_abs_v,
            max_abs_v=row.max_abs_v,
            min_t=row.min_t,
            max_t=row.max_t,
            min_cj=row.min_cj,
            max_cj=row.max_cj,
            min_ax=row.min_ax,
            max_ax=row.max_ax,
            min_ay=row.min_ay,
            max_ay=row.max_ay,
            min_az=row.min_az,
            max_az=row.max_az,
            min_dist_primary=row.min_dist_primary,
            max_dist_primary=row.max_dist_primary,
            min_dist_secondary=row.min_dist_secondary,
            max_dist_secondary=row.max_dist_secondary,
            min_stability_ind_1=row.min_stability_ind_1,
            max_stability_ind_1=row.max_stability_ind_1,
            min_stability_ind_2=row.min_stability_ind_2,
            max_stability_ind_2=row.max_stability_ind_2,
            min_stability_ind_3=row.min_stability_ind_3,
            max_stability_ind_3=row.max_stability_ind_3,
            min_alpha=row.min_alpha,
            max_alpha=row.max_alpha,
            min_beta=row.min_beta,
            max_beta=row.max_beta,
        ).model_dump()
        for row in result
    ]

    # ----- Сохраняем в кэш (TTL = 20 сек) -----
    if key == default_fam_key:
        await redis.set(key, json.dumps(res))
    else:
        await redis.set(key, json.dumps(res), ex=43200)
    print(f"DEBUG: /get_families SAVED NEW KEY IN REDIS")
    return result
