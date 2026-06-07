from models.base import RepoBaseModel


class OrbitPoincareViewModel(RepoBaseModel):
    orbit_id: int
    x: float
    y: float
    z: float
    abs_v: float
    vx: float
    vy: float
    vz: float
    ax: float
    ay: float
    az: float
    t: float
    cj: float
    dist_primary: float
    dist_secondary: float
    lib_point: str
    family_tag: str
    plane: str
    x_points: list[float]
    y_points: list[float]
    z_points: list[float]
    vx_points: list[float]
    vy_points: list[float]
    vz_points: list[float]
    t_points: list[float]
    points_count: int


class PoincareResponseModel(RepoBaseModel):
    orbit_id: int
    x: float
    y: float
    z: float
    vx: float
    vy: float
    vz: float
    ax: float
    ay: float
    az: float
    dist_primary: float
    dist_secondary: float
    abs_v: float
    x_points: list[float]
    y_points: list[float]
    z_points: list[float]
    vx_points: list[float]
    vy_points: list[float]
    vz_points: list[float]
    points_count: int
