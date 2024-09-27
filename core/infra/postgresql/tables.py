from datetime import date as datetype
from datetime import datetime
from datetime import time as timetype

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Time,
    inspect, 
    Boolean
)
from sqlalchemy import Enum 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from core.infra.abstract import DbAbsTable
from core.enums import Roles

from core.models.account import AccountModel
from core.models.hospital import HospitalModel

class Base(DeclarativeBase):
    def __repr__(self):
        mapper = inspect(self).mapper
        ent = []
        for col in [*mapper.column_attrs]:
            ent.append('{0}={1}'.format(col.key, getattr(self, col.key)))
        return '<{0}('.format(self.__class__.__name__) + ', '.join(ent) + ')>'


class ACCOUNT(Base, DbAbsTable):
    __tablename__ = 'account'
    id: Mapped[int] = mapped_column(
        Integer(),
        unique=True,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    lastName: Mapped[str] = mapped_column(String(), nullable=False)
    firstName: Mapped[str] = mapped_column(String(), nullable=False)
    username: Mapped[str] = mapped_column(String(), nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    roles: Mapped[list[Roles]] = mapped_column(ARRAY(Enum(Roles)), nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=False)

    def model(self):
        return AccountModel(
            id=self.id,
            lastName=self.lastName,
            firstName=self.firstName,
            username=self.username,
            password=self.password,
            roles=self.roles,
        )

class LASTOKEN(Base, DbAbsTable):
    __tablename__ = 'lastoken'
    id: Mapped[int] = mapped_column(
        Integer(),
        unique=True,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    accessToken: Mapped[str] = mapped_column(String(), nullable=True)
    refreshToken: Mapped[str] = mapped_column(String(), nullable=True)




class HOSPITAL(Base, DbAbsTable):
    __tablename__ = 'hospitals'
    id: Mapped[int] = mapped_column(
        Integer(),
        unique=True,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(), nullable=False)
    adress: Mapped[str] = mapped_column(String(), nullable=False)
    contactPhone: Mapped[str] = mapped_column(String(), nullable=False)
    rooms: Mapped[list[str]] = mapped_column(ARRAY(String()), nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=False)

    def model(self):
        return HospitalModel(
            id=self.id,
            name=self.name,
            adress=self.adress,
            contactPhone=self.contactPhone,
            rooms=self.rooms,
        )