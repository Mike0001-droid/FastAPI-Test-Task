from app.services.base import CRUDBase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.building import Building


class BuildingService(CRUDBase):
    model = Building

    @classmethod
    async def get_building_by_address(cls, db: AsyncSession, address: str):
        result = await db.execute(select(Building).where(Building.address == address))
        return result.scalar_one_or_none()
