from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Numeric, String, Boolean

from .base import Base
from .orbits import OrbitsTable

class OrbitFamiliesTable(Base):

    
    lib_point: Mapped[str] = mapped_column(String(20), nullable=False)
    family_tag: Mapped[str] = mapped_column(String(20), nullable=False)
    
    min_x: Mapped[float] = mapped_column(Numeric, nullable=True)
    min_y: Mapped[float] = mapped_column(Numeric, nullable=True)
    min_z: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_x: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_y: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_z: Mapped[float] = mapped_column(Numeric, nullable=True)
    
    min_vx: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_vx: Mapped[float] = mapped_column(Numeric, nullable=True)
    min_vy: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_vy: Mapped[float] = mapped_column(Numeric, nullable=True)
    min_vz: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_vz: Mapped[float] = mapped_column(Numeric, nullable=True)

    min_abs_v: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_abs_v: Mapped[float] = mapped_column(Numeric, nullable=True)

    min_t: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_t: Mapped[float] = mapped_column(Numeric, nullable=True)

    min_cj: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_cj: Mapped[float] = mapped_column(Numeric, nullable=True)

    min_ax: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_ax: Mapped[float] = mapped_column(Numeric, nullable=True)
    min_ay: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_ay: Mapped[float] = mapped_column(Numeric, nullable=True)
    min_az: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_az: Mapped[float] = mapped_column(Numeric, nullable=True)
    
    min_dist_primary: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_dist_primary: Mapped[float] = mapped_column(Numeric, nullable=True)
    min_dist_secondary: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_dist_secondary: Mapped[float] = mapped_column(Numeric, nullable=True)

    min_stability_ind_1: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_stability_ind_1: Mapped[float] = mapped_column(Numeric, nullable=True)
    min_stability_ind_2: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_stability_ind_2: Mapped[float] = mapped_column(Numeric, nullable=True)
    min_stability_ind_3: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_stability_ind_3: Mapped[float] = mapped_column(Numeric, nullable=True)

    min_alpha: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_alpha: Mapped[float] = mapped_column(Numeric, nullable=True)
    min_beta: Mapped[float] = mapped_column(Numeric, nullable=True)
    max_beta: Mapped[float] = mapped_column(Numeric, nullable=True)

    orbits: Mapped[list["OrbitsTable"]] = relationship(back_populates="family", cascade="all, delete-orphan")