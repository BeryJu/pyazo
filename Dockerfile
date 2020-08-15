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
    apt-get install -y libmagic-dev build-essential libldap2-dev libsasl2-dev && \
    rm -rf /var/cache/apt/ && \
    pip install -r requirements.txt  --no-cache-dir && \
    adduser --system --no-create-home --uid 1000 --group --home /app pyazo && \
    chown pyazo: /app && \
    apt-get remove --purge -y build-essential && \
    apt-get autoremove --purge -y

COPY ./pyazo/ /app/pyazo
COPY ./manage.py /app/
COPY ./docker/uwsgi.ini /app/

ENV PYAZO_POSTGRESQL__HOST=postgres
ENV PYAZO_REDIS__HOST=redis
ENV PYAZO_POSTGRESQL__USER=pyazo
# CI Password, same as in .github/workflows/ci.yml
ENV PYAZO_POSTGRESQL__PASSWORD="EK-5jnKfjrGRm<77"
RUN ./manage.py collectstatic --no-input

FROM python:3.8-slim-buster

COPY --from=locker /app/requirements.txt /app/
COPY --from=locker /app/requirements-dev.txt /app/
COPY --from=static-build /app/static /var/www/html/

WORKDIR /app/

RUN apt-get update && \
    apt-get install -y libmagic-dev build-essential libldap2-dev libsasl2-dev nginx && \
    rm -rf /var/cache/apt/ && \
    pip install -r requirements.txt --no-cache-dir && \
    pip install --no-cache-dir supervisor && \
    adduser --system --no-create-home --uid 1000 --group --home /app pyazo && \
    usermod -a -G www-data -G tty pyazo && \
    usermod -a -G pyazo www-data && \
    chown pyazo: /app && \
    apt-get remove --purge -y build-essential && \
    apt-get autoremove --purge -y

COPY ./bin/ /app/bin
COPY ./pyazo/ /app/pyazo
COPY ./manage.py /app/
# UWSGI and NGINX config
COPY ./docker/uwsgi.ini /app/
COPY ./docker/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/supervisor.server.ini /etc/supervisor/supervisor.server.ini
COPY ./docker/supervisor.worker.ini /etc/supervisor/supervisor.worker.ini
# Copy bootstrap scripts
COPY ./docker/bootstrap.sh /bootstrap.sh
COPY ./docker/wait_for_db.py /app/wait_for_db.py

ENV PYTHONUNBUFFERED=1

ENTRYPOINT [ "/bootstrap.sh" ]

CMD [ "" ]
