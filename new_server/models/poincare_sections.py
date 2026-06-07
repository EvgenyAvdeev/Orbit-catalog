from models.base import RepoBaseModel, RepoBaseIdModel


class CreatePoincareSectionModel(RepoBaseModel):
    orbit_id: int
    plane: str
    x: float
    y: float
    z: float
    vx: float
    vy: float
    vz: float
    abs_v: float
    t: float


class PoincareSectionModel(CreatePoincareSectionModel):
    id: int


class UpdatePoincareSectionModel(RepoBaseIdModel):
    orbit_id: int | None = None
    plane: str | None = None
    x: float | None = None
    y: float | None = None
    z: float | None = None
    vx: float | None = None
    vy: float | None = None
    vz: float | None = None
    t: float | None = None