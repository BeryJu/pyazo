#!/bin/bash -e
/app/wait_for_db.py
chown 1000:1000 /app/media
supervisord -c "/etc/supervisor/supervisor.${BOOTSTRAP_MODE}.ini"
