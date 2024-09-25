from core.infra.postgresql.tables import HOSPITAL
from core.repos.defaults.postgres import PostgresDefaultRepo

class HospitalRepo(PostgresDefaultRepo[HOSPITAL]):
    model = HOSPITAL
    reponame = 'hospital'