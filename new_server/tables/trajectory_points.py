from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Index, Numeric

from .base import Base
from .orbits import OrbitsTable

class TrajectoryPointsTable(Base):

    
    orbit_id: Mapped[int] = mapped_column(
        ForeignKey("orbits.id", ondelete="CASCADE", deferrable=True), 
        nullable=False
    )
    __table_args__ = {'extend_existing': True}
    x: Mapped[float] = mapped_column(Numeric, nullable=False)
    y: Mapped[float] = mapped_column(Numeric, nullable=False)
    z: Mapped[float] = mapped_column(Numeric, nullable=False)
    vx: Mapped[float] = mapped_column(Numeric, nullable=False)
    vy: Mapped[float] = mapped_column(Numeric, nullable=False)
    vz: Mapped[float] = mapped_column(Numeric, nullable=False)
    abs_v: Mapped[float] = mapped_column(Numeric, nullable=False)
    t: Mapped[float] = mapped_column(Numeric, nullable=False)
    
    orbits: Mapped["OrbitsTable"] = relationship(back_populates="trajectory_points")

Index("ind_trajectory_points_orbit_id", TrajectoryPointsTable.orbit_id)