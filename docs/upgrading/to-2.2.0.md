# Upgrading to 2.2.0

No breaking changes.

## Upgrade Procedure

```
wget https://raw.githubusercontent.com/BeryJu/pyazo/v2.1.0/docker-compose.yml
docker-compose pull
docker-compose up -d
docker-compose exec server ./manage.py migrate
```
