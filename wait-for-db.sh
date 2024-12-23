#!/bin/bash

cmd="$@"

echo "Waiting for postgres..."

while ! nc -z psql 5432; do
  sleep 0.1
  echo "Waiting"
done

echo "PostgreSQL started"
make reset_database
make revision
make migrate
exec $cmd