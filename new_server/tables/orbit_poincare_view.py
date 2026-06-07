from sqlalchemy import func, join, select
from tables import OrbitFamiliesTable, OrbitsTable, PoincareSectionsTable

from .base import ViewBase

# Создаем запрос представления с агрегацией
poincare_subquery = (
    select(
        PoincareSectionsTable.orbit_id,
        PoincareSectionsTable.plane,
        func.array_agg(PoincareSectionsTable.x).label("x_points"),
        func.array_agg(PoincareSectionsTable.y).label("y_points"),
        func.array_agg(PoincareSectionsTable.z).label("z_points"),
        func.array_agg(PoincareSectionsTable.vx).label("vx_points"),
        func.array_agg(PoincareSectionsTable.vy).label("vy_points"),
        func.array_agg(PoincareSectionsTable.vz).label("vz_points"),
        func.array_agg(PoincareSectionsTable.t).label("t_points"),
        func.count().label("points_count"),
    )
    .group_by(PoincareSectionsTable.orbit_id, PoincareSectionsTable.plane)
    .subquery()
)

view_query = select(
    OrbitsTable.id.label("orbit_id"),
    OrbitsTable.x,
    OrbitsTable.y,
    OrbitsTable.z,
    OrbitsTable.vx,
    OrbitsTable.vy,
    OrbitsTable.vz,
    OrbitsTable.abs_v,
    OrbitsTable.ax,
    OrbitsTable.ay,
    OrbitsTable.az,
    OrbitsTable.t,
    OrbitsTable.cj,
    OrbitsTable.dist_primary,
    OrbitsTable.dist_secondary,
    OrbitFamiliesTable.lib_point,
    OrbitFamiliesTable.family_tag,
    poincare_subquery.c.plane,
    poincare_subquery.c.x_points,
    poincare_subquery.c.y_points,
    poincare_subquery.c.z_points,
    poincare_subquery.c.vx_points,
    poincare_subquery.c.vy_points,
    poincare_subquery.c.vz_points,
    poincare_subquery.c.t_points,
    poincare_subquery.c.points_count,
).select_from(
    join(
        OrbitsTable, OrbitFamiliesTable, OrbitsTable.family_id == OrbitFamiliesTable.id
    ).join(poincare_subquery, poincare_subquery.c.orbit_id == OrbitsTable.id)
)


class OrbitPoincareViewTable(ViewBase):
    __table__ = view_query.cte("orbit_poincare_view")
