#!/usr/bin/env python
"""This file needs to be run from the root of the project to correctly
import pyazo. This is done by the dockerfile."""
from json import dumps
from time import sleep

from psycopg2 import OperationalError, connect
from redis import Redis
from redis.exceptions import RedisError

from pyazo.utils.config import CONFIG


while True:
    try:
        conn = connect(
            dbname=CONFIG.y("postgresql.name"),
            user=CONFIG.y("postgresql.user"),
            password=CONFIG.y("postgresql.password"),
            host=CONFIG.y("postgresql.host"),
        )
        conn.cursor()
        break
    except OperationalError:
        sleep(1)
        print(
            dumps(
                {
                    "event": "PostgreSQL Connection failed, retrying...",
                    "level": "warning",
                    "logger": __name__,
                }
            )
        )

while True:
    try:
        redis = Redis(
            host=CONFIG.y("redis.host"),
            port=6379,
            db=CONFIG.y("redis.message_queue_db"),
            password=CONFIG.y("redis.password"),
        )
        redis.ping()
        break
    except RedisError:
        sleep(1)
        print(
            dumps(
                {
                    "event": "Redis Connection failed, retrying...",
                    "level": "warning",
                    "logger": __name__,
                }
            )
        )
