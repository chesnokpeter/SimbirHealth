from fastapi import APIRouter, Depends, Security

from core.services.document import DocumentService
from core.exceptions import AccountException
from core.schemas.history import CreateHistory
from core.models.history import HistoryModel
from core.enums import Roles

from document.depends import (
    uowdep,
    get_token, 
    introspection,
    get_hisrepo,
    get_accrepo,
    get_hosrepo
)

historyR = APIRouter(prefix='/History', tags=['History'])


@historyR.post('/')
async def create_history(
    data: CreateHistory, token=Security(get_token), ht=Depends(get_hisrepo)
) -> HistoryModel:
    u = await introspection(token)
    if not (Roles.ADMIN in u.roles or Roles.MANAGER in u.roles or Roles.DOCTOR):
        raise AccountException('user not admin or manager or doctor')
    uow = uowdep(ht, get_accrepo(token), get_hosrepo(token))()
    h = await DocumentService(uow).create(data)
    return h

@historyR.put('/{id}')
async def upd_history(
    id: int, data: CreateHistory, token=Security(get_token), ht=Depends(get_hisrepo)
) -> HistoryModel:
    u = await introspection(token)
    if not (Roles.ADMIN in u.roles or Roles.MANAGER in u.roles or Roles.DOCTOR):
        raise AccountException('user not admin or manager or doctor')
    uow = uowdep(ht, get_accrepo(token), get_hosrepo(token))()
    h = await DocumentService(uow).update(id, data)
    return h


@historyR.get('/Account/{id}')
async def get_history_pacient(
    id: int, token=Security(get_token), ht=Depends(get_hisrepo)
) -> list[HistoryModel] | None:
    u = await introspection(token)
    uow = uowdep(ht)()
    h = await DocumentService(uow).history_pacient(id)
    for i in h:
        if not (Roles.ADMIN in u.roles or Roles.DOCTOR in u.roles or i.pacientId == u.id): #Вот здесь добавил чтобы Админы тоже могли смотреть историю
            raise AccountException('user not admin or doctor or pacient')
        break
    return h

@historyR.get('/{id}')
async def get_history(
    id: int, token=Security(get_token), ht=Depends(get_hisrepo)
) -> HistoryModel | None:
    u = await introspection(token)
    uow = uowdep(ht)()
    h = await DocumentService(uow).get_history(id)
    if not (Roles.ADMIN in u.roles or Roles.DOCTOR in u.roles or h.pacientId == u.id): #Вот здесь добавил чтобы Админы тоже могли смотреть историю
        raise AccountException('user not admin or doctor or pacient')
    return h