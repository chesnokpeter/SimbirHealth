from core.infra.postgresql.tables import TIMETABLE
from core.repos.defaults.postgres import PostgresDefaultRepo


class TimetableRepo(PostgresDefaultRepo[TIMETABLE]):
    model = TIMETABLE
    reponame = 'timetable'
