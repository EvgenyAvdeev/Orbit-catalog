import logging
import time

import pandas as pd
import typer
from create_tables import main
from DB_calc_and_fill import (
    calculate_stability_ind_and_a_b,
    compute_DB,
    db,
    prefix,
    update_orbit_families,
)
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
from repo import CRUDRepo
from rich import box
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table
from tables import (
    OrbitFamiliesTable,
    OrbitsTable,
    PoincareSectionsTable,
    TrajectoryPointsTable,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("rich")


class RepoUnit:
    def __init__(self, family_repo, orbit_repo, trajectory_repo, poincare_repo):
        self.family_repo = family_repo
        self.orbit_repo = orbit_repo
        self.trajectory_repo = trajectory_repo
        self.poincare_repo = poincare_repo


repo_unit = RepoUnit(
    family_repo=CRUDRepo[
        OrbitFamiliesTable,
        OrbitFamilyModel,
        CreateOrbitFamilyModel,
        UpdateOrbitFamilyModel,
    ](
        OrbitFamiliesTable,
        OrbitFamilyModel,
        CreateOrbitFamilyModel,
        UpdateOrbitFamilyModel,
    ),
    orbit_repo=CRUDRepo[OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel](
        OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel
    ),
    trajectory_repo=CRUDRepo[
        TrajectoryPointsTable,
        TrajectoryPointModel,
        CreateTrajectoryPointModel,
        UpdateTrajectoryPointModel,
    ](
        TrajectoryPointsTable,
        TrajectoryPointModel,
        CreateTrajectoryPointModel,
        UpdateTrajectoryPointModel,
    ),
    poincare_repo=CRUDRepo[
        PoincareSectionsTable,
        PoincareSectionModel,
        CreatePoincareSectionModel,
        UpdatePoincareSectionModel,
    ](
        PoincareSectionsTable,
        PoincareSectionModel,
        CreatePoincareSectionModel,
        UpdatePoincareSectionModel,
    ),
)

app = typer.Typer()

TAGS = [
    "L1.H_s",
    "L1.H_n",
    "L2.H_s",
    "L2.H_n",
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
    "L1.L.2P1.2P1",
    "L2.L.2P1.2P1",
    "L1.H_n.2P2",
    "L1.H_n.3P1",
    "L1.H_n.3P2",
    "L1.H_n.3P3",
    "L1.H_n.4P1",
    "L1.H_s.2P1",
    "L1.H_s.2P3",
    "L1.H_s.3P1",
    "L1.H_s.3P2",
    "L1.H_s.3P3",
    "L1.H_s.4P1",
    "L1.Planar.2P1.2P1",
    "L1.Planar.2P1.3P1",
    "L1.Planar.2P1.3P2",
    "L2.H_n.2P2",
    "L2.H_n.3P1",
    "L2.H_s.2P1",
    "L2.H_s.3P1",
    "L2.Planar.2P1.2P1",
    "L2.Planar.2P1.3P1",
    "L2.Planar.2P1.3P2",
]


@app.command()
def load_all():
    """
    Интегрирование и загрузка семейства орбит по всем файлам
    """
    for tag in TAGS:
        filename = prefix + tag + ".csv"
        compute_DB([tag], [filename])


@app.command()
def load_family(tag: str):
    """
    Интегрирование и загрузка семейства орбит по тегу
    """
    filename = prefix + tag + ".csv"
    compute_DB([tag], [filename])


@app.command()
def calc_i_a_b():
    """
    Рассчитать индексы устойчивости, параметры альфа и бета у всех орбит находящихся в БД
    """
    calculate_stability_ind_and_a_b()


@app.command()
def fill_min_max_value():
    """
    Пересчитать максимальные и минимальные значения параметров в семействах
    """
    update_orbit_families()


@app.command()
def update_family(tag: str, param_name: str, new_value):
    """
    Обновление параметра семейства орбит по тегу (тэг параметр новое_значение)
    """
    console = Console()

    # Вывод заголовка операции
    console.print(
        Panel.fit(
            f"[bold cyan]ОБНОВЛЕНИЕ СЕМЕЙСТВА ОРБИТ[/bold cyan]", border_style="cyan"
        )
    )

    session = None
    try:
        # Логирование начала операции
        logger.info(
            f"Начало обновления семейства: tag='{tag}', param='{param_name}', new_value='{new_value}'"
        )

        session = db.create_session()
        logger.info("Сессия с базой данных установлена")

        # Парсинг тега
        lib_point = tag[:2]
        family_tag = tag[3:]

        console.print(f"\n[bold]Параметры операции:[/bold]")
        console.print(f"  • Полный тег: [cyan]{tag}[/cyan]")
        console.print(f"  • Точка либрации: [blue]{lib_point}[/blue]")
        console.print(f"  • Тег семейства: [green]{family_tag}[/green]")
        console.print(f"  • Параметр: [yellow]{param_name}[/yellow]")
        console.print(f"  • Новое значение: [magenta]{new_value}[/magenta]")

        # Поиск семейства
        console.print("[cyan]Поиск семейства в базе данных...[/cyan]")

        filter = QueryParamsModel(
            filter_groups=[
                FilterGroup(
                    log_op=LogicalOpEnum.NONE,
                    filters=[
                        FilterModel(field="family_tag", op=Op.lk, value=family_tag),
                        FilterModel(field="lib_point", op=Op.lk, value=lib_point),
                    ],
                )
            ]
        )

        family = repo_unit.family_repo.get_chunk(session, filter)

        if not family:
            logger.error(f"Семейство с тегом '{tag}' не найдено")
            console.print(
                f"\n[bold red]ОШИБКА: Семейство с тегом '{tag}' не найдено в базе данных[/bold red]"
            )
            console.print(
                "[yellow]Проверьте правильность тега и повторите попытку[/yellow]"
            )
            return

        family_record = family[0]
        old_value = getattr(family_record, param_name, "N/A")

        logger.info(
            f"Найдено семейство: ID={family_record.id}, {param_name}={old_value}"
        )

        # Вывод информации о найденном семействе
        console.print(f"\n[bold green]Семейство найдено:[/bold green]")
        console.print(f"  • ID: [cyan]{family_record.id}[/cyan]")
        console.print(
            f"  • Текущее значение {param_name}: [yellow]{old_value}[/yellow]"
        )
        console.print(f"  • Новое значение {param_name}: [green]{new_value}[/green]")

        # Обновление данных
        console.print("[cyan]Обновление данных в базе...[/cyan]")

        update_data = {"id": family_record.id, param_name: new_value}
        update_record = UpdateOrbitFamilyModel(**update_data)
        repo_unit.family_repo.update(update_record, session)

        # Коммит изменений
        session.commit()
        logger.info(f"Данные успешно обновлены в базе")

        # Вывод результата
        console.print(f"\n[bold green]ОБНОВЛЕНИЕ УСПЕШНО ЗАВЕРШЕНО[/bold green]")

        # Создаем таблицу с результатами
        result_table = Table(show_header=False, box=box.SIMPLE, width=60)
        result_table.add_column("Параметр", style="cyan", width=20)
        result_table.add_column("Значение", style="white", width=40)

        result_table.add_row("Семейство", f"{lib_point}.{family_tag}")
        result_table.add_row("ID", f"{family_record.id}")
        result_table.add_row("Измененный параметр", param_name)
        result_table.add_row("Старое значение", str(old_value))
        result_table.add_row("Новое значение", str(new_value))

        console.print(result_table)

        logger.info(f"Обновление семейства {tag} завершено успешно")

    except ValueError as e:
        logger.error(f"Ошибка валидации данных: {str(e)}")
        console.print(f"\n[bold red]ОШИБКА ВАЛИДАЦИИ: {str(e)}[/bold red]")
        console.print(
            "[yellow]Проверьте корректность нового значения параметра[/yellow]"
        )
        if session:
            session.rollback()

    except Exception as e:
        logger.error(f"Ошибка при обновлении семейства: {str(e)}")
        console.print(f"\n[bold red]КРИТИЧЕСКАЯ ОШИБКА: {str(e)}[/bold red]")
        if session:
            session.rollback()
        raise

    finally:
        if session:
            session.close()
            logger.info("Сессия с базой данных закрыта")


@app.command()
def get_families():
    """
    Получение списка всех семейств орбит из базы данных с количеством орбит
    """
    console = Console()

    # Вывод заголовка
    console.print(
        Panel.fit("[bold cyan]СПИСОК СЕМЕЙСТВ ОРБИТ[/bold cyan]", border_style="cyan")
    )

    session = None
    try:
        session = db.create_session()
        logger.info("Сессия с базой данных установлена")

        # Инициализация репозиториев
        logger.info("Инициализация репозиториев...")

        # Репозиторий для семейств
        families_repo = CRUDRepo[
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

        orbits_repo = CRUDRepo[
            OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel
        ](OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel)

        logger.info("Загрузка данных о семействах...")
        families_records = families_repo.get_chunk(session)

        logger.info(f"Загружено {len(families_records)} семейств орбит")

        if not families_records:
            console.print("[yellow]В базе данных не найдено семейств орбит[/yellow]")
            return

        logger.info("Подсчет орбит в семействах...")

        orbit_counts = {}
        for family in families_records:
            orbit_filter = QueryParamsModel(
                filter_groups=[
                    FilterGroup(
                        log_op=LogicalOpEnum.NONE,
                        filters=[
                            FilterModel(field="family_id", op=Op.eq, value=family.id)
                        ],
                    )
                ]
            )

            orbits = orbits_repo.get_chunk(session, orbit_filter)
            orbit_counts[family.id] = len(orbits)

        console.print(
            f"\n[bold green]В базе данных находятся семейства со следующими тегами:[/bold green]"
        )
        console.print("")

        families_table = Table(
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED,
            show_lines=False,
            width=80,
        )

        families_table.add_column("#", style="cyan", width=6, justify="right")
        families_table.add_column("Точка либрации", style="green", width=15)
        families_table.add_column("Тег семейства", style="yellow", width=30)
        families_table.add_column("Орбит", style="blue", width=8, justify="right")
        families_table.add_column("ID", style="dim", width=8, justify="right")

        from collections import defaultdict

        libraries = defaultdict(list)

        for record in families_records:
            libraries[record.lib_point].append(record)

        count = 1
        total_orbits = 0

        for lib_point, lib_records in sorted(libraries.items()):
            lib_total_orbits = sum(orbit_counts[record.id] for record in lib_records)
            total_orbits += lib_total_orbits

            if len(libraries) > 1:
                families_table.add_row(
                    "",
                    f"[bold blue]{lib_point}[/bold blue]",
                    f"[bold blue]{len(lib_records)} семейств[/bold blue]",
                    f"[bold blue]{lib_total_orbits}[/bold blue]",
                    "",
                    style="blue",
                )

            for record in sorted(lib_records, key=lambda x: x.family_tag):
                orbit_count = orbit_counts[record.id]
                # Добавляем цветовое кодирование для количества орбит
                count_style = "green" if orbit_count > 0 else "red"

                families_table.add_row(
                    f"{count}",
                    lib_point,
                    record.family_tag,
                    f"[{count_style}]{orbit_count}[/{count_style}]",
                    f"{record.id}",
                )
                count += 1

        families_table.add_section()
        families_table.add_row(
            "[bold]ВСЕГО[/bold]",
            f"",
            f"[bold]{len(families_records)} семейств[/bold]",
            f"[bold]{total_orbits}[/bold]",
            "",  # Пустая ячейка вместо ID
            style="bold",
        )

        console.print(families_table)

    except Exception as e:
        logger.error(f"Ошибка при получении списка семейств: {str(e)}")
        console.print(f"[bold red]ОШИБКА: {str(e)}[/bold red]")
        raise

    finally:
        if session:
            session.close()
            logger.info("Сессия с базой данных закрыта")


def delete_orbits(ids: list[int]):
    """
    Удаление нескольких орбит и всех связанных данных
    """
    console = Console()

    if not ids:
        console.print("[yellow]Список ID для удаления пуст[/yellow]")
        return

    try:
        session = db.create_session()
        logger.info(f"Начало удаления орбит")
        start_time = time.time()

        # Получаем статистику перед удалением
        console.print("[cyan]Подсчет связанных данных...[/cyan]")

        trajectory_count = repo_unit.trajectory_repo.count_by_condition(
            session, orbit_id=ids
        )
        poincare_count = repo_unit.poincare_repo.count_by_condition(
            session, orbit_id=ids
        )
        orbits_count = repo_unit.orbit_repo.count_by_condition(session, id=ids)

        # Вывод статистики
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Тип данных", style="cyan")
        table.add_column("Количество", justify="right")

        table.add_row("Орбиты для удаления", str(orbits_count))
        table.add_row("Точки траектории", str(trajectory_count))
        table.add_row("Сечения Пуанкаре", str(poincare_count))
        table.add_row(
            "Всего записей", str(trajectory_count + poincare_count + orbits_count)
        )

        console.print(table)

        # Прямое удаление точек траектории по списку orbit_id
        if trajectory_count > 0:
            logger.info(f"Удаление {trajectory_count} точек траектории...")

            deleted_trajectories = repo_unit.trajectory_repo.delete_by_condition(
                session, orbit_id=ids
            )

            logger.info(f"Удалено {deleted_trajectories} точек траектории")

        # Прямое удаление сечений Пуанкаре по списку orbit_id
        if poincare_count > 0:
            logger.info(f"Удаление {poincare_count} сечений Пуанкаре...")

            deleted_poincare = repo_unit.poincare_repo.delete_by_condition(
                session, orbit_id=ids
            )

            logger.info(f"Удалено {deleted_poincare} сечений Пуанкаре")

        # Удаление самих орбит по списку ID
        logger.info(f"Удаление {len(ids)} орбит...")

        orbits_deleted = repo_unit.orbit_repo.delete_by_condition(session, id=ids)

        # Коммит всех изменений
        logger.info("Фиксация изменений в базе данных...")
        session.commit()

        # Вывод итогов
        end_time = time.time()
        execution_time = end_time - start_time

        console.print(f"\n[bold green]УДАЛЕНИЕ ЗАВЕРШЕНО[/bold green]")
        console.print(f"[green]Время выполнения: {execution_time:.2f} сек.[/green]")
        console.print(f"[green]Запрошено к удалению орбит: {len(ids)}[/green]")
        console.print(f"[green]Фактически удалено орбит: {orbits_deleted}[/green]")
        console.print(
            f"[green]Удалено точек траектории: {deleted_trajectories}[/green]"
        )
        console.print(f"[green]Удалено сечений Пуанкаре: {deleted_poincare}[/green]")
        console.print(
            f"[green]Всего удалено записей: {deleted_trajectories + deleted_poincare + orbits_deleted}[/green]"
        )

        # Предупреждение если какие-то орбиты не найдены
        if orbits_deleted < len(ids):
            console.print(
                f"[yellow]Внимание: найдено только {orbits_deleted} из {len(ids)} запрошенных орбит[/yellow]"
            )

        logger.info(f"Удаление орбит завершено за {execution_time:.2f} сек.")

    except Exception as e:
        logger.error(f"Ошибка при удалении орбит {ids}: {str(e)}")
        console.print(f"[bold red]ОШИБКА: {str(e)}[/bold red]")

        if "session" in locals():
            session.rollback()
        raise

    finally:
        if "session" in locals():
            session.close()


@app.command()
def delete_family(tag: str):
    """
    Удаление семейства по его тегу
    """
    session = db.create_session()
    family_filter = QueryParamsModel(
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
    family = repo_unit.family_repo.get_chunk(session, family_filter)
    family_id = family[0].id
    orbit_filter = QueryParamsModel(
        filter_groups=[
            FilterGroup(
                log_op=LogicalOpEnum.NONE,
                filters=[FilterModel(field="family_id", op=Op.eq, value=family_id)],
            )
        ]
    )
    orbits = repo_unit.orbit_repo.get_chunk(session, orbit_filter)
    orbit_ids = [orbit.id for orbit in orbits]
    delete_orbits(orbit_ids)
    repo_unit.family_repo.delete(family_id, session)
    session.close()


@app.command()
def create_tables():
    """
    Создание всех таблиц в БД (удаляет всю БД)
    """
    main()


if __name__ == "__main__":
    app()
