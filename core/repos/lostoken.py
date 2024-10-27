from core.infra.postgresql.tables import LASTOKEN
from core.repos.defaults.postgres import PostgresDefaultRepo
from core.repos.abstract import repo_logger


@repo_logger
class LostokenRepo(PostgresDefaultRepo[LASTOKEN]):
    model = LASTOKEN
    reponame = 'lostoken'
