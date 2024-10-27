from core.infra.postgresql.tables import APPOINTMENT
from core.repos.defaults.postgres import PostgresDefaultRepo
from core.repos.abstract import repo_logger

@repo_logger
class AppointmentRepo(PostgresDefaultRepo[APPOINTMENT]):
    model = APPOINTMENT
    reponame = 'appointment'
