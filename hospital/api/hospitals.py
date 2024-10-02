from fastapi import APIRouter, Depends, Security, Body, Query
from core.enums import Roles
from core.exceptions import AccountException, HospitalException
from core.models.hospital import HospitalModel
from core.schemas.hospital import CreateHospital
from core.services.hospital import HospitalService

hospitalsR = APIRouter(prefix='/Hospitals', tags=['Hospitals'])

from hospital.depends import (
    uowdep,
    get_token,
    introspection,
    hospital
)

@hospitalsR.get('/') 
async def get_hospitals(
        count: int=100, from_ : int = Query(0, alias='from'), token=Security(get_token), uow=Depends(uowdep(hospital))
    ):
    await introspection(token)
    h = await HospitalService(uow).get_hospitals(from_, count)
    return h

@hospitalsR.get('/{id}') 
async def get_hospital(
        id: int, token=Security(get_token), uow=Depends(uowdep(hospital))
    ):
    await introspection(token)
    h = await HospitalService(uow).get_hospital(id)
    return h

@hospitalsR.get('/{id}/Rooms') 
async def get_hospital_rooms(
        id: int, token=Security(get_token), uow=Depends(uowdep(hospital))
    ):
    await introspection(token)
    h = await HospitalService(uow).get_hospital(id)
    return h.rooms if h else None


@hospitalsR.post('/') 
async def create_hospital(
        data: CreateHospital, token=Security(get_token), uow=Depends(uowdep(hospital))
    ) -> HospitalModel:
    u = await introspection(token)
    if not Roles.ADMIN in u.roles:
        raise AccountException('user not admin')

    r = await HospitalService(uow).create(data)
    return r


@hospitalsR.put('/{id}') 
async def update_hospital(
        id: int, data: CreateHospital, token=Security(get_token), uow=Depends(uowdep(hospital))
    ) -> HospitalModel:
    u = await introspection(token)
    if not Roles.ADMIN in u.roles:
        raise AccountException('user not admin')

    r = await HospitalService(uow).update(id, data)
    return r


@hospitalsR.delete('/{id}') 
async def delete_hospital(
        id: int, token=Security(get_token), uow=Depends(uowdep(hospital))
    ):
    u = await introspection(token)
    if not Roles.ADMIN in u.roles:
        raise AccountException('user not admin')
    h = await HospitalService(uow).delete(id)
    return h
