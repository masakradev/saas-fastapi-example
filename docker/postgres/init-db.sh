#!/bin/bash
set -e

# Create test database with _test suffix
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "${POSTGRES_DB}_test";
    GRANT ALL PRIVILEGES ON DATABASE "${POSTGRES_DB}_test" TO "$POSTGRES_USER";
EOSQL

echo "Test database '${POSTGRES_DB}_test' created successfully!"
