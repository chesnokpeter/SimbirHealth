from core.infra.postgresql.tables import ACCOUNT
from core.repos.defaults.postgres import PostgresDefaultRepo


class AccountRepo(PostgresDefaultRepo[ACCOUNT]):
    model = ACCOUNT
    reponame = 'account'
