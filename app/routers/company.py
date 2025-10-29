from typing import List
from app.database.database import get_db
from app.services.auth import verify_api_key
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.company import CompanyService
from app.services.company import get_company_service
from app.database.schemas.company import Company, \
     CompanyCreate, CompanyUpdate, CompanyWithRelations
from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.exceptions import BuildingNotFound, ActivityNotFound


class CompanyRouter:
    model_name = "companies"
    schema = Company
    create_schema = CompanyCreate
    update_schema = CompanyUpdate
    prefix = "/companies"
    tags = ["companies"]
    router = APIRouter(
        prefix=prefix, 
        tags=tags,
        dependencies=[Depends(verify_api_key)]
    )
    
    @router.get("/building/{building_id}", response_model=List[CompanyWithRelations])
    async def get_companies_in_building(
        building_id: int,
        db: AsyncSession = Depends(get_db),
        service: CompanyService = Depends(get_company_service)
    ):
        """Список всех организаций находящихся в конкретном здании"""
        companies = await service.get_companies_by_building(db, building_id)
        return companies
    
    @router.get("/activity/{activity_id}", response_model=List[CompanyWithRelations])
    async def get_companies_by_activity(
        activity_id: int,
        db: AsyncSession = Depends(get_db),
        service: CompanyService = Depends(get_company_service)
    ):
        """Список всех организаций, которые относятся к указанному виду деятельности"""
        companies = await service.get_companies_by_activity(db, activity_id)
        return companies
    
    @router.get("/search/location/radius", response_model=List[CompanyWithRelations])
    async def get_companies_in_radius(
        lat: float = Query(..., description="Center latitude"),
        lng: float = Query(..., description="Center longitude"),
        radius: float = Query(..., description="Radius in kilometers"),
        db: AsyncSession = Depends(get_db),
        service: CompanyService = Depends(get_company_service)
    ):
        """Список организаций, которые находятся в заданном радиусе"""
        companies = await service.get_companies_in_radius(db, lat, lng, radius)
        return companies
    
    @router.get("/search/location/rectangle", response_model=List[CompanyWithRelations])
    async def get_companies_in_rectangle(
        lat_min: float = Query(..., description="Minimum latitude"),
        lat_max: float = Query(..., description="Maximum latitude"),
        lng_min: float = Query(..., description="Minimum longitude"),
        lng_max: float = Query(..., description="Maximum longitude"),
        db: AsyncSession = Depends(get_db),
        service: CompanyService = Depends(get_company_service)
    ):
        """Список организаций, которые находятся в заданноЙ прямоугольной области"""
        companies = await service.get_companies_in_rectangle(
            db, lat_min, lat_max, lng_min, lng_max
        )
        return companies
    
    @router.get("/search/activity", response_model=List[CompanyWithRelations])
    async def search_companies_by_activity(
        activity_name: str = Query(..., description="Activity name to search"),
        db: AsyncSession = Depends(get_db),
        service: CompanyService = Depends(get_company_service)
    ):
        """Искать организации по виду деятельности"""
        companies = await service.search_companies_by_activity_tree(
            db, activity_name
        )
        return companies
    
    @router.get("/search/name", response_model=List[CompanyWithRelations])
    async def search_companies_by_name(
        name: str = Query(..., description="Company name to search"),
        db: AsyncSession = Depends(get_db),
        service: CompanyService = Depends(get_company_service)
    ):
        """Поиск организации по названию"""
        companies = await service.search_companies_by_name(db, name)
        return companies
    
    @router.get("/", response_model=List[CompanyWithRelations])
    async def get_all_companies(
        skip: int = Query(0, description="Skip records"),
        limit: int = Query(100, description="Limit records", le=1000),
        db: AsyncSession = Depends(get_db),
        service: CompanyService = Depends(get_company_service),
    ):
        """Получение всех компаний"""
        companies = await service.get_multi(db, skip=skip, limit=limit)
        return companies
    
    @router.get("/{item_id}", response_model=schema)
    async def read_item(
        item_id: int, 
        db: AsyncSession = Depends(get_db),
        service: CompanyService = Depends(get_company_service)
    ):
        """Получение компании по её id"""
        company = await service.get(db, item_id)
        if not company:
            raise HTTPException(status_code=404, detail=f"Company not found")
        return company
    
    @router.delete("/{company_id}")
    async def delete_company(
        company_id: int,
        db: AsyncSession = Depends(get_db),
        service: CompanyService = Depends(get_company_service)
    ):
        """Удаление компании"""
        company = await service.get(db, company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        await service.delete(db, id=company_id)
        return {"message": "Company deleted successfully"}
    
    @router.post("/", response_model=CompanyWithRelations)
    async def create_company(
        company: CompanyCreate,
        db: AsyncSession = Depends(get_db),
        service: CompanyService = Depends(get_company_service)
    ):
        """Создание компании"""
        print("Переданные деятельности", company.activity_ids)
        try:
            return await service.create_company(db, company)
        except ActivityNotFound as e:
            raise HTTPException(status_code=404, detail="Activities not found")
        except BuildingNotFound as e:
            raise HTTPException(status_code=404, detail="Building not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating company: {str(e)}")
        
    @router.put("/{company_id}", response_model=CompanyWithRelations)
    async def update_company(
        company_id: int,
        company: CompanyUpdate,
        db: AsyncSession = Depends(get_db),
        service: CompanyService = Depends(get_company_service)
    ):
        """Обновление компании"""
        updated_company = await service.update_company(db, company_id, company)
        if not updated_company:
            raise HTTPException(status_code=404, detail="Company not found")
        return updated_company
    
    def get_router(self):
        return getattr(self, 'router', None)
    