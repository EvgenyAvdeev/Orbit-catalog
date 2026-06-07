import csv
import os
from io import StringIO

from database import db
from fastapi import APIRouter, Query, Response
from fastapi.responses import FileResponse
from tables import (
    OrbitFamiliesTable,
    OrbitsTable,
    PoincareSectionsTable,
    TrajectoryPointsTable,
)

download_router = APIRouter(prefix="/download", tags=["Downloads"])
from typing import Any, Dict, List

import pandas as pd
from models import (
    CreateOrbitFamilyModel,
    FilterGroup,
    FilterModel,
    LogicalOpEnum,
    OrbitFamilyModel,
    QueryParamsModel,
    UpdateOrbitFamilyModel,
)
from models import FilterOpEnum as Op
from repo import ReadRepo
from sqlalchemy import and_, select
from sqlalchemy.orm import joinedload


@download_router.get(
    "/get_data_for_script",
    summary="Получить данные для расчетов",
)
async def get_data_for_script(lib_point: str = Query(None), family: str = Query(None)):
    """
    Возвращает датасет с начальными данными для расчетов\n

    Параметры:\n
    ----------\n
    lib_point: str\n
        Точка либрации\n
    family: str\n
        Семейство орбит\n

    Возвращает:\n
    ----------\n
    Файл с датасетом\n
    """

    prefix = "DB_calc/computation_funcs_and_files/computation_files/"
    file_name = lib_point + "." + family + ".csv"
    file_path = prefix + file_name
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    return FileResponse(path=file_path, filename=f"{file_name}", media_type="text/csv")


@download_router.get(
    "/get_data_from_DB",
    summary="Получить данные из БД",
)
async def get_data_from_DB(
    what_return: str = Query(None),
    lib_point: str = Query(None),
    family: str = Query(None),
    param: str = Query(None),
    param_start: float = Query(None),
    param_end: float = Query(None),
):
    """
    Получает данные из базы данных и возвращает их в формате CSV\n

    Параметры:\n
    ----------\n
    what_return: str\n
        Тип возвращаемых данных: "orbits", "trajectory" или "sections"\n
    lib_point: str\n
        Точка либрации для фильтрации\n
    family: str\n
        Семейство орбит для фильтрации\n
    param: str\n
        Параметр для фильтрации по диапазону (x, y, vy, t и др.)\n
    param_start: float\n
        Начальное значение параметра для фильтрации по диапазону\n
    param_end: float\n
        Конечное значение параметра для фильтрации по диапазону\n

    Возвращает:\n
    ----------\n
    Response\n
        CSV-файл с запрошенными данными\n

    Примечания:\n
    ----------\n
    - Поддерживаемые параметры для фильтрации: x, y, vy, abs_v, t, floke_1_r,
        floke_2_r, floke_3_r, floke_4_r, floke_5_r, floke_6_r, floke_1_im,
        floke_2_im, floke_3_im, floke_4_im, floke_5_im, floke_6_im, ax, ay, az,
        dist_primary, dist_secondary, cj, stable\n
    - Если не найдено ни одной записи, возвращается пустой CSV-файл
    """
    param_mapping = {
        "x": OrbitsTable.x,
        "y": OrbitsTable.y,
        "vy": OrbitsTable.vy,
        "abs_v": OrbitsTable.abs_v,
        "t": OrbitsTable.t,
        "floke_1_r": OrbitsTable.floke_1_r,
        "floke_2_r": OrbitsTable.floke_2_r,
        "floke_3_r": OrbitsTable.floke_3_r,
        "floke_4_r": OrbitsTable.floke_4_r,
        "floke_5_r": OrbitsTable.floke_5_r,
        "floke_6_r": OrbitsTable.floke_6_r,
        "floke_1_im": OrbitsTable.floke_1_im,
        "floke_2_im": OrbitsTable.floke_2_im,
        "floke_3_im": OrbitsTable.floke_3_im,
        "floke_4_im": OrbitsTable.floke_4_im,
        "floke_5_im": OrbitsTable.floke_5_im,
        "floke_6_im": OrbitsTable.floke_6_im,
        "ax": OrbitsTable.ax,
        "ay": OrbitsTable.ay,
        "az": OrbitsTable.az,
        "dist_primary": OrbitsTable.dist_primary,
        "dist_secondary": OrbitsTable.dist_secondary,
        "cj": OrbitsTable.cj,
        "stable": OrbitsTable.stable,
    }
    session = db.create_session()
    try:
        family_id = None
        if family or lib_point:
            filter = QueryParamsModel(
                filter_groups=[
                    FilterGroup(
                        log_op=LogicalOpEnum.NONE,
                        filters=[
                            FilterModel(field="family_tag", op=Op.lk, value=family),
                            FilterModel(field="lib_point", op=Op.lk, value=lib_point),
                        ],
                    )
                ]
            )
            family_repo = ReadRepo(OrbitFamiliesTable, OrbitFamilyModel)
            family_records = family_repo.get_chunk(session, filter)
            if family_records:
                family_id = family_records[0].id
            else:
                output = StringIO()
                writer = csv.writer(output)
                writer.writerow([])
                return Response(
                    content=output.getvalue(),
                    media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=data.csv"},
                )

        if what_return == "orbits":
            query = select(OrbitsTable)
            if family_id:
                query = query.where(OrbitsTable.family_id == family_id)
            if param and param_start is not None and param_end is not None:
                if param in param_mapping:
                    param_field = param_mapping[param]
                    query = query.where(
                        and_(param_field >= param_start, param_field <= param_end)
                    )
            result = session.execute(query)
            records = result.scalars().all()
            model = OrbitsTable

        elif what_return == "trajectory":
            query = select(TrajectoryPointsTable).options(
                joinedload(TrajectoryPointsTable.orbits)
            )
            # Фильтр по орбитам через подзапрос
            if family_id or (
                param and param_start is not None and param_end is not None
            ):
                orbit_subquery = select(OrbitsTable.id)
                if family_id:
                    orbit_subquery = orbit_subquery.where(
                        OrbitsTable.family_id == family_id
                    )
                if param and param_start is not None and param_end is not None:
                    if param in param_mapping:
                        param_field = param_mapping[param]
                        orbit_subquery = orbit_subquery.where(
                            and_(param_field >= param_start, param_field <= param_end)
                        )
                query = query.where(TrajectoryPointsTable.orbit_id.in_(orbit_subquery))
            result = session.execute(query)
            records = result.scalars().all()
            model = TrajectoryPointsTable

        elif what_return == "sections":
            query = select(PoincareSectionsTable).options(
                joinedload(PoincareSectionsTable.orbits)
            )
            if family_id or (
                param and param_start is not None and param_end is not None
            ):
                orbit_subquery = select(OrbitsTable.id)
                if family_id:
                    orbit_subquery = orbit_subquery.where(
                        OrbitsTable.family_id == family_id
                    )
                if param and param_start is not None and param_end is not None:
                    if param in param_mapping:
                        param_field = param_mapping[param]
                        orbit_subquery = orbit_subquery.where(
                            and_(param_field >= param_start, param_field <= param_end)
                        )
                query = query.where(PoincareSectionsTable.orbit_id.in_(orbit_subquery))
            result = session.execute(query)
            records = result.scalars().all()
            model = PoincareSectionsTable

        else:
            return Response(
                content="Invalid what_return parameter",
                media_type="text/plain",
                status_code=400,
            )

        dataset = [
            {
                column.name: getattr(record, column.name)
                for column in model.__table__.columns
            }
            for record in records
        ]

        output = StringIO()
        if dataset:
            writer = csv.DictWriter(output, fieldnames=dataset[0].keys())
            writer.writeheader()
            writer.writerows(dataset)
        else:
            writer = csv.writer(output)
            writer.writerow([])

        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=data.csv"},
        )

    finally:
        session.close()


@download_router.get(
    "/get_docs",
    summary="Получить документацию",
)
async def get_docs():
    """
    Возвращает пользовательскую документацию\n

    Возвращает:\n
    ----------\n
    PDF файл с документацией\n
    """
    file_name = "docs.pdf"
    file_path = "docs/docs.pdf"
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    return FileResponse(path=file_path, filename=f"{file_name}", media_type="pdf")


@download_router.get(
    "/get_script",
    summary="Получить скрипт",
)
async def get_script():
    """
    Возвращает код скрипта\n

    Возвращает:\n
    ----------\n
    Файл со скриптом\n
    """
    file_name = "orbit_visibility.ipynb"
    file_path = "script/orbit_visibility.ipynb"
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    return FileResponse(
        path=file_path, filename=f"{file_name}", media_type="application/json"
    )
