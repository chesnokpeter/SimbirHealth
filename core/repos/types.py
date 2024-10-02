import httpx


class RestConnType:
    client: httpx.AsyncClient
    baseurl: str
