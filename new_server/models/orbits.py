from .base import RepoBaseModel, RepoBaseIdModel, MD5Hash



class CreateOrbitModel(RepoBaseModel):
    family_id: int
    unique_id: str
    x: float
    y: float
    z: float
    vx: float
    vy: float
    vz: float
    abs_v: float
    t: float
    floke_1_r: float
    floke_2_r: float
    floke_3_r: float
    floke_4_r: float
    floke_5_r: float
    floke_6_r: float
    floke_1_im: float
    floke_2_im: float
    floke_3_im: float
    floke_4_im: float
    floke_5_im: float
    floke_6_im: float
    ax: float
    ay: float
    az: float
    dist_primary: float
    dist_secondary: float
    cj: float
    stable: bool
    stability_ind_1: float
    stability_ind_2: float
    stability_ind_3: float
    alpha: float
    beta: float

class OrbitModel(CreateOrbitModel):
    id: int


class UpdateOrbitModel(RepoBaseIdModel):
    family_id: int | None = None
    x: float | None = None
    y: float | None = None
    z: float | None = None
    vx: float | None = None
    vy: float | None = None
    vz: float | None = None
    t: float | None = None
    floke_1_r: float | None = None
    floke_2_r: float | None = None
    floke_3_r: float | None = None
    floke_4_r: float | None = None
    floke_5_r: float | None = None
    floke_6_r: float | None = None
    floke_1_im: float | None = None
    floke_2_im: float | None = None
    floke_3_im: float | None = None
    floke_4_im: float | None = None
    floke_5_im: float | None = None
    floke_6_im: float | None = None
    ax: float | None = None
    ay: float | None = None
    az: float | None = None
    dist_primary: float | None = None
    dist_secondary: float | None = None
    cj: float | None = None
    stable: bool | None = None
    stability_ind_1: float | None = None
    stability_ind_2: float | None = None
    stability_ind_3: float | None = None
    alpha: float | None = None
    beta: float | None = None