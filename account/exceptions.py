from core.exceptions import RestExceptions


class JWTExceptions(RestExceptions):...



class JWTAccessExceptions(JWTExceptions): ...


class JWTRefreshExceptions(JWTExceptions): ...
