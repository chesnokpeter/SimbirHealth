FROM python:3.11.8-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    apt-get clean

COPY ./db_init/requirements.txt /db_init/requirements.txt

RUN pip install -r /db_init/requirements.txt

COPY ./db_init /db_init
COPY ./db_init/db_init.py db_init.py
COPY ./core /core

ENV POSTGRES_URL='postgresql+asyncpg://postgres:psql@localhost:5433/SimbirHealth'


RUN useradd -m appuser
USER appuser
CMD ["python", "db_init.py"]