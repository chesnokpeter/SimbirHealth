FROM python:3.11.8-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    apt-get clean

COPY ./account/requirements.txt /account/requirements.txt

RUN pip install -r /account/requirements.txt

COPY ./account /account
COPY ./core /core

ENV SECRET_KEY="sdhfh32khkjkhjekhjrk4h5k3hj"
ENV POSTGRES_URL='postgresql+asyncpg://postgres:psql@localhost:5433/SimbirHealth'

EXPOSE 8011

RUN useradd -m appuser
USER appuser
CMD ["uvicorn", "account.app:app", "--port", "8011", "--host", "0.0.0.0"]