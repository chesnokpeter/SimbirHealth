from abc import ABC, abstractmethod
from functools import wraps

from core.exceptions import NoAccessForRepo, NoConnectorForRepo
from core.infra.abstract import AbsConnector
from core.repos.abstract import AbsRepo, RestAPIAbsRepo
from core.repos.account import AccountRepo
from core.repos.lostoken import LostokenRepo
from core.repos.hospital import HospitalRepo
from core.repos.timetable import TimetableRepo
from core.repos.appointment import AppointmentRepo
from core.repos.history import HistoryRepo


class AbsUnitOfWork(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbsUnitOfWork):
    def __init__(self, repos: list[AbsRepo], connectors: list[AbsConnector]):
        self.connectors = connectors
        self.repo_names = [repo.reponame for repo in repos]
        [setattr(self, repo.reponame, repo) for repo in repos]
        for r in repos:
            if r.require_connector not in {c.connector_name for c in connectors}:
                raise NoConnectorForRepo(f'No Connector For Repo "{r.reponame}"')

    async def __aenter__(self):
        for c in self.connectors:
            await c.connect()
            for repo_name in self.repo_names:
                repo: AbsRepo = getattr(self, repo_name)
                if repo.require_connector == c.connector_name:
                    repo(c.session)

        return self

    async def __aexit__(self, *args):
        await self.rollback()
        for c in self.connectors:  # asyncio.gather not works(
            await c.close()

    async def commit(self):
        for c in self.connectors:  # asyncio.gather not works(
            await c.commit()

    async def rollback(self):
        for c in self.connectors:  # asyncio.gather not works(
            await c.rollback()


class AllReposUnitOfWork(AbsUnitOfWork, ABC):
    account: AccountRepo
    lostoken: LostokenRepo
    hospital: HospitalRepo
    timetable: TimetableRepo
    appointment: AppointmentRepo
    history: HistoryRepo


def uowaccess(*access: str):
    """этот декоратор проверяет доступ к репозиториям внутри unit of work"""

    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            for i in access:
                if not getattr(self.uow, i, False):
                    raise NoAccessForRepo(f'No Access For Repo "{i}"')
            return await func(self, *args, **kwargs)

        return wrapper

    return decorator
