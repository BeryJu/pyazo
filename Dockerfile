FROM python:3.6-slim-stretch as build

COPY ./pyazo/ /app/pyazo
COPY ./manage.py /app/
COPY ./requirements.txt /app/

WORKDIR /app/

RUN apt-get update && apt-get install build-essential libffi-dev libsasl2-dev python-dev libldap2-dev libssl-dev libpq-dev -y && \
    mkdir /app/static/ && \
    pip install -r requirements.txt && \
    pip install psycopg2 && \
    ./manage.py collectstatic --no-input && \
    apt-get remove --purge -y build-essential && \
    apt-get autoremove --purge -y

FROM python:3.6-slim-stretch

COPY ./pyazo/ /app/pyazo
COPY ./manage.py /app/
COPY ./requirements.txt /app/
COPY --from=build /app/static /app/static/

WORKDIR /app/

RUN apt-get update && apt-get install build-essential libffi-dev libsasl2-dev python-dev libldap2-dev libssl-dev libpq-dev  -y && \
    pip install -r requirements.txt && \
    pip install psycopg2 && \
    adduser --system --home /app/ pyazo && \
    chown -R pyazo /app/ && \
    apt-get remove --purge -y build-essential && \
    apt-get autoremove --purge -y

USER pyazo
