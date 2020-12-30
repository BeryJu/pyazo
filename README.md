# pyazo

# ARCHIVED, use https://github.com/BeryJu/imagik instead

![](https://github.com/BeryJu/pyazo/workflows/pyazo-ci/badge.svg)

Documentation: https://beryju.github.io/pyazo/

## Quick instance

```
echo "POSTGRES_PASSWORD=$(openssl rand -base64 12 | tr -d '\n ')" >> .env
echo "PYAZO_SECRET_KEY=$(openssl rand -base64 50 | tr -d '\n ')" >> .env
# Optionally enable Error-reporting
# echo "PYAZO_ERROR_REPORTING=true" >> .env
docker-compose pull
docker-compose up -d
docker-compose exec server ./manage.py migrate
docker-compose exec server ./manage.py createsuperuser
```
