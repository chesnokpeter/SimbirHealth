FROM python:3.11.8-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    apt-get clean

COPY ./timetable/requirements.txt /timetable/requirements.txt

RUN pip install -r /timetable/requirements.txt

COPY ./timetable /timetable
COPY ./core /core

ENV SECRET_KEY="sdhfh32khkjkhjekhjrk4h5k3hj"
ENV POSTGRES_URL='postgresql+asyncpg://postgres:psql@database:5432/SimbirHealth'

EXPOSE 8031

RUN useradd -m appuser
USER appuser
CMD ["uvicorn", "timetable.app:app", "--port", "8031", "--host", "0.0.0.0"]