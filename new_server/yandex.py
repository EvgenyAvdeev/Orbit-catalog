import logging
import os
import zipfile

import yadisk
from conf_info import YANDEX_TOKEN

gl_path = os.getcwd() + "/"
y = yadisk.YaDisk(token=YANDEX_TOKEN)
orbits_path = "orbits/orbs/"
traj_path = "orbits/trajectories/"
sections_path = "orbits/poincare_sections/"


def download_families(filename, local_dir=None):
    """
    Скачивает файл с диска

    Args:
        remote_filename: имя файла на диске
        local_filename: локальное имя файла (если None, используется remote_filename)
    """
    if local_dir is None:
        local_dir = os.path.join(gl_path, "loaded/families")
    logging.info(f"DIR = {local_dir}")
    os.makedirs(local_dir, exist_ok=True)
    local_path = os.path.join(local_dir, filename)
    remote_path = f"orbits/orbit_families/{filename}"

    try:
        y.download(remote_path, local_path)
        logging.info(f"[B] скачал {filename} из orbits/ в {local_path}")
        return True
    except Exception as e:
        logging.error(f"[B] Ошибка при скачивании {filename} из orbits: {e}")
        return False


def download_from_orbits(filename, local_dir=None):
    """
    Скачивает файл из каталога orbits/

    Args:
        filename: имя файла для скачивания
        local_dir: локальная директория (если None, то gl_path/orbits)
    """
    if local_dir is None:
        local_dir = os.path.join(gl_path, "loaded/orbits")
    logging.info(f"DIR = {local_dir}")
    os.makedirs(local_dir, exist_ok=True)
    local_path = os.path.join(local_dir, filename)
    remote_path = f"{orbits_path}{filename}"

    try:
        y.download(remote_path, local_path)
        logging.info(f"[B] скачал {filename} из orbits/ в {local_path}")
        return True
    except Exception as e:
        logging.error(f"[B] Ошибка при скачивании {filename} из orbits: {e}")
        return False


def download_and_extract_zip(remote_path, local_extract_dir, filename):
    """
    Скачивает ZIP-архив и распаковывает его

    Args:
        remote_path: путь к ZIP-файлу на Яндекс.Диске
        local_extract_dir: локальная директория для распаковки
        filename: имя файла для скачивания
    """
    # Создаем временный путь для ZIP-файла
    temp_zip_path = os.path.join(local_extract_dir, f"temp_{filename}")
    logging.info("Переход к архивации")
    try:
        # Скачиваем ZIP-файл
        y.download(remote_path, temp_zip_path)
        logging.info(f"[B] скачал архив {filename} в {temp_zip_path}")

        # Распаковываем архив
        with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
            zip_ref.extractall(local_extract_dir)
            logging.info(
                f"[B] распаковал архив {filename} в {local_extract_dir}, файлы: {zip_ref.namelist()}"
            )

        # Удаляем временный ZIP-файл
        os.remove(temp_zip_path)
        logging.info(f"[B] удалил временный архив {temp_zip_path}")

        return True
    except Exception as e:
        logging.error(f"[B] Ошибка при скачивании/распаковке {filename}: {e}")
        # Удаляем временный файл в случае ошибки
        if os.path.exists(temp_zip_path):
            os.remove(temp_zip_path)
        return False


def download_from_trajectories(filename, local_dir=None):
    """
    Скачивает ZIP-архив из каталога trajectories/ и распаковывает его

    Args:
        filename: имя ZIP-архива для скачивания (например, traj_123.zip)
        local_dir: локальная директория для распаковки (если None, то gl_path/loaded/trajectories)
    """
    if local_dir is None:
        local_dir = os.path.join(gl_path, "loaded/trajectories")

    os.makedirs(local_dir, exist_ok=True)
    remote_path = f"{traj_path}{filename}"

    return download_and_extract_zip(remote_path, local_dir, filename)


def download_from_poincare_sections(filename, local_dir=None):
    """
    Скачивает ZIP-архив из каталога poincare_sections/ и распаковывает его

    Args:
        filename: имя ZIP-архива для скачивания (например, secs.zip)
        local_dir: локальная директория для распаковки (если None, то gl_path/loaded/poincare_sections)
    """
    if local_dir is None:
        local_dir = os.path.join(gl_path, "loaded/poincare_sections")

    os.makedirs(local_dir, exist_ok=True)
    remote_path = f"{sections_path}{filename}"

    return download_and_extract_zip(remote_path, local_dir, filename)


def list_remote_files(remote_dir):
    """
    Возвращает список файлов в удаленной директории

    Args:
        remote_dir: путь на Яндекс.Диске (например, "orbs/", "trajectories/")

    Returns:
        list: список имен файлов
    """
    try:
        items = y.listdir(remote_dir)
        return [item["name"] for item in items if item["type"] == "file"]
    except Exception as e:
        logging.error(f"[B] Ошибка при получении списка файлов из {remote_dir}: {e}")
        return []
