from abc import ABC, abstractmethod
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result


class AbstractRepository(ABC):

    @abstractmethod
    async def find_one():
        raise NotImplementedError
    

    @abstractmethod
    async def find_all():
        raise NotImplementedError


    @abstractmethod
    async def create():
        raise NotImplementedError


    @abstractmethod
    async def update():
        raise NotImplementedError
    

    @abstractmethod
    async def delete():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def find_all(self, limit, offset):
        stmt = select(self.model).limit(limit).offset(offset)
        res: Result = await self.session.execute(stmt)
        return res.scalars().all()
    

    async def find_one(self, pk: int):
        stmt = select(self.model).where(self.model == pk)
        res: Result = await self.session.execute(stmt)
        return res.scalar_one_or_none()
    

    async def create(self, data: dict):
        new_data = self.model(**data)
        self.session.add(new_data)
        await self.session.commit()
        return new_data
    

    async def update(self, pk: int, data: dict):
        stmt = (
            update(self.model)
            .where(self.model.id == pk)
            .values(**data)
            .returning(self.model)
        )
        res: Result = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar()
    

    async def delete(self, pk: int):
        stmt = delete(self.model).where(self.model.id == pk)
        await self.session.execute(stmt)
        await self.session.commit()
