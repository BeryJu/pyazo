# Installation

The recommended way to deploy pyazo on docker is with docker-compose. Simply download the `docker-compose.yml` file from [here](https://raw.githubusercontent.com/BeryJu/pyazo/master/docker-compose.yml) and place it wherever you want to.

To make your pyazo install secure, create a file called `.env` in the same directory as `docker-compose.yml` and add the following value:

```
PYAZO_POSTGRESQL__PASSWORD=<some random password>
```

The secret key is used to create and sign cookies. Use a website like [this](https://miniwebtool.com/django-secret-key-generator/) to generate a key.

```
PYAZO_SECRET_KEY=some-key-that-should-be-really-long
```

Afterwards, run the following commands:

!!! note
    Optionally, if you want to migrate an old install, check [this](migration.md) out.

```
docker-compose pull
docker-compose up -d
docker-compose exec server ./manage.py migrate
docker-compose exec server ./manage.py createsuperuser
```

This will start pyazo, listening on port 8000.

To configure pyazo, check out [Configuration](configuration.md).
