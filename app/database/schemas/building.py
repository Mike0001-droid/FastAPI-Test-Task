from pydantic import BaseModel
from typing import Optional


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BaseModel):
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Building(BuildingBase):
    id: int
    
    class Config:
        from_attributes = True