#!/bin/bash

echo "Entrypoint script is executed"

echo "Waiting for the database to be ready (optional, depending on your setup)..."
sleep 5
# Check if the migrations folder exists to determine if the database has been initialized
if [ ! -d "migrations" ]; then
    echo "Initializing the database..."

    # Perform Flask database initialization
    flask db init

    # Create an initial migration
    flask db migrate -m "Initial revision"

    # Apply the initial migration
    flask db upgrade

    echo "Database initialization completed."
else
    echo "Database already initialized. Applying any pending migrations..."
    # Apply any pending database migrations
    flask db upgrade
fi

echo "Add data to db"
/usr/local/bin/python /app/app/init_db.py

# Start your main application process
echo "Starting the main application process..."

exec "$@"
