from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Index, Numeric, Boolean, String

from .base import Base

class OrbitsTable(Base):

    family_id: Mapped[int] = mapped_column(
        ForeignKey("orbit_families.id", ondelete="CASCADE", deferrable=True), 
        nullable=False
    )
    __table_args__ = {'extend_existing': True}
    unique_id: Mapped[str] = mapped_column(String(32), nullable=False)
    x: Mapped[float] = mapped_column(Numeric, nullable=False)
    y: Mapped[float] = mapped_column(Numeric, nullable=False)
    z: Mapped[float] = mapped_column(Numeric, nullable=False)
    vx: Mapped[float] = mapped_column(Numeric, nullable=False)
    vy: Mapped[float] = mapped_column(Numeric, nullable=False)
    vz: Mapped[float] = mapped_column(Numeric, nullable=False)
    abs_v: Mapped[float] = mapped_column(Numeric, nullable=False)
    t: Mapped[float] = mapped_column(Numeric, nullable=False)
    floke_1_r: Mapped[float] = mapped_column(Numeric, nullable=False)
    floke_2_r: Mapped[float] = mapped_column(Numeric, nullable=False)
    floke_3_r: Mapped[float] = mapped_column(Numeric, nullable=False)
    floke_4_r: Mapped[float] = mapped_column(Numeric, nullable=False)
    floke_5_r: Mapped[float] = mapped_column(Numeric, nullable=False)
    floke_6_r: Mapped[float] = mapped_column(Numeric, nullable=False)
    floke_1_im: Mapped[float] = mapped_column(Numeric, nullable=False)
    floke_2_im: Mapped[float] = mapped_column(Numeric, nullable=False)
    floke_3_im: Mapped[float] = mapped_column(Numeric, nullable=False)
    floke_4_im: Mapped[float] = mapped_column(Numeric, nullable=False)
    floke_5_im: Mapped[float] = mapped_column(Numeric, nullable=False)
    floke_6_im: Mapped[float] = mapped_column(Numeric, nullable=False)
    ax: Mapped[float] = mapped_column(Numeric, nullable=False)
    ay: Mapped[float] = mapped_column(Numeric, nullable=False)
    az: Mapped[float] = mapped_column(Numeric, nullable=False)
    
    dist_primary: Mapped[float] = mapped_column(Numeric, nullable=False)
    dist_secondary: Mapped[float] = mapped_column(Numeric, nullable=False)
    
    cj: Mapped[float] = mapped_column(Numeric, nullable=False)
    stable: Mapped[bool] = mapped_column(Boolean)
    
    stability_ind_1: Mapped[float] = mapped_column(Numeric, nullable=False)
    stability_ind_2: Mapped[float] = mapped_column(Numeric, nullable=False)
    stability_ind_3: Mapped[float] = mapped_column(Numeric, nullable=False)

    alpha: Mapped[float] = mapped_column(Numeric, nullable=False)
    beta: Mapped[float] = mapped_column(Numeric, nullable=False)

    family: Mapped["OrbitFamiliesTable"] = relationship(back_populates="orbits")
    trajectory_points: Mapped[list["TrajectoryPointsTable"]] = relationship(
        back_populates="orbits", 
        cascade="all, delete-orphan"
    )
    poincare_sections: Mapped[list["PoincareSectionsTable"]] = relationship(
        back_populates="orbits", 
        cascade="all, delete-orphan"    
    )

Index("ind_orbits_family_id", OrbitsTable.family_id)
Index("ind_orbits_x", OrbitsTable.x)
Index("ind_orbits_y", OrbitsTable.y)
Index("ind_orbits_z", OrbitsTable.z)
Index("ind_orbits_vx", OrbitsTable.vx)
Index("ind_orbits_vy", OrbitsTable.vy)
Index("ind_orbits_vz", OrbitsTable.vz)
Index("ind_orbits_t", OrbitsTable.t)
Index("ind_orbits_ax", OrbitsTable.ax)
Index("ind_orbits_ay", OrbitsTable.ay)
Index("ind_orbits_az", OrbitsTable.az)
Index("ind_orbits_dist_primary", OrbitsTable.dist_primary)
Index("ind_orbits_dist_secondary", OrbitsTable.dist_secondary)
Index("ind_orbits_cj", OrbitsTable.cj)