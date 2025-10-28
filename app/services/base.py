from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, List, Optional, Any, ClassVar
from sqlalchemy.ext.declarative import DeclarativeMeta


class CRUDBase:
    model: ClassVar[Type[DeclarativeMeta]]
    
    @classmethod
    async def get(cls, db: AsyncSession, id: Any) -> Optional[DeclarativeMeta]:
        result = await db.execute(select(cls.model).where(cls.model.id == id))
        return result.scalar_one_or_none()
    
    @classmethod
    async def get_multi(cls, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[DeclarativeMeta]:
        result = await db.execute(select(cls.model).offset(skip).limit(limit))
        return result.scalars().all()
    
    @classmethod
    async def create(cls, db: AsyncSession, obj_in: BaseModel) -> DeclarativeMeta:
        obj_in_data = obj_in.model_dump()
        db_obj = cls.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    @classmethod
    async def update(cls, db: AsyncSession, db_obj: DeclarativeMeta, obj_in: BaseModel) -> DeclarativeMeta:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    @classmethod
    async def delete(cls, db: AsyncSession, id: Any) -> bool:
        try:
            obj = await cls.get(db, id)
            if not obj:
                return False
            await db.delete(obj)
            await db.flush()
            await db.commit()
            return True
        except Exception:
            await db.rollback()
            raise