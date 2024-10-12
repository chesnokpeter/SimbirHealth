import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.infra.postgresql.tables import Base, ACCOUNT

from core.enums import Roles

DATABASE_URL = os.environ.get('POSTGRES_URL')

async def main():
    engine = create_async_engine(DATABASE_URL, echo=True)

    AsyncSessionLocal = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = ACCOUNT(lastName='user', firstName='user', username='user', password='user', roles=[Roles.USER])
            admin = ACCOUNT(lastName='admin', firstName='admin', username='admin', password='admin', roles=[Roles.ADMIN])
            doctor = ACCOUNT(lastName='doctor', firstName='doctor', username='doctor', password='doctor', roles=[Roles.DOCTOR])
            manager = ACCOUNT(lastName='manager', firstName='manager', username='manager', password='manager', roles=[Roles.MANAGER])
            session.add_all([user, admin, doctor, manager])
        await session.commit()

if __name__ == '__main__':
    asyncio.run(main())