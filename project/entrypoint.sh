#!/bin/sh
set -e

echo "*-- Debug Mode --*"

if [ "$DB_TYPE" = "postgres" ]
then
    echo "01: Waiting for PostgreSQL to start..."

    while ! nc -z "$DB_HOST" "$DB_PORT"; do
      sleep 0.1
    done

    echo "02: PostgreSQL succesfully started!."
fi

echo "03: Successful entrypoint!"
exec "$@"