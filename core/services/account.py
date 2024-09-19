from typing import Annotated, TypeAlias
from core.enums import Roles
from core.exceptions import AccountException
from core.models.account import AccountModel
from core.schemas.account import SignUpSch
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
