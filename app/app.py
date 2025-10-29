from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routers.activity import ActivityRouter
from app.routers.building import BuildingRouter
from app.routers.company import CompanyRouter


app = FastAPI(
    title="Company Directory API",
    description="REST API для справочника организаций, зданий и видов деятельности",
    version="1.0.0"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "Enter your API key"
        }
    }    
    openapi_schema["security"] = [{"APIKeyHeader": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def read_root():
    return {"message": "Company Directory API"}


app.include_router(ActivityRouter().get_router())
app.include_router(BuildingRouter().get_router())
app.include_router(CompanyRouter().get_router())

