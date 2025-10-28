from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None


class Activity(ActivityBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class ActivityWithChildren(Activity):
    children: List['ActivityWithChildren'] = []

