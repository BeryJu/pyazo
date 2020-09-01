# pyazo Documentation

## Installation

The recommended way to deploy pyazo on docker is with docker-compose. Simply download the `docker-compose.yml` file from [here](https://raw.githubusercontent.com/BeryJu/pyazo/master/docker-compose.yml) and place it wherever you want to.

To make your pyazo install secure, generate a PostgreSQL Password using the following command.

```
echo "POSTGRES_PASSWORD=$(openssl rand -base64 12 | tr -d '\n ')" >> .env
```

The secret key is used to create and sign cookies.

```
echo "PYAZO_SECRET_KEY=$(openssl rand -base64 50 | tr -d '\n ')" >> .env
```

Afterwards, run the following commands:

!!! note
    Optionally, if you want to migrate an old install, check [upgrade guide](upgrading/to-2.0.0.md) out.

```
docker-compose pull
docker-compose up -d
docker-compose exec server ./manage.py migrate
docker-compose exec server ./manage.py createsuperuser
```

This will start pyazo, listening on port 8000.

To configure pyazo, check out [Configuration](configuration.md).
