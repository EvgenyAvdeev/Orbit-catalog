from models.base import RepoBaseModel, RepoBaseIdModel

class CreateOrbitFamilyModel(RepoBaseModel):
    lib_point: str
    family_tag: str
    min_x: float
    min_y: float
    min_z: float
    max_x: float
    max_y: float
    max_z: float
    min_vx: float
    max_vx: float
    min_vy: float
    max_vy: float
    min_vz: float
    max_vz: float
    min_abs_v: float
    max_abs_v: float
    min_t: float
    max_t: float
    min_cj: float
    max_cj: float
    min_ax: float
    max_ax: float
    min_ay: float
    max_ay: float
    min_az: float
    max_az: float
    min_dist_primary: float
    max_dist_primary: float
    min_dist_secondary: float
    max_dist_secondary: float
    min_stability_ind_1: float
    max_stability_ind_1: float
    min_stability_ind_2: float
    max_stability_ind_2: float
    min_stability_ind_3: float
    max_stability_ind_3: float
    min_alpha: float
    max_alpha: float
    min_beta: float
    max_beta: float

class OrbitFamilyModel(CreateOrbitFamilyModel):
    id: int


class UpdateOrbitFamilyModel(RepoBaseIdModel):
    tag: str | None = None
    min_x: float | None = None
    min_y: float | None = None
    min_z: float | None = None
    max_x: float | None = None
    max_y: float | None = None
    max_z: float | None = None
    min_vx: float | None = None
    max_vx: float | None = None
    min_vy: float | None = None
    max_vy: float | None = None
    min_vz: float | None = None
    max_vz: float | None = None
    min_abs_v: float | None = None
    max_abs_v: float | None = None
    min_t: float | None = None
    max_t: float | None = None
    min_cj: float | None = None
    max_cj: float | None = None
    min_ax: float | None = None
    max_ax: float | None = None
    min_ay: float | None = None
    max_ay: float | None = None
    min_az: float | None = None
    max_az: float | None = None
    min_dist_primary: float | None = None
    max_dist_primary: float | None = None
    min_dist_secondary: float | None = None
    max_dist_secondary: float | None = None
    min_stability_ind_1: float | None = None
    max_stability_ind_1: float | None = None
    min_stability_ind_2: float | None = None
    max_stability_ind_2: float | None = None
    min_stability_ind_3: float | None = None
    max_stability_ind_3: float | None = None
    min_alpha: float | None = None
    max_alpha: float | None = None
    min_beta: float | None = None
    max_beta: float | None = None
    correct_bypass: bool | None = None