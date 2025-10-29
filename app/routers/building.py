from app.services.decorators import get
from app.database.database import get_db
from app.services.auth import verify_api_key
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.base import AutoRouterGenerator
from app.services.building import BuildingService
from fastapi import Depends, Query, HTTPException
from app.database.schemas.building import BuildingCreate, \
     BuildingUpdate, Building


class BuildingRouter(AutoRouterGenerator):
    model_name = "buildings"
    service = BuildingService()
    schema = Building
    create_schema = BuildingCreate
    update_schema = BuildingUpdate
    prefix = "/buildings"
    tags = ["buildings"]

    @get("/search/address", response_model=Building)
    async def get_building_by_address(
        self,
        address: str = Query(..., description="Адрес здания"),
        db: AsyncSession = Depends(get_db),
        api_key: str = Depends(verify_api_key)
    ):
        building = await self.service.get_building_by_address(db, address)
        if not building:
            raise HTTPException(status_code=404, detail="Building not found")
        return building
