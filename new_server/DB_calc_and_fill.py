import math
from typing import List

import pandas as pd
from database import db
from DB_calc.computation_funcs_and_files.preprocessing_functions import *
from models import (
    CreateOrbitFamilyModel,
    CreateOrbitModel,
    CreatePoincareSectionModel,
    CreateTrajectoryPointModel,
    FilterGroup,
    FilterModel,
    LogicalOpEnum,
    OrbitFamilyModel,
    OrbitModel,
    PoincareSectionModel,
    QueryParamsModel,
    TrajectoryPointModel,
    UpdateOrbitFamilyModel,
    UpdateOrbitModel,
    UpdatePoincareSectionModel,
    UpdateTrajectoryPointModel,
)
from models import FilterOpEnum as Op
from repo import CreateRepo, CRUDRepo
from sqlalchemy.orm import Session
from tables import (
    OrbitFamiliesTable,
    OrbitsTable,
    PoincareSectionsTable,
    TrajectoryPointsTable,
)


def fill_orbits_family(orbit_family: pd.DataFrame, session: Session) -> None:
    """
    Загружает набор данных о семействах орбит в базу данных
    Параметры:
    ----------
    orbit_family : pd.DataFrame
        DataFrame, содержащий данные о семействах орбит для загрузки
    session : Session
        Сессия SQLAlchemy

    Возвращает:
    ----------
    None
    """
    repo = CRUDRepo[
        OrbitFamiliesTable,
        OrbitFamilyModel,
        CreateOrbitFamilyModel,
        UpdateOrbitFamilyModel,
    ](
        OrbitFamiliesTable,
        OrbitFamilyModel,
        CreateOrbitFamilyModel,
        UpdateOrbitFamilyModel,
    )

    data = orbit_family.to_dict(orient="records")
    items = [CreateOrbitFamilyModel.model_validate(element) for element in data]
    result = repo.bulk_create_records(items, session)
    print(f"INFO: LOADED {len(items)} families")
    session.commit()
    session.close()


def fill_orbit(orbit: pd.DataFrame, session: Session) -> None:
    """
    Загружает запись об орбите в базу данных

    Параметры:
    ----------
    orbit : pd.DataFrame
        DataFrame, содержащий данные об орбите для загрузки
    session : Session
        Сессия SQLAlchemy

    Возвращает:
    ----------
    None
    """
    repo = CRUDRepo[OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel](
        OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel
    )
    orbit_model = CreateOrbitModel.model_validate(orbit.iloc[0].to_dict())
    result = repo.bulk_create_records([orbit_model], session)
    print("INFO: ORBIT LOADED")
    session.flush()
    session.commit()


def fill_poincare_sections(section: pd.DataFrame, session: Session) -> None:
    """
    Загружает набор данных о сечениях Пуанкаре в базу данных

    Параметры:
    ----------
    section : pd.DataFrame
        DataFrame, содержащий данные о сечениях Пуанкаре для загрузки
    session : Session
        Сессия SQLAlchemy

    Возвращает:
    ----------
    None
    """
    repo = CreateRepo[
        PoincareSectionsTable, PoincareSectionModel, CreatePoincareSectionModel
    ](PoincareSectionsTable, PoincareSectionModel, CreatePoincareSectionModel)
    data = section.to_dict(orient="records")
    items = [CreatePoincareSectionModel.model_validate(element) for element in data]
    result = repo.bulk_create_records(items, session)
    print("INFO: SECTIONS LOADED")


def fill_trajectory_points(trajectory: pd.DataFrame, session: Session) -> None:
    """
    Загружает набор данных о точках траекторий в базу данных

    Параметры:
    ----------
    trajectory : pd.DataFrame
        DataFrame, содержащий данные о точках траекторий для загрузки
    session : Session
        Сессия SQLAlchemy

    Возвращает:
    ----------
    None
    """
    repo = CreateRepo[
        TrajectoryPointsTable, TrajectoryPointModel, CreateTrajectoryPointModel
    ](TrajectoryPointsTable, TrajectoryPointModel, CreateTrajectoryPointModel)
    data = trajectory.to_dict(orient="records")
    items = [CreateTrajectoryPointModel.model_validate(element) for element in data]
    result = repo.bulk_create_records(items, session)
    print("INFO: TRAJECTORIES LOADED")


def calc_hashes_batch(records: pd.DataFrame, family_id: int) -> pd.Series:
    """
    Вычисляет уникальные хеш-идентификаторы для пакета записей траекторий.

    Функция создаёт уникальный хеш для каждой строки DataFrame на основе идентификатора семейства,
    координат (x, v) и индекса строки. Координаты округляются до 10 знаков после запятой для
    обеспечения консистентности при вычислении хешей для числовых данных с плавающей точкой.

    Параметры:
    ----------
    records : pd.DataFrame
        DataFrame, содержащий записи орбит семейства
    family_id : int
        Идентификатор семейства орбит

    Возвращает:
    ----------
    pd.Series
        Серия строк, содержащая уникальные MD5-хеши для каждой орбиты
    """
    records_cp = records.copy()
    try:
        records_cp["combined"] = (
            records_cp["family_id"].astype(str)
            + round(records_cp["x"] * (10**10)).astype(str)
            + round(records_cp["v"] * (10**10)).astype(str)
            + records_cp.index.astype(str)
        )
    except Exception:
        records_cp["combined"] = (
            records_cp["family_id"].astype(str)
            + round(records_cp["x"] * (10**10)).astype(str)
            + round(records_cp["vy"] * (10**10)).astype(str)
            + records_cp.index.astype(str)
        )
    records_cp["unique_id"] = records_cp["combined"].apply(
        lambda x: hashlib.md5(x.encode()).hexdigest()
    )
    return records_cp["unique_id"]


def get_existing_hashes(session: Session) -> set:
    """
    Получает множество уникальных хеш-идентификаторов всех орбит, уже существующих в базе данных

    Параметры:
    ----------
    session : Session
        Сессия SQLAlchemy

    Возвращает:
    ----------
    set
        Множество строк, содержащее все уникальные хеш-идентификаторы
    """
    repo = CRUDRepo[OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel](
        OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel
    )

    existing_hashes = set()
    DB_data = repo.get_chunk(session)
    for record in DB_data:
        existing_hashes.add(record.unique_id)

    return existing_hashes


def delete_orbit(id: int, session: Session) -> None:
    """
    Удаляет запись об орбите из базы данных по её идентификатору

    Параметры:
    ----------
    id : int
        Идентификатор орбиты, которую необходимо удалить
    session : Session
        Сессия SQLAlchemy

    Возвращает:
    ----------
    None
    """
    repo = CRUDRepo[OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel](
        OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel
    )
    repo.delete(id, session)


def delete_section(section: pd.DataFrame, session: Session) -> None:
    """
    Удаляет записи о сечениях Пуанкаре из базы данных

    Параметры:
    ----------
    section : pd.DataFrame
        DataFrame, содержащий данные о сечениях Пуанкаре для удаления
    session : Session
        Сессия SQLAlchemy

    Возвращает:
    ----------
    None
    """
    repo = CRUDRepo[
        PoincareSectionsTable,
        PoincareSectionModel,
        CreatePoincareSectionModel,
        UpdatePoincareSectionModel,
    ](
        PoincareSectionsTable,
        PoincareSectionModel,
        CreatePoincareSectionModel,
        UpdatePoincareSectionModel,
    )
    for i in range(len(section)):
        record = section.iloc[[i]]
        repo.delete(record.id, session)


def load_orbits_batch(
    new_orbits_data: List[List[pd.DataFrame]], session: Session
) -> tuple[List[int], List[int]]:
    """
    Загружает данные о сечениях Пуанкаре и точках траекторий

    Параметры:
    ----------
    new_orbits_data : List[List[pd.DataFrame]]
        Список списков DataFrame, где каждый внутренний список содержит:
        - orbit_df: DataFrame с данными об одной орбите.
        - sections_df: DataFrame с данными о сечениях Пуанкаре для этой орбиты.
        - trajectories_df: DataFrame с данными о точках траекторий для этой орбиты.
        - orbit_id: Целочисленный идентификатор орбиты.
    session : Session
        Сессия SQLAlchemy

    Возвращает:
    ----------
    tuple[List[int], List[int]]
        Кортеж из двух списков:
        - successful_orbits: Список идентификаторов успешно загруженных орбит.
        - failed_orbits: Список идентификаторов орбит, загрузка которых завершилась с ошибкой.
    """
    successful_orbits = []
    failed_orbits = []

    for orbit_df, sections_df, trajectories_df, orbit_id in new_orbits_data:
        print(f"INFO: START OF LOADING orbit with id = {orbit_id}")
        try:
            fill_poincare_sections(sections_df, session)

            try:
                fill_trajectory_points(trajectories_df, session)
                session.commit()
                print(f"INFO: LOADING COMPLETED orbit with id = {orbit_id}")
                successful_orbits.append(orbit_id)

            except Exception as e:
                print(
                    f"ERROR: Failed to fill trajectory points for orbit {orbit_id}: {e}"
                )
                session.rollback()
                delete_section(sections_df, session)
                delete_orbit(orbit_df.iloc[0]["id"], session)
                failed_orbits.append(orbit_id)

        except Exception as e:
            print(f"ERROR: Failed to fill poincare sections for orbit {orbit_id}: {e}")
            session.rollback()
            delete_orbit(orbit_df.iloc[0]["id"], session)
            failed_orbits.append(orbit_id)
    return successful_orbits, failed_orbits


def compare_tag(tag: str, session: Session) -> bool:
    """
    Проверяет, существует ли указанный тег в базе данных семейств орбит

    Параметры:
    ----------
    tag : str
        Строка тега в формате "lib_point.family_tag", которую необходимо проверить на существование
    session : Session
        Сессия SQLAlchemy

    Возвращает:
    ----------
    bool
        True, если указанный тег найден в базе данных, иначе False
    """
    repo = CRUDRepo[
        OrbitFamiliesTable,
        OrbitFamilyModel,
        CreateOrbitFamilyModel,
        UpdateOrbitFamilyModel,
    ](
        OrbitFamiliesTable,
        OrbitFamilyModel,
        CreateOrbitFamilyModel,
        UpdateOrbitFamilyModel,
    )
    existing_tags = []
    DB_data = repo.get_chunk(session)
    for record in DB_data:
        existing_tags.append(record.lib_point + "." + record.family_tag)
    return tag in existing_tags


def get_fam_shape() -> int:
    """
    Получает общее количество записей в таблице семейств орбит.

    Возвращает:
    ----------
    int
        Общее количество записей в таблице семейств орбит
    """
    repo = CRUDRepo[
        OrbitFamiliesTable,
        OrbitFamilyModel,
        CreateOrbitFamilyModel,
        UpdateOrbitFamilyModel,
    ](
        OrbitFamiliesTable,
        OrbitFamilyModel,
        CreateOrbitFamilyModel,
        UpdateOrbitFamilyModel,
    )
    session = db.create_session()
    count = repo.get_count(session)
    session.close()
    return count


def get_orbit_shape() -> int:
    """
    Получает общее количество записей в таблице орбит

    Возвращает:
    ----------
    int
        Общее количество записей (строк) в таблице орбит
    """
    repo = CRUDRepo[OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel](
        OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel
    )
    session = db.create_session()
    count = repo.get_count(session)
    session.close()
    return count


def get_fam_by_tag(tag: str, session: Session) -> pd.DataFrame:
    """
    Получает запись о семействе орбит по его тегу и возвращает её в виде DataFrame

    Параметры:
    ----------
    tag : str
        Строка тега в формате "lib_point.family_tag"
    session : Session
        Сессия SQLAlchemy

    Возвращает:
    ----------
    pd.DataFrame
        DataFrame, содержащий одну строку с данными найденного семейства орбит
    """
    repo = CRUDRepo[
        OrbitFamiliesTable,
        OrbitFamilyModel,
        CreateOrbitFamilyModel,
        UpdateOrbitFamilyModel,
    ](
        OrbitFamiliesTable,
        OrbitFamilyModel,
        CreateOrbitFamilyModel,
        UpdateOrbitFamilyModel,
    )
    filter = QueryParamsModel(
        filter_groups=[
            FilterGroup(
                log_op=LogicalOpEnum.NONE,
                filters=[
                    FilterModel(field="family_tag", op=Op.lk, value=tag[3:]),
                    FilterModel(field="lib_point", op=Op.lk, value=tag[:2]),
                ],
            )
        ]
    )
    family = repo.get_chunk(session, filter)
    session.close()
    df = pd.DataFrame([family[0].model_dump()])
    return df


def get_orbit_id_by_fam_id(family_id: int, session: Session) -> int:
    """
    Получает идентификатор последней орбиты для указанного семейства

    Параметры:
    ----------
    family_id : int
        Идентификатор семейства орбит, для которого необходимо найти последнюю орбиту.
    session : Session
        Сессия SQLAlchemy

    Возвращает:
    ----------
    int
        Идентификатор последней орбиты в указанном семействе
    """
    repo = CRUDRepo[OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel](
        OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel
    )
    # session = db.create_session()
    filter = QueryParamsModel(
        filter_groups=[
            FilterGroup(
                log_op=LogicalOpEnum.NONE,
                filters=[FilterModel(field="family_id", op=Op.eq, value=family_id)],
            )
        ]
    )
    orbits = repo.get_chunk(session, filter)
    sorted(orbits, key=lambda orbit: orbit.id)
    session.close()
    return orbits[-1].id


def get_first_orbit_id_by_fam_id(family_id: int, session: Session) -> int:
    """
    Получает идентификатор последней орбиты для указанного семейства

    Параметры:
    ----------
    family_id : int
        Идентификатор семейства орбит, для которого необходимо найти последнюю орбиту.
    session : Session
        Сессия SQLAlchemy

    Возвращает:
    ----------
    int
        Идентификатор последней орбиты в указанном семействе
    """
    repo = CRUDRepo[OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel](
        OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel
    )
    # session = db.create_session()
    filter = QueryParamsModel(
        filter_groups=[
            FilterGroup(
                log_op=LogicalOpEnum.NONE,
                filters=[FilterModel(field="family_id", op=Op.eq, value=family_id)],
            )
        ]
    )
    orbits = repo.get_chunk(session, filter)
    sorted(orbits, key=lambda orbit: orbit.id)
    session.close()
    return orbits[0].id


def calculate_stability_ind_and_a_b() -> None:
    """
    Вычисляет и обновляет индексы устойчивости, а также параметры alpha и beta для орбит в базе данных

    Возвращает:
    ----------
    None
    """
    repo = CRUDRepo[OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel](
        OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel
    )
    session = db.create_session()
    records = repo.get_chunk(session)
    reverse_lamda = set()
    acc = 1e-5
    for record in records:
        print(f"INFO: Orbit {record.id}")
        lamda_list = [
            record.floke_1_r + record.floke_1_im * 1j,
            record.floke_2_r + record.floke_2_im * 1j,
            record.floke_3_r + record.floke_3_im * 1j,
            record.floke_4_r + record.floke_4_im * 1j,
            record.floke_5_r + record.floke_5_im * 1j,
            record.floke_6_r + record.floke_6_im * 1j,
        ]

        for idx, l in enumerate(lamda_list):
            print(f"LAMDA[{idx}] = {l}")

        if not reverse_lamda:
            for i in range(len(lamda_list)):
                for j in range(i + 1, len(lamda_list)):
                    if abs(lamda_list[i] * lamda_list[j] - 1) < acc:
                        reverse_lamda.add(frozenset([i, j]))

        print(f"REVERSE_ARR = {reverse_lamda}")

        stability_inds = []
        alpha = 0
        sum_val = 0
        for pair in reverse_lamda:
            pair_list = list(pair)
            i, j = pair_list[0], pair_list[1]

            stability = (abs(lamda_list[i]) + abs(lamda_list[j])) / 2
            stability_inds.append(stability)

            if 5 in pair:
                continue

            alpha -= lamda_list[i] + lamda_list[j]

        print(f"STABILITY_ARR = {stability_inds}")
        print(f"ALPHA = {alpha}")

        for pair in reverse_lamda:
            pair_list = list(pair)
            i, j = pair_list[0], pair_list[1]

            if 5 in pair:
                continue

            sum_val -= lamda_list[i] ** 2 + lamda_list[j] ** 2

        beta = (alpha**2 + sum_val) / 2
        # print(f"BETA = {beta}")
        if record.stability_ind_1 == 0:
            update_record = UpdateOrbitModel(
                id=record.id,
                stability_ind_1=stability_inds[0],
                stability_ind_2=stability_inds[1],
                stability_ind_3=stability_inds[2],
                alpha=alpha.real,
                beta=beta.real,
            )
            repo.update(update_record, session)


def update_orbit_families() -> None:
    """
    Обновляет минимальные и максимальные значения в записях семейств орбит

    Пропускаемые значения:
        - id, family_id, unique_id
        - stable
        - floke

    Возвращает:
    ----------
    None
    """
    orbit_repo = CRUDRepo[OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel](
        OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel
    )
    family_repo = CRUDRepo[
        OrbitFamiliesTable,
        OrbitFamilyModel,
        CreateOrbitFamilyModel,
        UpdateOrbitFamilyModel,
    ](
        OrbitFamiliesTable,
        OrbitFamilyModel,
        CreateOrbitFamilyModel,
        UpdateOrbitFamilyModel,
    )

    session = db.create_session()

    try:
        families = family_repo.get_chunk(session)

        all_orbits = orbit_repo.get_chunk(session)

        orbits_data = [orbit.model_dump() for orbit in all_orbits]
        orbits_df = pd.DataFrame(orbits_data) if orbits_data else pd.DataFrame()

        skip_columns = {
            "id",
            "family_id",
            "stable",
            "floke_1_r",
            "floke_2_r",
            "floke_3_r",
            "floke_4_r",
            "floke_5_r",
            "floke_6_r",
            "floke_1_im",
            "floke_2_im",
            "floke_3_im",
            "floke_4_im",
            "floke_5_im",
            "floke_6_im",
            "unique_id",
        }
        for family in families:
            family_orbits = orbits_df[orbits_df["family_id"] == family.id]
            if family_orbits.empty:
                continue

            update_data = {"id": family.id}

            for column in orbits_df.columns:
                if column not in skip_columns:
                    values = family_orbits[column].dropna()

                    if not values.empty:
                        update_data[f"min_{column}"] = float(values.min())
                        update_data[f"max_{column}"] = float(values.max())
            update_record = UpdateOrbitFamilyModel(**update_data)
            family_repo.update(update_record, session)

        session.commit()
        print("Orbit families updated successfully")

    except Exception as e:
        session.rollback()
        print(f"Error updating orbit families: {e}")
        raise
    finally:
        session.close()


def compute_DB(tags: List[str], file_names: List[str]) -> None:
    """
    Основная функция для интегрирования и загрузки данных об орбитах в базу данных

    Параметры:
    ----------
    tags : List[str]
        Список тегов семейств орбит в формате "lib_point.family_tag"
    file_names : List[str]
        Список путей к CSV-файлам, содержащим данные об орбитах для соответствующих тегов

    Возвращает:
    ----------
    None
    """
    for tag, file_name in zip(tags, file_names):
        session_fam = db.create_session()
        if not compare_tag(tag, session_fam):
            orbit_families_df = create_orbit_families_step_1([tag])
            fill_orbits_family(orbit_families_df, session_fam)
            print(f"INFO: created family with tag = {tag}")
        else:
            print(f"INFO: already exist family with tag = {tag}")
        session_fam.close()
        orbit_families_df = get_fam_by_tag(tag, session_fam)
        orb = pd.read_csv(file_name)
        family_id = int(
            orbit_families_df.loc[
                (orbit_families_df.family_tag == tag[3:])
                & (orbit_families_df.lib_point == tag[:2]),
                "id",
            ].values[0]
        )

        orb["family_id"] = family_id

        # расчет всех хешей поступивших на вход
        print(f"INFO: Calculating hashes for {len(orb)} orbits in family {tag}")
        hashes = calc_hashes_batch(orb, family_id)
        orb["unique_id"] = hashes

        # получение всех хешей в БД
        session = db.create_session()
        existing_hashes = get_existing_hashes(session)
        session.close()

        # получаем только новые орбиты
        new_orbits_mask = ~orb["unique_id"].isin(existing_hashes)
        new_orbits = orb[new_orbits_mask]
        existing_orbits = orb[~new_orbits_mask]

        print(
            f"INFO: Family {tag}: {len(new_orbits)} new orbits, {len(existing_orbits)} existing orbits"
        )

        if len(new_orbits) == 0:
            print(f"INFO: No new orbits to integrate for family {tag}")
            continue

        new_orbits_data = []
        id_shift = get_orbit_shape()
        session = db.create_session()

        for idx, (_, record) in enumerate(new_orbits.iterrows()):
            record_df = pd.DataFrame([record])

            print(f"START OF INTAGRAION family = {tag}, orbit_id = {idx}")
            orbits_df = compute_properties(
                record_df, fam_name=tag, family_id=family_id, hash=record["unique_id"]
            )
            orbit_columns_to_scale = [
                "x",
                "z",
                "ax",
                "ay",
                "az",
                "dist_primary",
                "dist_secondary",
            ]
            orbits_df.loc[:, orbit_columns_to_scale] = (
                orbits_df[orbit_columns_to_scale] / 10**3
            )
            print(f"DEBUG: {orbits_df[['x', 'cj']]}")
            fill_orbit(orbits_df, session)
            orbit_id = get_orbit_id_by_fam_id(family_id, session)
            print(f"INTAGRATED ORBIT with id: {orbit_id}")
            poincare_sections = compute_poincare_sections(
                record_df, fam_name=tag, orbit_id=orbit_id
            )
            print(f"INTAGRATED SECTIONS")
            trajectories = compute_trajectories(
                record_df, fam_name=tag, orbit_id=orbit_id
            )
            print(f"INTAGRATED TRAJECTORIES")
            poincare_columns_to_scale = ["x", "y", "z"]
            trajectory_orbit_columns_to_scale = ["x", "y", "z"]
            poincare_sections.loc[:, poincare_columns_to_scale] = (
                poincare_sections[poincare_columns_to_scale] / 10**3
            )
            trajectories.loc[:, trajectory_orbit_columns_to_scale] = (
                trajectories[trajectory_orbit_columns_to_scale] / 10**3
            )
            new_orbits_data.append(
                (orbits_df, poincare_sections, trajectories, orbit_id)
            )
        successful, failed = load_orbits_batch(new_orbits_data, session)
        session.close()

        print(
            f"INFO: Family {tag}: {len(successful)} orbits successfully loaded, {len(failed)} failed"
        )


tags = [  # "L1.H_s",
    "L1.H_n",
    "L2.H_s",
    "L2.H_s",
    "L1.V",
    "L2.V",
    "L1.L",
    "L2.L",
    "L1.L.2P1",
    "L2.L.2P1",
    "L1.L.3P1",
    "L2.L.3P1",
    "L1.L.4P1",
    "L2.L.4P1",
    # "L1.L.2P1.2P1",
    # "L2.L.2P1.2P1",
]
prefix = "DB_calc/computation_funcs_and_files/computation_files/"
file_names = [prefix + tag + ".csv" for tag in tags]

if __name__ == "__main__":
    # compute_DB(["L2.H_s"], file_names)
    calculate_stability_ind_and_a_b()
    # update_orbit_families()
