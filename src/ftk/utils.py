from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result

from typing import Type, List
from abc import ABC, abstractmethod

from src.config.base import Base


class Repository(ABC):


    @abstractmethod
    async def create(self, **kwargs) -> Type[Base]:
        ...

    @abstractmethod
    async def update(self, id: int, **kwargs) -> Type[Base]:
        ...

    @abstractmethod
    async def get_data_by_id(self, id: int) -> Type[Base]:
        ...

    @abstractmethod
    async def get_all(self) -> List[Type[Base]]:    
        ...

    @abstractmethod
    async def delete(self, id: int) -> None:    
        ...

class BaseRepository(Repository):


    def __init__(self, model: Type[Base], session: AsyncSession) -> None:
        self.session = session
        self.model = model

    async def create(self, **kwargs) -> Type[Base]:
        try:
            return await self._create(**kwargs)
        except Exception as e:
            print(f"Failed {e}")
            raise ValueError("Cannot create data")
    
    async def _create(self, **kwargs):
        new_data = self.model(**kwargs)
        self.session.add(new_data)
        return await self._commit_and_refresh(new_data)

    async def _commit_and_refresh(self, instance: Type[Base]) -> Type[Base]:
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
    
    async def update(self, id: int, **kwargs) -> Type[Base]:
        try:
            return await self._update(id, **kwargs)
        except Exception as e:
            print(f"Failed {e}")
            raise ValueError("Cannot update data")
        
    async def _update(self, id: int, **kwargs) -> Type[Base]:
        data = self.get_data_by_id(id)
        updated_data = self._update_instance(data, **kwargs)
        await self._commit_and_refresh(updated_data)
        return updated_data

    async def _update_instance(self, instance: Type[Base], /, **kwargs) -> Type[Base]:
        for key, value in kwargs.items():
            if value is not None: 
                setattr(instance, key, value)
        return instance     

    async def get_data_by_id(self, id: int) -> Type[Base]:
        data = await self.get_all()
        if not data:
            print(f"Failed {e}")
            raise ValueError(f"Not found data with id {id}")
        return data[0]
    
    async def get_all(self) -> List[Type[Base]]:
        stmt = select(self.model).where(self.model.id==id)
        result: Result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def delete(self, id: int) -> None:    
        data = await self.get_data_by_id(id)
        await self.session.delete(data)
        await self.session.commit()