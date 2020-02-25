# Installation

The recommended way to deploy pyazo on docker is with docker-compose. Simply download the `docker-compose.yml` file from [https://raw.githubusercontent.com/BeryJu/pyazo/master/docker-compose.yml](here), place it wherever you want to, and run the following commands:

```
docker-compose pull
docker-compose up -d
docker-compose exec server ./manage.py migrate
docker-compose exec server ./manage.py createsuperuser
```

This will start pyazo, listening on port 80 and 443.

To configure pyazo, check out [Configuration](configuration.md).
