# Upgrading to 2.1.0

## Changes

- pyazo now only listens on Port 8000 instead of 80 and 443. This is because traefik has been replaced with nginx.
- The docker-compose file now references a static Version instead of :latest. This has been changed to prevent unintended updates.

## Upgrade Procedure

```
wget https://raw.githubusercontent.com/BeryJu/pyazo/v2.1.0/docker-compose.yml
docker-compose pull
docker-compose up -d
docker-compose exec server ./manage.py migrate
```

## Fixes

- Fix pyazo not working if multiple instances are deployed on the same host
- Update dependencies
