from core.enums import Roles
from core.exceptions import NotFoundError, ConflictError, IncorrectError
from core.models.account import AccountModel
from core.schemas.account import SignUpSch, SignInSch, SignOutSch, UpdateSch, AdminCreate
from core.services.abstract import AbsService, service_logger
from core.uow import uowaccess

from core.utils import hash

@service_logger
class AccountService(AbsService):
    @uowaccess('account')
    async def signup(self, data: SignUpSch) -> AccountModel:
        async with self.uow:
            exist = await self.uow.account.get_one(username=data.username)
            if exist:
                raise ConflictError('account already exist')

            passhash = hash(data.password)

            u = await self.uow.account.add(**data.model_dump(exclude=['password']), roles=[Roles.USER], password=passhash)
            await self.uow.commit()
            return u.model()

    @uowaccess('account')
    async def signin(self, data: SignInSch) -> AccountModel:
        async with self.uow:
            u = await self.uow.account.get_one(username=data.username, password=hash(data.password))
            if not u:
                raise IncorrectError('login or password is incorrect')

            return u.model()

    @uowaccess('account')
    async def me(self, id: int) -> AccountModel:
        async with self.uow:
            u = await self.uow.account.get_one(id=id)
            if not u:
                raise NotFoundError('account not found')

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
                if t:
                    raise ConflictError('accessToken has already been used')
            if refreshToken:
                t = await self.uow.lostoken.get_one(refreshToken=refreshToken)
                if t:
                    raise ConflictError('refreshToken has already been used')

    @uowaccess('account')
    async def update(self, id: int, data: UpdateSch) -> AccountModel:
        async with self.uow:
            u = await self.uow.account.get_one(id=id)
            if not u:
                raise NotFoundError('account does not exist')
            passhash = hash(data.password)
            u = await self.uow.account.update(id=id, **data.model_dump(exclude=['password']), password=passhash)
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
                raise ConflictError('account already exist')
            passhash = hash(data.password)

            u = await self.uow.account.add(**data.model_dump(exclude=['password']), password=passhash)
            await self.uow.commit()
            return u.model()

    @uowaccess('account')
    async def admin_update(self, id: int, data: AdminCreate) -> AccountModel:
        async with self.uow:
            exist = await self.uow.account.get_one(id=id)
            if not exist:
                raise NotFoundError('account not found')
            exist = await self.uow.account.get_one(username=data.username)
            if exist:
                raise ConflictError('account already exist')
            passhash = hash(data.password)
            u = await self.uow.account.update(id, **data.model_dump(exclude=['password']), password=passhash)
            await self.uow.commit()
            return u.model()

    @uowaccess('account')
    async def admin_delete(self, id: int) -> None:
        async with self.uow:
            exist = await self.uow.account.get_one(id=id)
            if exist:
                await self.uow.account.update(id=id, is_deleted=True)
                await self.uow.commit()
            return None

    @uowaccess('account')
    async def get_doctors(
        self, nameFilter: str, from_: int, count: int
    ) -> list[AccountModel] | None:
        async with self.uow:
            u = await self.uow.account.filter_by_name_from_count(nameFilter, from_, count)
            return [i.model() for i in u if Roles.DOCTOR in i.roles]

    @uowaccess('account')
    async def get_doctor(self, id: int) -> AccountModel | None:
        async with self.uow:
            u = await self.uow.account.get_one(id=id)
            return u.model() if u and Roles.DOCTOR in u.roles else None

