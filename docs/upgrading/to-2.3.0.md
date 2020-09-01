# Upgrading to 2.3.0

## Changes

- Django has been upgraded to 3.1
- Webserver has been migrated from uWSGI to Gunicorn and uvicorn to make use of the ASGI features in Django 3.1
- Logging is now completely JSON

## Upgrade Procedure

```
wget https://raw.githubusercontent.com/BeryJu/pyazo/v2.3.0/docker-compose.yml
docker-compose pull
docker-compose up -d
docker-compose exec server ./manage.py migrate
```

## Fixes

- Update dependencies
