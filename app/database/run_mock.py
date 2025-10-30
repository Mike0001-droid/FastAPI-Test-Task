import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.activity import Activity
from app.database.models.building import Building
from app.database.models.company import Company, CompanyPhone
from app.database import AsyncSessionLocal

async def seed_data():
    async with AsyncSessionLocal() as db:
        activities_data = [
            {"name": "IT и технологии", "parent_id": None},
            {"name": "Торговля", "parent_id": None},
            {"name": "Услуги", "parent_id": None},
            {"name": "Производство", "parent_id": None},
            
            {"name": "Разработка ПО", "parent_id": 1},
            {"name": "Веб-разработка", "parent_id": 1},
            {"name": "Мобильная разработка", "parent_id": 1},
            {"name": "Кибербезопасность", "parent_id": 1},
            
            {"name": "Розничная торговля", "parent_id": 2},
            {"name": "Оптовая торговля", "parent_id": 2},
            {"name": "Интернет-магазин", "parent_id": 2},
            
            {"name": "Юридические услуги", "parent_id": 3},
            {"name": "Консалтинг", "parent_id": 3},
            {"name": "Образовательные услуги", "parent_id": 3},
            {"name": "Медицинские услуги", "parent_id": 3},
            
            {"name": "Пищевая промышленность", "parent_id": 4},
            {"name": "Машиностроение", "parent_id": 4},
            {"name": "Легкая промышленность", "parent_id": 4},
        ]
        
        activities = []
        for activity_data in activities_data:
            activity = Activity(**activity_data)
            db.add(activity)
            activities.append(activity)
        
        await db.commit()
        
        buildings_data = [
            {
                "address": "ул. Ленина, д. 10",
                "latitude": 55.7558,
                "longitude": 37.6173
            },
            {
                "address": "пр. Мира, д. 25",
                "latitude": 55.7818,
                "longitude": 37.6327
            },
            {
                "address": "ул. Пушкина, д. 5",
                "latitude": 55.7654,
                "longitude": 37.6056
            },
            {
                "address": "ул. Гагарина, д. 15",
                "latitude": 55.7412,
                "longitude": 37.6259
            },
            {
                "address": "пр. Ленинградский, д. 40",
                "latitude": 55.7964,
                "longitude": 37.5355
            }
        ]
        
        buildings = []
        for building_data in buildings_data:
            building = Building(**building_data)
            db.add(building)
            buildings.append(building)
        
        await db.commit()
        
        companies_data = [
            {
                "name": "ТехноСофт",
                "building_id": buildings[0].id,
                "activity_ids": [5, 6],  # Разработка ПО, Веб-разработка
                "phones": ["+7-999-123-45-67", "+7-495-123-45-67"]
            },
            {
                "name": "МегаМаркет",
                "building_id": buildings[1].id,
                "activity_ids": [9, 11],  # Розничная торговля, Интернет-магазин
                "phones": ["+7-999-234-56-78"]
            },
            {
                "name": "ЮрКонсалт",
                "building_id": buildings[2].id,
                "activity_ids": [12],  # Юридические услуги
                "phones": ["+7-495-234-56-78", "+7-999-345-67-89"]
            },
            {
                "name": "ПрогрессТех",
                "building_id": buildings[3].id,
                "activity_ids": [17],  # Машиностроение
                "phones": ["+7-499-345-67-89"]
            },
            {
                "name": "ИТРешения",
                "building_id": buildings[0].id,
                "activity_ids": [5, 7, 8],  # Разработка ПО, Мобильная разработка, Кибербезопасность
                "phones": ["+7-495-456-78-90"]
            },
            {
                "name": "Учебный Центр",
                "building_id": buildings[4].id,
                "activity_ids": [14],  # Образовательные услуги
                "phones": ["+7-499-567-89-01", "+7-999-456-78-90"]
            },
            {
                "name": "МедСервис",
                "building_id": buildings[2].id,
                "activity_ids": [15],  # Медицинские услуги
                "phones": ["+7-495-678-90-12"]
            },
            {
                "name": "ПромТорг",
                "building_id": buildings[1].id,
                "activity_ids": [10],  # Оптовая торговля
                "phones": ["+7-499-789-01-23"]
            }
        ]
        
        for company_data in companies_data:
            result = await db.execute(
                Activity.__table__.select().where(Activity.id.in_(company_data["activity_ids"]))
            )
            company_activities = result.fetchall()
            
            company = Company(
                name=company_data["name"],
                building_id=company_data["building_id"]
            )
            
            for activity_id in company_data["activity_ids"]:
                activity = next((a for a in activities if a.id == activity_id), None)
                if activity:
                    company.activities.append(activity)
            
            for phone in company_data["phones"]:
                company_phone = CompanyPhone(phone_number=phone)
                company.phones.append(company_phone)
            
            db.add(company)
        
        await db.commit()
        
        return {
            "Виды деятельности": len(activities),
            "Здания": len(buildings),
            "Компании": len(companies_data)
        }