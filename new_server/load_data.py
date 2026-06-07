import glob
import json
from random import choice
from typing import List, Tuple

import numpy as np
import pandas as pd
from database import db
from DB_calc_and_fill import (
    calc_hashes_batch,
    fill_orbit,
    fill_orbits_family,
    fill_trajectory_points,
    get_fam_by_tag,
    get_first_orbit_id_by_fam_id,
    get_orbit_id_by_fam_id,
    get_orbit_shape,
)
from yandex import *

# ======================== Константы ========================
ORBITS_PATH = "orbits/orbs/"
TRAJ_PATH = "orbits/trajectories/"
SECTIONS_PATH = "orbits/poincare_sections/"

DEFAULT_TAG = "L1.Q"

VOID_COLUMNS = [
    "t",
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
    "ax",
    "ay",
    "az",
    "dist_primary",
    "dist_secondary",
    "cj",
    "stable",
    "stability_ind_1",
    "stability_ind_2",
    "stability_ind_3",
    "alpha",
    "beta",
]


# ======================== Логирование ========================
def log_info(msg: str) -> None:
    print(f"[INFO] {msg}")


def log_error(msg: str) -> None:
    print(f"[ERROR] {msg}")


def log_debug(msg: str) -> None:
    print(f"[DEBUG] {msg}")


# ======================== Функции для работы с файлами ========================
def download_all() -> None:
    log_info("Начинаем скачивание файлов из удалённого хранилища")
    download_families("orbit_families_fixed.csv")
    log_debug("Скачан файл семейств орбит")

    traj_files = list_remote_files(TRAJ_PATH)
    sec_files = list_remote_files(SECTIONS_PATH)

    traj_files = [f for f in traj_files if f.startswith("traj_") and f.endswith(".zip")]
    # Для сечений Пуанкаре: скачиваем secs.zip (или другие ZIP-архивы)
    sec_files = [
        f for f in sec_files if f.endswith(".zip") and ("sec" in f or "poincare" in f)
    ]
    log_info(
        f"Найдено траекторий (архивов): {len(traj_files)}, сечений (архивов): {len(sec_files)}"
    )

    for traj in traj_files:
        download_from_trajectories(traj)
        log_debug(f"Скачан и распакован архив траекторий: {traj}")

    for sec in sec_files:
        download_from_poincare_sections(sec)
        log_debug(f"Скачан и распакован архив сечений Пуанкаре: {sec}")

    log_info("Скачивание завершено")


# ======================== Функции для подготовки данных ========================
def create_default_family() -> pd.DataFrame:
    log_info("Создаём DataFrame для семейства L1.Q")
    columns = [
        "lib_point",
        "family_tag",
        "min_x",
        "min_y",
        "min_z",
        "max_x",
        "max_y",
        "max_z",
        "min_vx",
        "max_vx",
        "min_vy",
        "max_vy",
        "min_vz",
        "max_vz",
        "min_abs_v",
        "max_abs_v",
        "min_t",
        "max_t",
        "min_cj",
        "max_cj",
        "min_ax",
        "max_ax",
        "min_ay",
        "max_ay",
        "min_az",
        "max_az",
        "min_dist_primary",
        "max_dist_primary",
        "min_dist_secondary",
        "max_dist_secondary",
        "min_stability_ind_1",
        "max_stability_ind_1",
        "min_stability_ind_2",
        "max_stability_ind_2",
        "min_stability_ind_3",
        "max_stability_ind_3",
        "min_alpha",
        "max_alpha",
        "min_beta",
        "max_beta",
    ]
    family = pd.DataFrame(columns=columns)

    new_row = {col: 0.0 for col in columns}
    new_row["lib_point"] = "L1"
    new_row["family_tag"] = "Q"
    family = pd.concat([family, pd.DataFrame([new_row])], ignore_index=True)
    log_debug(f"Создано семейство с {len(family)} записью")
    return family


def get_orbit_and_trajectory(csv_file: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    log_info(f"Загружаем файл: {csv_file}")
    orb_parts = []
    trajectory_parts = []

    traj_raw = pd.read_csv(csv_file)
    orb_parts.append(traj_raw[["orbit_id", "x", "y", "z", "vx", "vy", "vz"]])

    for _, row in traj_raw.iterrows():
        orbit_id = row["orbit_id"]
        points = json.loads(row["v"])
        for point in points:
            point["orbit_id"] = orbit_id
            trajectory_parts.append(point)

    orb = pd.concat(orb_parts, ignore_index=True)
    trajectory = pd.DataFrame(trajectory_parts)
    trajectory = trajectory[["orbit_id", "t", "x", "y", "z", "vx", "vy", "vz"]]

    log_info(
        f"Загружено орбит (уникальных состояний): {len(orb)}, точек траектории: {len(trajectory)}"
    )
    return orb, trajectory


def prepare_orb_dataframe(orb: pd.DataFrame, family_id: int) -> pd.DataFrame:
    log_debug(
        f"Подготовка DataFrame орбит: добавление family_id={family_id}, хэшей, abs_v и пустых колонок"
    )
    orb = orb.copy()
    orb["family_id"] = family_id
    orb["unique_id"] = calc_hashes_batch(orb, family_id)
    orb["abs_v"] = np.sqrt(orb["vx"] ** 2 + orb["vy"] ** 2 + orb["vz"] ** 2)

    for col in VOID_COLUMNS:
        orb[col] = 0
    orbit_columns_to_scale = [
        "x",
        "z",
        "ax",
        "ay",
        "az",
        "dist_primary",
        "dist_secondary",
    ]
    orb.loc[:, orbit_columns_to_scale] = orb[orbit_columns_to_scale] / 10**3
    log_debug(f"Подготовлено {len(orb)} строк орбит")
    return orb


def get_family_id_by_tag(tag: str, session) -> int:
    log_info(f"Получаем ID семейства по тегу {tag}")
    family = get_fam_by_tag(tag, session)
    lib_point, family_tag = tag[:2], tag[3:]
    family_id = int(
        family.loc[
            (family.family_tag == family_tag) & (family.lib_point == lib_point), "id"
        ].values[0]
    )
    log_debug(f"Найден family_id = {family_id}")
    return family_id


def insert_orbits_one_by_one(orb_df: pd.DataFrame, session) -> None:
    log_info(f"Вставка {len(orb_df)} орбит в БД (по одной строке)")
    for idx, (_, orbit_row) in enumerate(orb_df.iterrows()):
        orbit_as_df = pd.DataFrame([orbit_row])
        fill_orbit(orbit_as_df, session)
        if (idx + 1) % 100 == 0:
            log_debug(f"Вставлено {idx + 1} орбит")
    log_info("Вставка орбит завершена")


def remap_trajectory_orbit_ids(traj: pd.DataFrame, start_id: int) -> pd.DataFrame:
    log_debug(f"Переиндексация orbit_id в траекториях, начальный ID = {start_id}")
    traj = traj.copy()
    new_ids = []
    shift = 0
    prev_id = traj["orbit_id"][0]

    for i in range(len(traj)):
        if i == 0:
            new_ids.append(start_id)
        elif prev_id < traj["orbit_id"][i]:
            shift += 1
            new_ids.append(start_id + shift)
            prev_id = traj["orbit_id"][i]
        else:
            new_ids.append(start_id + shift)

    traj["orbit_id"] = new_ids
    log_debug(f"Переиндексировано {len(traj)} точек траектории")
    return traj


def save_trajectory_to_db(traj: pd.DataFrame, session) -> None:
    log_info(f"Сохранение {len(traj)} точек траектории в БД")
    try:
        fill_trajectory_points(traj, session)
        session.commit()
        log_info("Траекторные точки успешно загружены для L1.Q")
    except Exception as e:
        log_error(f"Не удалось заполнить точки траектории для L1.Q: {e}")


# ======================== Основной процесс ========================
def process_trajectory_file(
    file_path: str, family_session, all_new_orbit_ids: List
) -> None:
    log_info(f"Начинаем обработку файла: {file_path}")

    # 1. Загрузка данных из файла
    orb, traj = get_orbit_and_trajectory(file_path)

    # 2. Получение ID семейства
    family_id = get_family_id_by_tag(DEFAULT_TAG, family_session)
    family_session.close()
    # 3. Подготовка DataFrame орбит
    orb = prepare_orb_dataframe(orb, family_id)

    # 4. Получение стартового ID для орбит данного семейства
    session = db.create_session()
    try:
        start_orbit_id = get_orbit_id_by_fam_id(family_id, session)
    except Exception:
        start_orbit_id = get_orbit_shape()
    start_orbit_id += 1
    log_debug(f"Стартовый orbit_id для семейства {family_id} = {start_orbit_id}")

    # 5. Вставка орбит
    insert_orbits_one_by_one(orb, session)

    # 6. Переиндексация orbit_id в траекториях
    traj = remap_trajectory_orbit_ids(traj, start_orbit_id)
    all_new_orbit_ids.append(traj["orbit_id"].tolist())

    # 7. Добавление модуля скорости и сохранение траекторий
    traj["abs_v"] = np.sqrt(traj["vx"] ** 2 + traj["vy"] ** 2 + traj["vz"] ** 2)
    trajectory_orbit_columns_to_scale = ["x", "y", "z"]
    traj.loc[:, trajectory_orbit_columns_to_scale] = (
        traj[trajectory_orbit_columns_to_scale] / 10**3
    )
    save_trajectory_to_db(traj, session)

    log_info(f"Файл {file_path} обработан успешно")


if __name__ == "__main__":
    download_all()
    log_info("=== ЗАПУСК СКРИПТА ЗАГРУЗКИ ОРБИТ И ТРАЕКТОРИЙ ===")

    # Сессия для работы с семействами орбит
    family_session = db.create_session()
    log_debug("Сессия для семейств создана")

    # Создаём и сохраняем семейство L1.Q
    family_df = create_default_family()
    fill_orbits_family(family_df, family_session)
    log_info("Семейство L1.Q сохранено в БД")

    # Список для сбора ID орбит (оригиналом не используется, но сохраняем для совместимости)
    all_new_orbit_ids = []

    # Находим все CSV-файлы с траекториями
    all_trajectory_files = glob.glob("loaded/trajectories/traj_*/*.csv")
    log_info(f"Найдено CSV-файлов траекторий: {len(all_trajectory_files)}")

    # Обрабатываем каждый файл
    loaded = []
    for idx, traj_file in enumerate(all_trajectory_files, 1):
        log_info(f"Обработка файла {idx}/{len(all_trajectory_files)}")
        process_trajectory_file(traj_file, family_session, all_new_orbit_ids)
        loaded.append(traj_file)

    log_info(f"=== {loaded} ОБРАБОТАНЫ, РАБОТА ЗАВЕРШЕНА ===")
    # sec_df = pd.read_csv("loaded/poincare_sections/sect_1_new.csv")

    # sec_parts = []
    # for _, row in sec_df.iterrows():
    #         orbit_id = row["orbit_id"]
    #         plane = row["plane"]
    #         points = json.loads(row["v"])
    #         for point in points:
    #             point["orbit_id"] = orbit_id
    #             point["plane"] = plane
    #             sec_parts.append(point)

    # secs = pd.DataFrame(sec_parts)
    # secs = secs[["orbit_id", "plane", "t", "x", "y", "z", "vx", "vy", "vz"]]
    # session = db.create_session()
    # family_id = get_family_id_by_tag(DEFAULT_TAG, session)
    # start_orbit_id = get_orbit_id_by_fam_id(family_id, session)
    # start_value = secs["orbit_id"][0]
    # for _, row in secs.iterrows():
    #     if row["orbit_id"] == start_value:
    #         row["orbit_id"] = start_orbit_id
    #     else:
    #         start_value = row["orbit_id"]
    #         start_orbit_id += 1
    #         row["orbit_id"] = start_orbit_id


# # import glob
# # import json

# # import numpy as np
# # import pandas as pd
# # from database import db
# # from DB_calc_and_fill import (
# #     calc_hashes_batch,
# #     fill_orbit,
# #     fill_orbits_family,
# #     fill_poincare_sections,
# #     fill_trajectory_points,
# #     get_fam_by_tag,
# #     get_orbit_id_by_fam_id,
# # )
# # from yandex import *

# # orbits_path = "orbits/orbs/"
# # traj_path = "orbits/trajectories/"
# # sections_path = "orbits/poincare_sections/"


# # def download_all():
# #     download_families("orbit_families_fixed.csv")
# #     orbits_files = list_remote_files(orbits_path)
# #     traj_files = list_remote_files(traj_path)
# #     sec_files = list_remote_files(sections_path)
# #     traj_files = [traj for traj in traj_files if "traj" in traj]
# #     sec_files = [sec for sec in sec_files if "new" in sec]
# #     for orb in orbits_files:
# #         download_from_orbits(orb)
# #     for traj in traj_files:
# #         download_from_trajectories(traj)
# #     for sec in sec_files:
# #         download_from_poincare_sections(sec)


# # def get_family():
# #     family = pd.DataFrame(
# #         columns=[
# #             "lib_point",
# #             "family_tag",
# #             "min_x",
# #             "min_y",
# #             "min_z",
# #             "max_x",
# #             "max_y",
# #             "max_z",
# #             "min_vx",
# #             "max_vx",
# #             "min_vy",
# #             "max_vy",
# #             "min_vz",
# #             "max_vz",
# #             "min_abs_v",
# #             "max_abs_v",
# #             "min_t",
# #             "max_t",
# #             "min_cj",
# #             "max_cj",
# #             "min_ax",
# #             "max_ax",
# #             "min_ay",
# #             "max_ay",
# #             "min_az",
# #             "max_az",
# #             "min_dist_primary",
# #             "max_dist_primary",
# #             "min_dist_secondary",
# #             "max_dist_secondary",
# #             "min_stability_ind_1",
# #             "max_stability_ind_1",
# #             "min_stability_ind_2",
# #             "max_stability_ind_2",
# #             "min_stability_ind_3",
# #             "max_stability_ind_3",
# #             "min_alpha",
# #             "max_alpha",
# #             "min_beta",
# #             "max_beta",
# #         ]
# #     )
# #     all_columns = family.columns.tolist()

# #     new_row = {col: 0.0 for col in all_columns}
# #     new_row["lib_point"] = "L1"
# #     new_row["family_tag"] = "Q"

# #     family = pd.concat([family, pd.DataFrame([new_row])], ignore_index=True)
# #     return family


# # def get_orb_traj(filename: str):
# #     orb_parts = []
# #     trajectory_parts = []

# #     traj = pd.read_csv(filename)

# #     orb_parts.append(traj[["orbit_id", "x", "y", "z", "vx", "vy", "vz"]])

# #     for idx, row in traj.iterrows():
# #         orbit_id = row["orbit_id"]
# #         points = json.loads(row["v"])

# #         for point in points:
# #             point["orbit_id"] = orbit_id
# #             trajectory_parts.append(point)

# #     orb = pd.concat(orb_parts, ignore_index=True)
# #     trajectory = pd.DataFrame(trajectory_parts)
# #     trajectory = trajectory[["orbit_id", "t", "x", "y", "z", "vx", "vy", "vz"]]
# #     print(f"LEN: {len(trajectory)}")
# #     return orb, trajectory


# # if __name__ == "__main__":
# #     session_fam = db.create_session()
# #     fam = get_family()
# #     fill_orbits_family(fam, session_fam)
# #     all_trajs = glob.glob("loaded/trajectories/*.csv")
# #     all_new_orbit_ids = []
# #     tag = "L1.Q"
# #     family = get_fam_by_tag(tag, session_fam)
# #     for traj_file in all_trajs:
# #         tmp_session = db.create_session()
# #         orb, traj = get_orb_traj(traj_file)
# #         orbit_families_df = get_fam_by_tag(tag, tmp_session)
# #         tmp_session.close()
# #         family_id = int(
# #             orbit_families_df.loc[
# #                 (orbit_families_df.family_tag == tag[3:])
# #                 & (orbit_families_df.lib_point == tag[:2]),
# #                 "id",
# #             ].values[0]
# #         )
# #         orb["family_id"] = family_id
# #         hashes = calc_hashes_batch(orb, family_id)
# #         orb["unique_id"] = hashes
# #         orb["abs_v"] = np.sqrt(orb["vx"] ** 2 + orb["vy"] ** 2 + orb["vz"] ** 2)
# #         void_columns = [
# #             "t",
# #             "floke_1_r",
# #             "floke_2_r",
# #             "floke_3_r",
# #             "floke_4_r",
# #             "floke_5_r",
# #             "floke_6_r",
# #             "floke_1_im",
# #             "floke_2_im",
# #             "floke_3_im",
# #             "floke_4_im",
# #             "floke_5_im",
# #             "floke_6_im",
# #             "ax",
# #             "ay",
# #             "az",
# #             "dist_primary",
# #             "dist_secondary",
# #             "cj",
# #             "stable",
# #             "stability_ind_1",
# #             "stability_ind_2",
# #             "stability_ind_3",
# #             "alpha",
# #             "beta",
# #         ]
# #         for col in void_columns:
# #             orb[col] = [0] * orb.shape[0]
# #         session = db.create_session()
# #         print(f"FAMILY_ID: {family_id}")
# #         id_start = get_orbit_id_by_fam_id(family_id, session)
# #         for ind, orbit in orb.iterrows():
# #             orbit = pd.DataFrame([orbit])
# #             print(f"ORBIT: {id_start + ind}")
# #             fill_orbit(orbit, session)
# #         ids_for_traj = []
# #         shift = 0
# #         start_value = traj["orbit_id"][0]

# #         for i in range(len(traj)):
# #             if i == 0:
# #                 ids_for_traj.append(id_start)
# #                 continue

# #             if start_value < traj["orbit_id"][i]:
# #                 shift += 1
# #                 ids_for_traj.append(id_start + shift)
# #                 start_value = traj["orbit_id"][i]
# #             else:
# #                 ids_for_traj.append(id_start + shift)

# #         traj["orbit_id"] = ids_for_traj
# #         all_new_orbit_ids.append(ids_for_traj)
# #         traj["abs_v"] = np.sqrt(traj["vx"] ** 2 + traj["vy"] ** 2 + traj["vz"] ** 2)

# #         try:
# #             fill_trajectory_points(traj, session)
# #             session.commit()
# #             print(f"INFO: LOADING COMPLETED trajectory points for L1.Q")

# #         except Exception as e:
# #             print(f"ERROR: Failed to fill trajectory points for for L1.Q: {e}")

# # try:
# #     fill_poincare_sections(sections_df, session)

# #         session.rollback()
# #         delete_section(sections_df, session)
# #         delete_orbit(orbit_df.iloc[0]["id"], session)
# #         failed_orbits.append(orbit_id)

# # except Exception as e:
# #     print(f"ERROR: Failed to fill poincare sections for orbit {orbit_id}: {e}")
# #     session.rollback()
# #     delete_orbit(orbit_df.iloc[0]["id"], session)
# #     failed_orbits.append(orbit_id)
