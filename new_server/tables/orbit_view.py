from sqlalchemy import select, join
from tables import OrbitsTable,  OrbitFamiliesTable
from .base import ViewBase


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
    OrbitsTable.floke_1_r,
    OrbitsTable.floke_2_r,
    OrbitsTable.floke_3_r,
    OrbitsTable.floke_4_r,
    OrbitsTable.floke_5_r,
    OrbitsTable.floke_6_r,
    OrbitsTable.t,
    OrbitsTable.cj,
    OrbitsTable.dist_primary,
    OrbitsTable.dist_secondary,
    OrbitsTable.stable,
    OrbitsTable.alpha,
    OrbitsTable.beta,
    OrbitsTable.stability_ind_1,
    OrbitsTable.stability_ind_2,
    OrbitsTable.stability_ind_3,
    OrbitFamiliesTable.family_tag,
    OrbitFamiliesTable.lib_point,
).select_from(
    join(OrbitsTable, OrbitFamiliesTable, OrbitsTable.family_id == OrbitFamiliesTable.id)
)

class OrbitViewTable(ViewBase):
    __table__ = view_query.cte("orbit_view")