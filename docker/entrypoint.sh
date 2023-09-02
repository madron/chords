#!/bin/sh
set -e

if [ "$1" = 'uwsgi' ]; then
    echo 'Wait for database'
    gosu nobody python3 /src/manage.py wait_for_database --timeout 20
    echo 'Migrate'
    gosu nobody python3 /src/manage.py migrate --noinput
    echo gosu nobody $*
    exec gosu nobody $*
elif [ "$1" = 'nginx' ]; then
    chown nobody /var/tmp/nginx
    exec nginx -c /src/docker/nginx.conf -g "daemon off;"
else
    exec "$@"
fi
