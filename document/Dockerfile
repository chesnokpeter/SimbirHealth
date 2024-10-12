FROM python:3.11.8-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    apt-get clean

COPY ./document/requirements.txt /document/requirements.txt

RUN pip install -r /document/requirements.txt

COPY ./document /document
COPY ./core /core

ENV SECRET_KEY="sdhfh32khkjkhjekhjrk4h5k3hj"
ENV POSTGRES_URL='postgresql+asyncpg://postgres:psql@database:5432/SimbirHealth'

EXPOSE 8041

RUN useradd -m appuser
USER appuser
CMD ["uvicorn", "document.app:app", "--port", "8041", "--host", "0.0.0.0"]