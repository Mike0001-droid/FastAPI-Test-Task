from typing import List
from fastapi import Depends
from app.services.decorators import get
from app.database.database import get_db
from app.services.auth import verify_api_key
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.base import AutoRouterGenerator
from app.services.activity import ActivityService
from app.database.schemas.activity import ActivityCreate, \
     ActivityUpdate, Activity
from app.database.schemas.activity import ActivityWithChildren


class ActivityRouter(AutoRouterGenerator):
    model_name = "activities"
    service = ActivityService()
    schema = Activity
    create_schema = ActivityCreate
    update_schema = ActivityUpdate
    prefix = "/activities"
    tags = ["activities"]

    @get("/get_activities_tree", response_model=List[ActivityWithChildren])
    async def get_activities_tree(
        self,
        db: AsyncSession = Depends(get_db),
        api_key: str = Depends(verify_api_key)
    ):
        result = await self.service.get_activities_tree(db)
        return result

        