import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from core.infra.postgresql.tables import Base, ACCOUNT

from core.enums import Roles

DATABASE_URL = os.environ.get('POSTGRES_URL')


async def main():
    engine = create_async_engine(DATABASE_URL)

    AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def add_if_not(session, lastName, firstName, username, password, roles):
        stmt = select(ACCOUNT).filter_by(
            lastName=lastName,
            firstName=firstName,
            username=username,
            password=password,
            roles=roles,
        )
        res = await session.execute(stmt)
        res = res.first()
        if not res:
            user = ACCOUNT(
                lastName=lastName,
                firstName=firstName,
                username=username,
                password=password,
                roles=roles,
            )
            session.add(user)

    async with AsyncSessionLocal() as session:
        async with session.begin():
            await add_if_not(
                session,
                lastName='user',
                firstName='user',
                username='user',
                password='user',
                roles=[Roles.USER],
            )
            await add_if_not(
                session,
                lastName='admin',
                firstName='admin',
                username='admin',
                password='admin',
                roles=[Roles.ADMIN],
            )
            await add_if_not(
                session,
                lastName='doctor',
                firstName='doctor',
                username='doctor',
                password='doctor',
                roles=[Roles.DOCTOR],
            )
            await add_if_not(
                session,
                lastName='manager',
                firstName='manager',
                username='manager',
                password='manager',
                roles=[Roles.MANAGER],
            )

        await session.commit()


if __name__ == '__main__':
    asyncio.run(main())
