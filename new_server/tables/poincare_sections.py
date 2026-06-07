from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Index, Numeric, String

from .base import Base
from .orbits import OrbitsTable

class PoincareSectionsTable(Base):

    
    orbit_id: Mapped[int] = mapped_column(
        ForeignKey("orbits.id", ondelete="CASCADE", deferrable=True), 
        nullable=False
    )
    __table_args__ = {'extend_existing': True}
    plane: Mapped[str] = mapped_column(String(8), nullable=False)
    x: Mapped[float] = mapped_column(Numeric, nullable=False)
    y: Mapped[float] = mapped_column(Numeric, nullable=False)
    z: Mapped[float] = mapped_column(Numeric, nullable=False)
    vx: Mapped[float] = mapped_column(Numeric, nullable=False)
    vy: Mapped[float] = mapped_column(Numeric, nullable=False)
    vz: Mapped[float] = mapped_column(Numeric, nullable=False)
    abs_v: Mapped[float] = mapped_column(Numeric, nullable=False)
    t: Mapped[float] = mapped_column(Numeric, nullable=False)
    
    orbits: Mapped["OrbitsTable"] = relationship(back_populates="poincare_sections")

Index("ind_poincare_sections_orbit_id_plane", PoincareSectionsTable.orbit_id, PoincareSectionsTable.plane)