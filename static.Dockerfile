FROM python:3.8-slim-buster as locker

COPY ./Pipfile /app/
COPY ./Pipfile.lock /app/

WORKDIR /app/

RUN pip install pipenv && \
    pipenv lock -r > requirements.txt && \
    pipenv lock -rd > requirements-dev.txt

FROM python:3.8-slim-buster AS static-build

COPY --from=locker /app/requirements.txt /app/
COPY --from=locker /app/requirements-dev.txt /app/

WORKDIR /app/

RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client-11 && \
    rm -rf /var/lib/apt/ && \
    pip install -r requirements.txt  --no-cache-dir && \
    adduser --system --no-create-home --uid 1000 --group --home /app pyazo

COPY ./pyazo/ /app/pyazo
COPY ./manage.py /app/
COPY ./docker/uwsgi.ini /app/

ENV PYAZO_POSTGRESQL__HOST=postgres
ENV PYAZO_REDIS__HOST=redis
ENV PYAZO_POSTGRESQL__USER=pyazo
# CI Password, same as in .github/workflows/ci.yml
ENV PYAZO_POSTGRESQL__PASSWORD="EK-5jnKfjrGRm<77"
RUN ./manage.py collectstatic --no-input

FROM nginx

COPY --from=static-build /app/static /usr/share/nginx/html/static/
