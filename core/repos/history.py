from core.infra.postgresql.tables import HISTORY
from core.repos.defaults.postgres import PostgresDefaultRepo


class HistoryRepo(PostgresDefaultRepo[HISTORY]):
    model = HISTORY
    reponame = 'history'
