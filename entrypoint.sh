#!/bin/bash

# Exit on error
set -e

# Run database migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Execute the container's main command
exec "$@"