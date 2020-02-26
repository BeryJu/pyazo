# Migrating from pyazo < 2.0

This migration guide uses `pgLoader` to convert the MySQL Database from the old instance into the PostgreSQL Database that is used now. This guide also assumes that you want to keep using the same underlying server. Even if you want to move pyazo to a different machine, it is recommended to use this guide, as it makes it much easier to migrate on the same host.

## Pre-requisites

- Docker and docker-compose is installed on the pyazo Server
- Install pgLoader (`apt install pgloader` for example.)

## Prepare the new pyazo install

The old config file is located here: `/etc/pyazo/config.yml`

| Old setting name        | New setting name             |
|-------------------------|------------------------------|
| `error_report_enabled:` | `PYAZO_ERROR_REPORTING`      |
| `external_url`          | Not needed anymore.          |
| `default_return_view`   | `PYAZO_DEFAULT_RETURN_VIEW`  |
| `external_auth_only`    | Not needed anymore.          |
| `auto_claim_enabled`    | `PYAZO_AUTO_CLAIM_ENABLED`   |

**Additionally**, the content of `/etc/pyazo/secret_key` should be added as `PYAZO_SECRET_KEY`.

!!! note
    For LDAP Configuration, see [Configuration](configuration.md)

## Saving an export of the old pyazo install

Incase the migration goes wrong, it is recommended to create a database backup.

```
mysqldump -u pyazo -p pyazo > pyazo-backup.sql
```

The password is saved in `/etc/pyazo/config.d/database.yml`.

## Copying the media

The media needs to be copied from `/usr/share/pyazo/media/` to `<new pyazo install>/media/`.

Simply run the following command in your new pyazo's installation directory:

```
rsync -r --progress /usr/share/pyazo/media .
chown -R 1000:1000 media
```

## Migrate from MySQL to PostgreSQL

```
# Download latest images, create containers, but *only* start PostgreSQL
docker-compose pull
docker-compose up --no-start
docker-compose start postgresql

# Password from /etc/pyazo/config.d/database.yml
export MYSQL_PWD=''

# Password you've generated during install
export PGPASSWORD=''

# This contains the IP Address of your PostgreSQL Container
PG_ID=$(docker ps | grep postgres | awk '{print $1}')
PG_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $PG_ID)

# Run the actual migration
pgloader mysql://pyazo:@localhost/pyazo pgsql://pyazo@$PG_IP/pyazo
```

## Update the database to the newest version

```
docker-compose run server ./manage.py migrate
```

## Start pyazo

```
docker-compose pull
docker-compose up -d
```
