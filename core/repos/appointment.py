from core.infra.postgresql.tables import APPOINTMENT
from core.repos.defaults.postgres import PostgresDefaultRepo


class AppointmentRepo(PostgresDefaultRepo[APPOINTMENT]):
    model = APPOINTMENT
    reponame = 'appointment'
