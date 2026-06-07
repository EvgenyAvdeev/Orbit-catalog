import hashlib

import numpy as np
import orbipy as op
import pandas as pd
from tables import OrbitFamiliesTable

# Параметры интегратора
params = {"rtol": 1e-12, "atol": 1e-12, "nsteps": 100000, "max_step": np.inf}
integrator = op.dopri5_integrator(params=params)

# Создание модели CRTBP для системы Земля-Луна с использованием интегратора
model = op.crtbp3_model("Earth-Moon (default)", integrator=integrator)

# Создание объекта для визуализации орбит
plotter = op.plotter.from_model(model, length_units="Mm")

# Масштабировщик для модели
scaler = op.scaler.from_model(model)

# Создание модели с State Transition Matrix (STM)
stmmodel = op.crtbp3_model("Earth-Moon (default)", stm=True)


def get_ind(data, num):
    """
    Получить индексы равномерно распределенных на кривой начальных условий точек

    Параметры:
    data - массив данных
    num - количество точек

    Возвращает:
    indlist - список индексов равномерно распределенных точек
    """
    indlist = []
    ideal = np.linspace(data.min(), data.max(), num=num)
    for i in range(num):
        indlist.append((abs(data - ideal[i])).idxmin())
    return indlist


def get_stability_complex(orb, threshold=1e-2):
    """
    Определить устойчивость орбиты на основе анализа множителей Флоке, если они хранятся как комплексные значения..

    Параметры:
    orb - DataFrame с данными орбиты
    threshold - пороговое значение для определения устойчивости

    Добавляет в DataFrame колонки 'stability' (устойчивость) и 'unitCirclePairs' (порядок устойчивости).
    """
    # nums - число пар НЕ на единичной окружности
    nums = []
    if "l6" in orb.columns:
        mlt = orb[["l1", "l2", "l3", "l4", "l5", "l6"]]
        fmNum = 6
    else:
        mlt = orb[["l1", "l2", "l3", "l4", "l5"]]
        fmNum = 5

    for i in range(orb.shape[0]):
        num = 0
        for j in range(fmNum):
            if abs(mlt.iloc[i, j]) - 1.0 > threshold:
                num += 1
        nums.append(num)
    nums = np.array(nums)

    stability = np.array(nums == 0, dtype=int)
    orb["stability"] = stability

    # число пар множителей на единичной окружности
    orb["unitCirclePairs"] = 2 - nums


def get_stability(orb, threshold=1e-2):
    """
    Определить устойчивость орбиты на основе анализа множителей Флоке.

    Параметры:
    orb - DataFrame с данными орбиты
    threshold - пороговое значение для определения стабильности

    Добавляет в DataFrame колонки 'stability' (устойчивость) и 'unitCirclePairs' (порядок устойчивости).
    """
    if "l6" in orb.columns:
        mlt = orb[
            [
                "l1_r",
                "l2_r",
                "l3_r",
                "l4_r",
                "l5_r",
                "l6_r",
                "l1_im",
                "l2_im",
                "l3_im",
                "l4_im",
                "l5_im",
                "l6_im",
            ]
        ]
        numFM = 6
    else:
        mlt = orb[
            [
                "l1_r",
                "l2_r",
                "l3_r",
                "l4_r",
                "l5_r",
                "l1_im",
                "l2_im",
                "l3_im",
                "l4_im",
                "l5_im",
            ]
        ]
        numFM = 5

    # nums - число пар НЕ на единичной окружности
    nums = []
    for i in range(orb.shape[0]):
        num = 0
        for j in range(numFM):
            if abs(mlt.iloc[i, j] + mlt.iloc[i, numFM + j] * 1j) - 1.0 > threshold:
                num += 1
        nums.append(num)

    nums = np.array(nums)
    stability = np.array(nums == 0, dtype=int)
    orb["stability"] = stability

    # число пар множителей на единичной окружности
    orb["unitCirclePairs"] = 2 - nums


def get_cj(orb):
    """
    Рассчитать константу Якоби для каждой орбиты.

    Параметры:
    orb - DataFrame с данными орбит

    Добавляет в DataFrame колонку 'cj'.
    """
    cjs = []
    for i in range(orb.shape[0]):
        y = model.get_zero_state()
        y[[0, 2, 4]] = np.real(orb.iloc[i, :3])
        cj = model.jacobi(y)
        cjs.append(cj)
    orb["cj"] = cjs


def get_cj_and_periods(orb, nCr):
    """
    Рассчитать константу Якоби и периоды орбит

    Параметры:
    orb - DataFrame с данными орбиты
    nCr - количество пересечений с плоскостью y=0 орбит из рассчитываемого семейства

    Добавляет в DataFrame колонки 't' (период) и 'cj'(константа Якоби).
    """
    det = op.event_detector(model, events=[op.eventY(count=nCr)])

    periods = []
    cjs = []
    for i in range(orb.shape[0]):
        y = model.get_zero_state()
        y[[0, 2, 4]] = np.real(orb.iloc[i, :3])
        _, evout = det.prop(y, 0.0, 20.0 * np.pi, ret_df=False, last_state="last")
        t = scaler(evout[-1, 3], "nd-d")
        cj = model.jacobi(y)
        periods.append(t)
        cjs.append(cj)

    orb["t"] = periods
    orb["cj"] = cjs


def df2complex(data):
    """
    Преобразование колонок множителей Флоке из вещественных чисел в комплексные числа.

    Параметры:
    ----------
    data : pandas.DataFrame
        Данные орбиты с колонками множителей Флоке.
    """
    if "l6" in data.columns:
        fmNum = 6
    else:
        fmNum = 5
    for i in range(fmNum):
        # Преобразование каждой компоненты множителя Флоэда в комплексное число
        data[f"l{i + 1}"] = data[f"l{i + 1}"].apply(lambda x: complex(x))


def trajectory2SI(orb):
    """
    Преобразование траектории из безразмерных единиц (DU) в системы единиц SI.

    Параметры:
    ----------
    orb : pandas.DataFrame
        Траектория орбиты в безразмерных единицах.

    Возвращает:
    ----------
    pandas.DataFrame
        Траектория орбиты в системах единиц SI.
    """
    # Масштабирование координат из DU в километры
    orb.x = scaler(orb.x, "nd-km")
    orb.y = scaler(orb.y, "nd-km")
    orb.z = scaler(orb.z, "nd-km")

    # Масштабирование скоростей из DU/DU-км/с в км/с
    orb.vx = scaler(orb.vx, "nd/nd-km/s")
    orb.vy = scaler(orb.vy, "nd/nd-km/s")
    orb.vz = scaler(orb.vz, "nd/nd-km/s")

    # Масштабирование времени из DU-дней в дни
    orb.t = scaler(orb.t, "nd-d")
    return orb


def generate_one_trajectory(s, t):
    """
    Генерация одной траектории орбиты на заданный период.

    Параметры:
    ----------
    s : numpy.ndarray
        Начальное состояние орбиты в безразмерных единицах.
    t : float
        Полный период орбиты в безразмерных единицах.

    Возвращает:
    ----------
    pandas.DataFrame
        Траектория орбиты в системах единиц SI.
    """
    # Интегрирование орбиты вперед на половину периода
    arr1 = model.prop(s, 0, t / 2)
    # Интегрирование орбиты назад на половину периода
    arr2 = model.prop(s, 0, -t / 2)
    # Корректировка времени для обратной траектории
    arr2.t = arr1.t.iloc[-1] - arr2.t
    # Объединение двух траекторий в одну
    arr = pd.concat([arr1, arr2[::-1]]).reset_index(drop=True)
    return trajectory2SI(arr)


def compute_properties(
    orb_dataframe: pd.DataFrame,
    fam_name: str,
    family_id: int,
    hash: pd.Series,
    saveFiles=False,
    planarLyapunov=False,
    index_start=1,
    request=False,
    sym=1,
) -> pd.DataFrame:
    """
    Вычисление и форматирование свойств орбит

    Форматирует колонки в следующем порядке:
    + family_id (int),
    + unique_id (str)
    + x (км), y (км), z (км), vx (км/с), vy (км/с), vz (км/с), t (дни),
    + floke_1_r, floke_2_r, floke_3_r, floke_4_r, floke_5_r, floke_6_r,
    + floke_1_im, floke_2_im, floke_3_im, floke_4_im, floke_5_im, floke_6_im,
    + ax (км), ay (км), az (км),
    + dist_primary (км), dist_secondary (км),
    + cj (float),
    + stable (bool),
    + stability_ind_1 (float),
    + stability_ind_2 (float),
    + stability_ind_3 (float),
    + alpha (float),
    + beta (float)

    Параметры:
    ----------
    orb_dataframe : pandas.DataFrame
        Данные орбиты с безразмерными состояниями и периодом в днях
    fam_name : str
        Тег семейства орбит в формате "lib_point.family_tag"
    family_id : int
        Идентификатор семейства орбит в базе данных
    hash : pd.Series
        Уникальный хеш-идентификатор орбиты для предотвращения дублирования
    saveFiles : bool, optional
        Если True, сохраняет промежуточные файлы в формате CSV
        По умолчанию False.
    planarLyapunov : bool, optional
        True, если идёт расчет горизонтальных орбит Ляпунова
        По умолчанию False.
    index_start : int, optional
        Начальный индекс для идентификации орбит при сохранении файлов
        По умолчанию 1.
    request : bool, optional
        Если True, подготавливает данные для отправки как запрос API
        По умолчанию False.
    sym : int, optional
        Коэффициент симметрии орбиты. По умолчанию 1

    Возвращает:
    ----------
    pandas.DataFrame
        Форматированные данные орбиты
    """
    orb = orb_dataframe.copy()
    orbColumns = orb.columns

    # Обработка множителей Флоке
    if "l6_r" not in orbColumns:
        if "l5_r" in orbColumns:
            # Добавление столбцов l6_r и l6_im со значениями по умолчанию
            orb["l6_r"] = [1] * orb.shape[0]
            orb["l6_im"] = [0] * orb.shape[0]
        elif "l1" in orbColumns:
            if "l6" not in orbColumns:
                orb["l6"] = [1 + 0j] * orb.shape[0]

            # Создание DataFrame для вещественных частей множителей Флоэда
            lr = pd.DataFrame(
                list(
                    [
                        np.real(orb.l1.astype(np.complex128)),
                        np.real(orb.l2.astype(np.complex128)),
                        np.real(orb.l3.astype(np.complex128)),
                        np.real(orb.l4.astype(np.complex128)),
                        np.real(orb.l5.astype(np.complex128)),
                        np.real(orb.l6.astype(np.complex128)),
                    ]
                ),
                index=["l1_r", "l2_r", "l3_r", "l4_r", "l5_r", "l6_r"],
            ).T
            # Создание DataFrame для мнимых частей множителей Флоэда
            lim = pd.DataFrame(
                list(
                    [
                        np.imag(orb.l1.astype(np.complex128)),
                        np.imag(orb.l2.astype(np.complex128)),
                        np.imag(orb.l3.astype(np.complex128)),
                        np.imag(orb.l4.astype(np.complex128)),
                        np.imag(orb.l5.astype(np.complex128)),
                        np.imag(orb.l6.astype(np.complex128)),
                    ]
                ),
                index=["l1_im", "l2_im", "l3_im", "l4_im", "l5_im", "l6_im"],
            ).T
            # Объединение исходного DataFrame с новыми столбцами
            orb = pd.concat([orb, lr, lim], axis=1)

    # Проверка наличия информации о стабильности
    if "unitCirclePairs" not in orbColumns:
        get_stability(orb)

        # Расчет свойств орбит
    ax = []
    ay = []
    az = []
    distPrim = []
    distSec = []
    stable = []
    stabilityOrder = []
    arr_all = []
    coordinates = []
    unique_id = []
    if "CJ" in orbColumns:
        orb = orb.rename(columns={"CJ": "cj"})
    if "T" in orbColumns:
        orb = orb.rename(columns={"T": "t"})

    cjNotIn = "cj" not in orbColumns
    if cjNotIn:
        cj = []

    for i in range(orb.shape[0]):
        # Получение начального состояния орбиты
        s = model.get_zero_state()
        s[[0, 2, 4]] = np.real(orb.iloc[i][["x", "z", "v"]])
        # Масштабирование периода
        t = np.real(scaler(orb.iloc[i]["t"], "d-nd"))
        # Генерация траектории орбиты
        arr = generate_one_trajectory(s, t)
        if saveFiles:
            # Сохранение траектории в формате JSON
            arr_all.append(arr.to_json(orient="records"))
            # Сохранение координат начальной точки траектории
            coordinates.append(arr.iloc[0, 1:])
        #         plotter.plot_proj(arr)

        # Вычисление разницы максимумов и минимумов координат для определения размеров орбиты
        ax.append(arr.x.max() - arr.x.min())
        ay.append(arr.y.max() - arr.y.min())
        az.append(arr.z.max() - arr.z.min())

        # Вычисление минимальных расстояний до первичной и вторичной точек
        distPrim.append(
            min(
                np.linalg.norm(
                    arr.iloc[:, 1:4] - [-scaler(model.mu, "nd-km"), 0, 0], axis=1
                )
            )
        )
        distSec.append(
            min(
                np.linalg.norm(
                    arr.iloc[:, 1:4] - [scaler(model.mu1, "nd-km"), 0, 0], axis=1
                )
            )
        )

        if cjNotIn:
            # Вычисление постоянной Жакоби
            cj.append(model.jacobi(s))
        # Определение стабильности орбиты
        unit_circle_pairs = orb.unitCirclePairs.reset_index(drop=True)
        stable.append(True if unit_circle_pairs[i] == 2 else False)
        stabilityOrder.append(unit_circle_pairs[i])

    if planarLyapunov:
        orb["alpha"] = [0] * orb.shape[0]

    # Добавление рассчитанных свойств в DataFrame
    orb["ax"] = ax
    orb["ay"] = ay
    orb["az"] = az
    orb["dist_primary"] = distPrim
    orb["dist_secondary"] = distSec
    # Масштабирование координат и скоростей в системе единиц SI
    orb.x = scaler(orb.x, "nd-km")
    orb.z = scaler(orb.z, "nd-km")
    orb.v = scaler(orb.v, "nd/nd-km/s")

    if cjNotIn:
        # Добавление колонки 'cj' в DataFrame
        orb["cj"] = cj

    orb["stable"] = stable
    orb["stability_order"] = stabilityOrder
    orb["t_period"] = orb["t"]

    if sym == 1:
        orb["y"] = [0] * orb.shape[0]
        orb["vx"] = [0] * orb.shape[0]
        orb["vz"] = [0] * orb.shape[0]

    orb["vy"] = orb["v"]
    orb = orb.drop(columns=["v"])
    orb["stability_ind_1"] = [0] * orb.shape[0]
    orb["stability_ind_2"] = [0] * orb.shape[0]
    orb["stability_ind_3"] = [0] * orb.shape[0]
    orb["abs_v"] = np.sqrt(orb["vx"] ** 2 + orb["vy"] ** 2 + orb["vz"] ** 2)
    orb["alpha"] = [0] * orb.shape[0]
    orb["beta"] = [0] * orb.shape[0]
    orb["family_id"] = family_id
    orb["unique_id"] = hash

    column_mapping = {
        "l1_r": "floke_1_r",
        "l2_r": "floke_2_r",
        "l3_r": "floke_3_r",
        "l4_r": "floke_4_r",
        "l5_r": "floke_5_r",
        "l6_r": "floke_6_r",
        "l1_im": "floke_1_im",
        "l2_im": "floke_2_im",
        "l3_im": "floke_3_im",
        "l4_im": "floke_4_im",
        "l5_im": "floke_5_im",
        "l6_im": "floke_6_im",
    }
    # old_columns_present = [col for col in column_mapping.keys() if col in orbColumns]
    # new_columns_present = [col for col in column_mapping.values() if col in orbColumns]
    #
    # if old_columns_present and not new_columns_present:
    orb = orb.rename(columns=column_mapping)

    if request:
        # Выбор определенных колонок для запроса
        orb = orb[
            [
                "family_id",
                "unique_id",
                "x",
                "y",
                "z",
                "vx",
                "vy",
                "vz",
                "abs_v",
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
        ]
    else:
        # Добавление идентификаторов орбит
        orb["id"] = pd.DataFrame(range(index_start, index_start + orb.shape[0]))

        # Выбор определенных колонок для базы данных
        orb = orb[
            [
                "id",
                "family_id",
                "unique_id",
                "x",
                "y",
                "z",
                "vx",
                "vy",
                "vz",
                "abs_v",
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
        ]

    if saveFiles:
        # Сохранение данных орбиты в CSV файл
        file_name = f"formatted files/orbits/{fam_name}.csv"
        orb.to_csv(file_name, index=False)
    return orb


def compute_trajectories(
    orb: pd.DataFrame,
    fam_name: str,
    orbit_id: int,
    saveFiles=False,
    index_start=0,
    request=False,
) -> pd.DataFrame:
    """
    Вычисление траекторий орбиты и их сохранение

    Параметры:
    ----------
    orb : pandas.DataFrame
        Данные орбиты с безразмерными состояниями и периодом в днях
    fam_name : str
        Тег семейства орбит
    orbit_id: int
        Индификатор орбиты
    saveFiles : bool, optional
        Если True, сохраняет траектории в формате CSV
    index_start : int, optional
        Начальный индекс для идентификации орбит
    request : bool, optional
        Если True, подготавливает данные для запроса
    Возвращает:
    ----------
    pandas.DataFrame
        Данные траекторий орбиты
    """
    all_trajectories = []
    if "CJ" in orb.columns:
        orb = orb.rename(columns={"CJ": "cj"})
    if "T" in orb.columns:
        orb = orb.rename(columns={"T": "t"})
    for i in range(orb.shape[0]):
        # Получение начального состояния орбиты
        s = model.get_zero_state()
        s[[0, 2, 4]] = np.real(orb.iloc[i][["x", "z", "v"]])
        # Масштабирование периода
        t = np.real(scaler(orb.iloc[i]["t"], "d-nd"))
        # Генерация траектории орбиты
        trajectory = generate_one_trajectory(s, t)

        # Добавляем идентификатор орбиты к каждой точке траектории
        trajectory["orbit_id"] = index_start + i + orbit_id
        all_trajectories.append(trajectory)

    # Объединяем все траектории в один DataFrame
    result_df = pd.concat(all_trajectories).reset_index(drop=True)
    result_df["abs_v"] = np.sqrt(
        result_df["vx"] ** 2 + result_df["vy"] ** 2 + result_df["vz"] ** 2
    )
    if request:
        result_df = result_df[
            ["orbit_id", "x", "y", "z", "vx", "vy", "vz", "abs_v", "t"]
        ]
    else:
        result_df["id"] = pd.DataFrame(
            range(index_start, index_start + result_df.shape[0])
        )
        result_df = result_df[
            ["id", "orbit_id", "x", "y", "z", "vx", "vy", "vz", "abs_v", "t"]
        ]
    if saveFiles:
        # Сохранение траекторий орбит в CSV файл
        file_name = f"formatted files/trajectory_points/{fam_name}_trajectories.csv"
        result_df.to_csv(file_name, index=False)

    return result_df


def compute_poincare_sections(
    orb: pd.DataFrame,
    fam_name: str,
    orbit_id: int,
    saveFiles=False,
    index_start=0,
    request=False,
) -> pd.DataFrame:
    """
    Вычисление сечений Пуанкаре для орбиты и их сохранение

    Параметры:
    ----------
    orb : pandas.DataFrame
        Данные орбиты с безразмерными состояниями и периодом в днях
    fam_name : str
        Тег семейства орбит
    orbit_id: int
        Индификатор орбиты
    saveFiles : bool, optional
        Если True, сохраняет сечения Пуанкаре в формате CSV
    index_start : int, optional
        Начальный индекс для идентификации орбит
    request : bool, optional
        Если True, подготавливает данные для запроса
    Возвращает:
    ----------
    pandas.DataFrame
        Данные сечений Пуанкаре орбиты
    """
    # Создание детектора событий для различных плоскостей
    det = op.event_detector(
        model,
        events=[
            op.eventX(terminal=False),
            op.eventY(terminal=False),
            op.eventZ(terminal=False),
            op.eventVX(terminal=False),
            op.eventVY(terminal=False),
            op.eventVZ(terminal=False),
        ],
    )

    # Определение названий плоскостей сечений
    planes = ["x = 0", "y = 0", "z = 0", "vx = 0", "vy = 0", "vz = 0"]
    all_sections = []
    if "CJ" in orb.columns:
        orb = orb.rename(columns={"CJ": "cj"})
    if "T" in orb.columns:
        orb = orb.rename(columns={"T": "t"})
    for i in range(orb.shape[0]):
        # Получение начального состояния орбиты
        s = model.get_zero_state()
        s[[0, 2, 4]] = orb[["x", "z", "v"]].iloc[i]
        # Масштабирование периода
        period = scaler(orb["t"].iloc[i], "d-nd")
        # Интегрирование орбиты на заданный период
        _, ev = det.prop(s, 0, period + 1e-10)

        # Масштабирование результатов интегрирования
        ev["t"] = scaler(ev["t"], "nd-d")
        ev["x"] = scaler(ev["x"], "nd-km")
        ev["y"] = scaler(ev["y"], "nd-km")
        ev["z"] = scaler(ev["z"], "nd-km")
        ev["vx"] = scaler(ev["vx"], "nd/nd-km/s")
        ev["vy"] = scaler(ev["vy"], "nd/nd-km/s")
        ev["vz"] = scaler(ev["vz"], "nd/nd-km/s")

        # Поиск точек пересечения орбиты с плоскостями
        for j in range(6):
            section = ev[ev.e == j].copy()
            if len(section) > 0:
                # Обнуление соответствующей координаты при пересечении
                section.iloc[:, j + 1] = 0
                section["plane"] = planes[j]
                # print(f"ORBIT ID IN SECTION: {i + index_start + orbit_id}")
                section["orbit_id"] = i + index_start + orbit_id

                # Выбираем только нужные столбцы
                section = section[
                    ["orbit_id", "plane", "x", "y", "z", "vx", "vy", "vz", "t"]
                ]
                all_sections.append(section)

    # Объединение всех сечений в один DataFrame
    if all_sections:
        result_df = pd.concat(all_sections).reset_index(drop=True)
    else:
        # Если нет ни одного сечения, возвращаем пустой DataFrame с правильными колонками
        result_df = pd.DataFrame(
            columns=["orbit_id", "plane", "x", "y", "z", "vx", "vy", "vz", "abs_v", "t"]
        )

    result_df["abs_v"] = np.sqrt(
        result_df["vx"] ** 2 + result_df["vy"] ** 2 + result_df["vz"] ** 2
    )
    if request:
        result_df = result_df[
            ["orbit_id", "plane", "x", "y", "z", "vx", "vy", "vz", "abs_v", "t"]
        ]
    else:
        result_df["id"] = pd.DataFrame(
            range(index_start, index_start + result_df.shape[0])
        )
        result_df = result_df[
            ["id", "orbit_id", "plane", "x", "y", "z", "vx", "vy", "vz", "abs_v", "t"]
        ]

    if saveFiles:
        # Сохранение сечений Пуанкаре в CSV файл
        file_name = (
            f"formatted files/poincare_sections/{fam_name}_poincare_sections.csv"
        )
        result_df.to_csv(file_name, index=False)

    return result_df


def create_orbit_families_step_1(tags: list[str], index_start=1) -> pd.DataFrame:
    """
    Создание семейств орбит

    Параметры:
    ----------
    tags : list
        Список тегов семейств орбит
    index_start : int, optional
        Начальный индекс для идентификации семейств орбит
    Возвращает:
    ----------
    pd.DataFrame
        Данные с тегами и идентификаторами семейств орбит
    """
    points = []
    family_tags = []
    for tag in tags:
        points.append(tag[:2])
        family_tags.append(tag[3:])
    # Создание словаря с тегами семейств орбит
    data_dict = {"lib_point": points, "family_tag": family_tags}

    # Создание списка пустых значений для всех тегов
    void_cols = [0] * len(tags)
    skip_cols = ["lib_point", "family_tag", "id"]
    # Заполнение словаря пустыми значениями для всех колонок, кроме "tag" и "id"
    for column in OrbitFamiliesTable.__table__.columns:
        if column.name not in skip_cols:
            data_dict[column.name] = void_cols
    result_df = pd.DataFrame(data_dict)
    result_df["id"] = pd.DataFrame(range(index_start, index_start + result_df.shape[0]))
    result_df = result_df[[col.name for col in OrbitFamiliesTable.__table__.columns]]
    return result_df
