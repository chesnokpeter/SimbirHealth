from core.infra.postgresql.tables import LASTOKEN
from core.repos.defaults.postgres import PostgresDefaultRepo


class LostokenRepo(PostgresDefaultRepo[LASTOKEN]):
    model = LASTOKEN
    reponame = 'lostoken'
