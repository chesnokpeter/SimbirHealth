from fastapi import APIRouter, Depends, Security, Body, Query

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

historyR = APIRouter(prefix='/history', tags=['History'])


@historyR.delete('/{id}')
async def create_history(
    data: CreateHistory, token=Security(get_token), ht=Depends(get_hisrepo)
) -> HistoryModel:
    u = await introspection(token)
    if not (Roles.ADMIN in u or Roles.MANAGER in u or Roles.DOCTOR):
        raise AccountException('user not admin or manager or doctor')
    uow = uowdep(ht, get_accrepo(token), get_hosrepo(token))()
    h = await DocumentService(uow).create(data)
    return h