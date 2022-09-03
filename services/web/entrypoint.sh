#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ "$RABBITMQ" = "rabbitmq" ]
then
    echo "Waiting for rabbitmq..."

    while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
      sleep 0.1
    done

    echo "rabbitmq started"
fi

exec "$@"