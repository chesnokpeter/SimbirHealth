from typing import Annotated, TypeAlias
from core.enums import Roles
from core.exceptions import AccountException
from core.models.account import AccountModel
from core.schemas.account import SignUpSch, SignIn
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
    async def signin(self, data: SignIn) -> AccountModel:
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
