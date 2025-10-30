from pydantic import BaseModel
from typing import List, Optional
from .building import Building
from .activity import Activity

class PhoneBase(BaseModel):
    phone_number: str


class CompanyBase(BaseModel):
    name: str
    building_id: int


class CompanyCreate(CompanyBase):
    phone_numbers: List[str]
    activity_ids: List[int]


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    building_id: Optional[int] = None
    phone_numbers: Optional[List[str]] = None
    activity_ids: Optional[List[int]] = None


class Company(CompanyBase):
    id: int
    phones: List[PhoneBase]
    
    class Config:
        from_attributes = True


class CompanyWithRelations(Company):
    building: Building
    activities: List[Activity]