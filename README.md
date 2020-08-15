# pyazo

![](https://github.com/BeryJu/pyazo/workflows/pyazo-ci/badge.svg)

Documentation: https://beryju.github.io/pyazo/

## Quick instance

```
echo "PYAZO_POSTGRESQL__PASSWORD=$(openssl rand -base64 12)" >> .env
echo "PYAZO_SECRET_KEY=$(openssl rand -base64 50)" >> .env
# Optionally enable Error-reporting
# echo "PYAZO_ERROR_REPORTING=true" >> .env
docker-compose pull
docker-compose up -d
docker-compose exec server ./manage.py migrate
docker-compose exec server ./manage.py createsuperuser
```
