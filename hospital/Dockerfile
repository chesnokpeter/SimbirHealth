FROM python:3.11.8-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    apt-get clean

COPY ./hospital/requirements.txt /hospital/requirements.txt

RUN pip install -r /hospital/requirements.txt

COPY ./hospital /hospital
COPY ./core /core

ENV SECRET_KEY="sdhfh32khkjkhjekhjrk4h5k3hj"
ENV POSTGRES_URL='postgresql+asyncpg://postgres:psql@localhost:5433/SimbirHealth'

EXPOSE 8021

RUN useradd -m appuser
USER appuser
CMD ["uvicorn", "hospital.app:app", "--port", "8021", "--host", "0.0.0.0"]