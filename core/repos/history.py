from core.infra.postgresql.tables import HISTORY
from core.repos.defaults.postgres import PostgresDefaultRepo
from core.repos.abstract import repo_logger

@repo_logger
class HistoryRepo(PostgresDefaultRepo[HISTORY]):
    model = HISTORY
    reponame = 'history'
