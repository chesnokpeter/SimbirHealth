from typing import Annotated, TypeAlias
from core.enums import Roles
from core.exceptions import AccountException
from core.models.account import AccountModel
from core.schemas.account import SignUpSch, SignInSch, SignOutSch, UpdateSch, AdminCreate
from core.services.abstract import AbsService
from core.uow import BaseUnitOfWork, UnitOfWork, uowaccess

UnitOfWork: TypeAlias = Annotated[BaseUnitOfWork, UnitOfWork]


class AccountService(AbsService):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @uowaccess('account')
    async def signup(self, data: SignUpSch) -> AccountModel:
        async with self.uow:
            exist = await self.uow.account.get_one(username=data.username)
            if exist:
                raise AccountException('account already exist')

            u = await self.uow.account.add(**data.model_dump(), roles=[Roles.USER])
            await self.uow.commit()
            return u.model()



    @uowaccess('account')
    async def signin(self, data: SignInSch) -> AccountModel:
        async with self.uow:
            u = await self.uow.account.get_one(username=data.username, password=data.password)
            if not u:
                raise AccountException('login or password is incorrect')

            return u.model()



    @uowaccess('account')
    async def me(self, id: int) -> AccountModel:
        async with self.uow:
            u = await self.uow.account.get_one(id=id)
            if not u:
                raise AccountException('account not found')

            return u.model()



    @uowaccess('lostoken')
    async def signout(self, data: SignOutSch) -> None:
        async with self.uow:
            await self.uow.lostoken.add(**data.model_dump())
            await self.uow.commit()



    @uowaccess('lostoken')
    async def checklostoken(self, accessToken: str = None, refreshToken: str = None) -> None:
        async with self.uow:
            if accessToken:
                t = await self.uow.lostoken.get_one(accessToken=accessToken)
                if t: raise AccountException('accessToken has already been used')
            if refreshToken:
                t = await self.uow.lostoken.get_one(refreshToken=refreshToken)
                if t: raise AccountException('refreshToken has already been used')



    @uowaccess('account')
    async def update(self, id: int, data: UpdateSch) -> AccountModel:
        async with self.uow:
            u = await self.uow.account.get_one(id=id)
            if not u:
                raise AccountException('account does not exist')

            u = await self.uow.account.update(id=id, **data.model_dump())
            await self.uow.commit()
            return u.model()
        



    @uowaccess('account')
    async def get_all(self, from_: int, count: int) -> list[AccountModel] | None:
        async with self.uow:
            u = await self.uow.account.offset(from_, count)
            return [i.model() for i in u]
        



    @uowaccess('account')
    async def admin_create(self, data: AdminCreate) -> AccountModel:
        async with self.uow:
            exist = await self.uow.account.get_one(username=data.username)
            if exist:
                raise AccountException('account already exist')

            u = await self.uow.account.add(**data.model_dump())
            await self.uow.commit()
            return u.model()



    @uowaccess('account')
    async def admin_update(self, id: int,  data: AdminCreate) -> AccountModel:
        async with self.uow:
            exist = await self.uow.account.get_one(username=data.username)
            if exist:
                raise AccountException('account already exist')

            u = await self.uow.account.update(id, **data.model_dump())
            await self.uow.commit()
            return u.model()