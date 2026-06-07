from models.base import RepoBaseIdModel, RepoBaseModel


class CreateTrajectoryPointModel(RepoBaseModel):
    orbit_id: int
    x: float
    y: float
    z: float
    vx: float
    vy: float
    vz: float
    abs_v: float
    t: float


class TrajectoryPointModel(CreateTrajectoryPointModel):
    id: int


class TrajectoryPointResponseModel(RepoBaseIdModel):
    orbit_id: int
    x: float
    y: float
    z: float
    vx: float
    vy: float
    vz: float
    t: float
    abs_v: float


class UpdateTrajectoryPointModel(RepoBaseIdModel):
    orbit_id: int | None = None
    x: float | None = None
    y: float | None = None
    z: float | None = None
    vx: float | None = None
    vy: float | None = None
    vz: float | None = None
    t: float | None = None
