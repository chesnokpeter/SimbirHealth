import httpx
from dataclasses import dataclass


@dataclass
class RestConnType:
    client: httpx.AsyncClient
    baseurl: str
