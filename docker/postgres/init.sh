#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER mazimia;
	CREATE DATABASE flaskdevdb;
	GRANT ALL PRIVILEGES ON DATABASE flaskdevdb TO mazimia;
EOSQL