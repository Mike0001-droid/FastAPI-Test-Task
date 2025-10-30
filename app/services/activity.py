from typing import Optional
from sqlalchemy import select
from app.services.base import CRUDBase
from app.database.models.activity import Activity
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.schemas.activity import ActivityWithChildren


class ActivityService(CRUDBase):
    model = Activity

    @classmethod
    async def get_activity_by_name(cls, db: AsyncSession, name: str):
        result = await db.execute(select(Activity).where(Activity.name == name))
        return result.scalar_one_or_none()

    @classmethod
    async def get_activities_tree(cls, db: AsyncSession, max_depth: int = 3):
        async def get_children(parent_id: Optional[int], current_depth: int = 0):
            if current_depth >= max_depth:
                return []
            result = await db.execute(
                select(Activity).where(Activity.parent_id == parent_id)
            )
            activities = result.scalars().all()
            result_activities = []
            for activity in activities:
                children = await get_children(activity.id, current_depth + 1)
                activity_dict = ActivityWithChildren(
                    id=activity.id,
                    name=activity.name,
                    parent_id=activity.parent_id,
                    children=children
                )
                result_activities.append(activity_dict)
            return result_activities
        return await get_children(None)
    
    @classmethod
    async def get_activity_descendants(cls, db: AsyncSession, activity_id: int, max_depth: int = 3):
        async def get_descendants_ids(parent_id: int, current_depth: int = 0, collected_ids: set = None):
            if collected_ids is None:
                collected_ids = set()
            if current_depth >= max_depth:
                return collected_ids
            result = await db.execute(
                select(Activity).where(Activity.parent_id == parent_id)
            )
            children = result.scalars().all()
            for child in children:
                collected_ids.add(child.id)
                await get_descendants_ids(child.id, current_depth + 1, collected_ids)
            return collected_ids
        activity = await cls.get(db, activity_id)
        if not activity:
            return set()
        descendant_ids = await get_descendants_ids(activity_id)
        descendant_ids.add(activity_id)
        return descendant_ids