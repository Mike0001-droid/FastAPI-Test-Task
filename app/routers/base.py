from typing import List
from app.database.database import get_db
from app.services.auth import verify_api_key
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException


class AutoRouterGenerator:
    def __init__(self):
        self._routers = {}
        
        if hasattr(self, 'model_name') and hasattr(self, 'service') and hasattr(self, 'schema'):
            self.router = APIRouter(
                prefix=getattr(self, 'prefix', None) or f"/{self.model_name}",
                tags=getattr(self, 'tags', None) or [self.model_name],
                dependencies=[Depends(verify_api_key)]
            )
            
            self._register_decorated_methods()
            
            self._add_auto_routes()
            
            self._remove_disabled_routes()

    
    def _remove_disabled_routes(self):
        if hasattr(self, 'disabled_routes'):
            disabled_routes = getattr(self, 'disabled_routes', {})
            
            route_mapping = {
                'get_all': {'path': self.router.prefix + '/', 'methods': ['GET']},
                'get_by_id': {'path': self.router.prefix + '/{item_id}', 'methods': ['GET']},
                'create': {'path': self.router.prefix + '/', 'methods': ['POST']},
                'update': {'path': self.router.prefix + '/{item_id}', 'methods': ['PUT']},
                'delete': {'path': self.router.prefix + '/{item_id}', 'methods': ['DELETE']},
            }
            
            self.router.routes = [
                route for route in self.router.routes
                if not any(
                    route.path == route_info['path'] and 
                    any(method in route_info['methods'] for method in route.methods)
                    for disabled_route, route_info in route_mapping.items()
                    if disabled_route in disabled_routes
                )
            ]

    def _register_decorated_methods(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, '_route_info'):
                route_info = getattr(attr, '_route_info')
                self.router.add_api_route(
                    route_info['path'],
                    attr,
                    methods=[route_info['method']],
                    response_model=route_info.get('response_model')
                )
    
    def _add_auto_routes(self):
        if not hasattr(self, 'service') or not hasattr(self, 'schema'):
            return
        
        crud_instance = self.service
        schema = self.schema
        create_schema = getattr(self, 'create_schema', None)
        update_schema = getattr(self, 'update_schema', None)
        model_name = getattr(self, 'model_name', 'item')
        
        if not self._is_route_disabled('get_all'):
            @self.router.get("/", response_model=List[schema])
            async def read_items(skip: int = 0, limit: int = 100,
                db: AsyncSession = Depends(get_db)
            ):
                return await crud_instance.get_multi(db, skip=skip, limit=limit)
        
        if not self._is_route_disabled('get_by_id'):
            @self.router.get("/{item_id}", response_model=schema)
            async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
                item = await crud_instance.get(db, item_id)
                if not item:
                    raise HTTPException(status_code=404, detail=f"{model_name} not found")
                return item
        
        if create_schema and not self._is_route_disabled('create'):
            @self.router.post("/", response_model=schema)
            async def create_item(item: create_schema, db: AsyncSession = Depends(get_db)):
                return await crud_instance.create(db, obj_in=item)
        
        if update_schema and not self._is_route_disabled('update'):
            @self.router.put("/{item_id}", response_model=schema)
            async def update_item(item_id: int, item: update_schema, db: AsyncSession = Depends(get_db)):
                db_item = await crud_instance.get(db, item_id)
                if not db_item:
                    raise HTTPException(status_code=404, detail=f"{model_name} not found")
                return await crud_instance.update(db, db_obj=db_item, obj_in=item)
        
        if not self._is_route_disabled('delete'):
            @self.router.delete("/{item_id}")
            async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
                item = await crud_instance.delete(db, id=item_id)
                if not item:
                    raise HTTPException(status_code=404, detail=f"{model_name} not found")
                return {"message": f"{model_name} deleted successfully"}

    def _is_route_disabled(self, route_name: str) -> bool:
        disabled_routes = getattr(self, 'disabled_routes', {})
        return route_name in disabled_routes
    
    def get_router(self):
        return getattr(self, 'router', None)
    
    def get_all_routers(self):
        return list(self._routers.values())