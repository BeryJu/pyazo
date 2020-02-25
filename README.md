# pyazo

![](https://github.com/BeryJu/pyazo/workflows/pyazo-ci/badge.svg)

Documentation: https://beryju.github.io/pyazo/

## Quick instance

```
# Optionally enable Error-reporting
# export PYAZO_ERROR_REPORTING=true
docker-compose pull
docker-compose up -d
docker-compose exec server ./manage.py migrate
docker-compose exec server ./manage.py createsuperuser
```
