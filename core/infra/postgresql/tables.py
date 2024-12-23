from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Time,
    inspect,
    Boolean,
)
from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from core.infra.abstract import DbAbsTable
from core.enums import Roles

from core.models.account import AccountModel
from core.models.hospital import HospitalModel
from core.models.timetable import TimetableModel
from core.models.appoiniment import AppoinimentModel
from core.models.history import HistoryModel


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

    timetables: Mapped[list['TIMETABLE']] = relationship(
        'TIMETABLE', back_populates='doctor', lazy='selectin'
    )

    appointments: Mapped[list['APPOINTMENT']] = relationship(
        'APPOINTMENT', back_populates='patient', lazy='selectin'
    )

    history_as_patient: Mapped[list['HISTORY']] = relationship(
        'HISTORY', foreign_keys='HISTORY.pacientId', back_populates='pacient', lazy='selectin'
    )

    history_as_doctor: Mapped[list['HISTORY']] = relationship(
        'HISTORY', foreign_keys='HISTORY.doctorId', back_populates='doctor', lazy='selectin'
    )

    def model(self):
        return AccountModel(
            id=self.id,
            lastName=self.lastName,
            firstName=self.firstName,
            username=self.username,
            # password=self.password,
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

    timetables: Mapped[list['TIMETABLE']] = relationship(
        'TIMETABLE', back_populates='hospital', lazy='selectin'
    )

    history: Mapped[list['HISTORY']] = relationship(
        'HISTORY', back_populates='hospital', lazy='selectin'
    )

    def model(self):
        return HospitalModel(
            id=self.id,
            name=self.name,
            adress=self.adress,
            contactPhone=self.contactPhone,
            rooms=self.rooms,
        )


class TIMETABLE(Base, DbAbsTable):
    __tablename__ = 'timetable'

    id: Mapped[int] = mapped_column(
        Integer(),
        unique=True,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    hospital_id: Mapped[int] = mapped_column(Integer(), ForeignKey('hospitals.id'), nullable=False)
    doctor_id: Mapped[int] = mapped_column(Integer(), ForeignKey('account.id'), nullable=False)
    from_dt: Mapped[DateTime] = mapped_column(DateTime(), nullable=False)
    to_dt: Mapped[DateTime] = mapped_column(DateTime(), nullable=False)
    room: Mapped[str] = mapped_column(String(), nullable=False)

    hospital: Mapped['HOSPITAL'] = relationship(
        'HOSPITAL', back_populates='timetables', lazy='selectin'
    )
    doctor: Mapped['ACCOUNT'] = relationship(
        'ACCOUNT', back_populates='timetables', lazy='selectin'
    )
    appointments: Mapped[list['APPOINTMENT']] = relationship(
        'APPOINTMENT', back_populates='timetable', lazy='selectin', cascade='all, delete-orphan'
    )

    def model(self):
        return TimetableModel(
            id=self.id,
            hospital_id=self.hospital_id,
            doctor_id=self.doctor_id,
            from_time=self.from_dt,
            to_time=self.to_dt,
            room=self.room
        )


class APPOINTMENT(Base, DbAbsTable):
    __tablename__ = 'appointment'
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    time: Mapped[DateTime] = mapped_column(DateTime(), nullable=False)

    timetable_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey('timetable.id', ondelete='CASCADE'), nullable=False
    )
    patient_id: Mapped[int] = mapped_column(Integer(), ForeignKey('account.id'), nullable=False)

    timetable: Mapped['TIMETABLE'] = relationship(
        'TIMETABLE', back_populates='appointments', lazy='selectin'
    )
    patient: Mapped['ACCOUNT'] = relationship(
        'ACCOUNT', back_populates='appointments', lazy='selectin'
    )

    def model(self):
        return AppoinimentModel(
            id=self.id, time=self.time, timetable_id=self.timetable_id, patient_id=self.patient_id
        )


class HISTORY(Base, DbAbsTable):
    __tablename__ = 'history'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    date: Mapped[DateTime] = mapped_column(DateTime(), nullable=False)

    pacientId: Mapped[int] = mapped_column(Integer(), ForeignKey('account.id'), nullable=False)

    hospitalId: Mapped[int] = mapped_column(Integer(), ForeignKey('hospitals.id'), nullable=False)

    doctorId: Mapped[int] = mapped_column(Integer(), ForeignKey('account.id'), nullable=False)
    room: Mapped[str] = mapped_column(String(), nullable=False)
    data: Mapped[str] = mapped_column(String(), nullable=False)

    pacient: Mapped['ACCOUNT'] = relationship(
        'ACCOUNT', foreign_keys=[pacientId], back_populates='history_as_patient', lazy='selectin'
    )

    doctor: Mapped['ACCOUNT'] = relationship(
        'ACCOUNT', foreign_keys=[doctorId], back_populates='history_as_doctor', lazy='selectin'
    )

    hospital: Mapped['HOSPITAL'] = relationship(
        'HOSPITAL', back_populates='history', lazy='selectin'
    )

    def model(self):
        return HistoryModel(
            id=self.id,
            date=self.date,
            pacientId=self.pacientId,
            hospitalId=self.hospitalId,
            doctorId=self.doctorId,
            room=self.room,
            data=self.data,
        )
