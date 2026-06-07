from pydantic import BaseModel, ConfigDict, constr

# For MD5 hash (32 hex characters)
MD5Hash = constr(pattern=r'^[a-f0-9]{32}$')

class RepoBaseModel(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)


class RepoBaseIdModel(RepoBaseModel):
    id: int
