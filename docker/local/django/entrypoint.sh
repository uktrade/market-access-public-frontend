#!/usr/bin/env bash

# Wait for the DB server to be running
dockerize -wait tcp://db:5432 -timeout 60s
# Apply django migrations
python manage.py makemigrations
python manage.py migrate

echo -e "╔══════════════════════════════════════════════════════╗"
echo -e "                👏  Ready to roll!  👏                 "
echo -e "╠══════════════════════════════════════════════════════╣"
echo -e "║  - To list all available make commands               ║"
echo -e "║    run 'make help'.                                  ║"
echo -e "╚══════════════════════════════════════════════════════╝"

# Tail a file to keep the container alive
tail -f /dev/null
