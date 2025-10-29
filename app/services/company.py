from sqlalchemy import select, and_
from geopy.distance import geodesic
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.activity import ActivityService
from app.services.building import BuildingService
from app.database.models.building import Building
from app.database.models.activity import Activity
from app.database.models.company import Company, CompanyPhone
from app.database.schemas.company import CompanyCreate, CompanyUpdate
from app.services.exceptions import BuildingNotFound, ActivityNotFound



class CompanyService:
    async def get(self, db: AsyncSession, company_id: int):
        result = await db.execute(
            select(Company)
            .where(Company.id == company_id)
        )
        return result.scalar_one_or_none()
    
    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(Company)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(Company)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def delete(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(Company)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_companies(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(Company)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_companies_by_building(self, db: AsyncSession, building_id: int):
        result = await db.execute(
            select(Company)
            .where(Company.building_id == building_id)
        )
        return result.scalars().all()

    async def get_companies_by_activity(self, db: AsyncSession, activity_id: int):
        activity_descendants = await ActivityService().get_activity_descendants(db, activity_id)
        result = await db.execute(
            select(Company)
            .where(
                Company.activities.any(Activity.id.in_(activity_descendants))
            )
        )
        return result.scalars().all()

    async def search_companies_by_name(self, db: AsyncSession, name: str):
        result = await db.execute(
            select(Company)
            .where(Company.name.ilike(f"%{name}%"))
        )
        return result.scalars().all()

    async def get_companies_in_radius(self, db: AsyncSession, center_lat: float, center_lng: float, radius_km: float):
        result = await db.execute(
            select(Building)
        )
        buildings = result.scalars().all()
        
        companies_in_radius = []
        for building in buildings:
            distance = geodesic(
                (center_lat, center_lng), 
                (building.latitude, building.longitude)
            ).kilometers
            
            if distance <= radius_km:
                companies_in_radius.extend(building.companies)
        
        return companies_in_radius

    async def get_companies_in_rectangle(
        self,
        db: AsyncSession, 
        lat_min: float, 
        lat_max: float, 
        lng_min: float, 
        lng_max: float
    ):
        result = await db.execute(
            select(Building)
            .where(
                and_(
                    Building.latitude >= lat_min,
                    Building.latitude <= lat_max,
                    Building.longitude >= lng_min,
                    Building.longitude <= lng_max
                )
            )
        )
        buildings = result.scalars().all()
        
        companies_in_rect = []
        for building in buildings:
            companies_in_rect.extend(building.companies)
        
        return companies_in_rect

    async def search_companies_by_activity_tree(self, db: AsyncSession, activity_name: str):
        result = await db.execute(
            select(Activity).where(Activity.name.ilike(f"%{activity_name}%"))
        )
        activities = result.scalars().all()
        
        if not activities:
            return []
        
        all_activity_ids = set()
        for activity in activities:
            descendants = await ActivityService().get_activity_descendants(db, activity.id)
            all_activity_ids.update(descendants)
        
        result = await db.execute(
            select(Company)
            .where(Company.activities.any(Activity.id.in_(all_activity_ids)))
        )
        return result.scalars().all()

    async def create_company(self, db: AsyncSession, company_data: CompanyCreate):
        building = await BuildingService().get(db, company_data.building_id)
        if not building:
            raise BuildingNotFound(f"Building with id {company_data.building_id} not found")
        
        db_company = Company(
            name=company_data.name,
            building_id=company_data.building_id
        )
        if company_data.activity_ids:
            result = await db.execute(
                select(Activity).where(Activity.id.in_(company_data.activity_ids))
            )
            activities = result.scalars().all()
            if len(activities) < 1:
                raise ActivityNotFound(f"Activities with id {company_data.activity_ids} not found")
            db_company.activities.extend(activities)
        
        for phone in company_data.phone_numbers:
            db_phone = CompanyPhone(phone_number=phone)
            db_company.phones.append(db_phone)
        
        db.add(db_company)
        await db.commit()
        await db.refresh(db_company)
        
        result = await db.execute(
            select(Company)
            .where(Company.id == db_company.id)
        )
        return result.scalar_one()

    async def update_company(self, db: AsyncSession, company_id: int, company_data: CompanyUpdate):
        db_company = await self.get(db, company_id)
        if not db_company:
            return None
        
        update_data = company_data.model_dump(exclude_unset=True)
        
        if 'name' in update_data:
            db_company.name = update_data['name']
        
        if 'building_id' in update_data:
            db_company.building_id = update_data['building_id']
        
        if 'activity_ids' in update_data:
            result = await db.execute(
                select(Activity).where(Activity.id.in_(update_data['activity_ids']))
            )
            activities = result.scalars().all()
            db_company.activities = activities
        
        if 'phone_numbers' in update_data:
            db_company.phones = []
            for phone in update_data['phone_numbers']:
                db_phone = CompanyPhone(phone_number=phone)
                db_company.phones.append(db_phone)
        
        await db.commit()
        await db.refresh(db_company)
        
        return db_company
    
def get_company_service():
    return CompanyService()