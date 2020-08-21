#!/usr/bin/env bash
set -e

POSTGRES="psql --username ${POSTGRES_USER}"

echo -e "╔══════════════════════════════════════════════════════╗"
echo -e "  🔥  Dropping DB                                       "
echo -e "╠══════════════════════════════════════════════════════╣"
echo -e "  database: ${POSTGRES_DB}                              "
echo -e "╚══════════════════════════════════════════════════════╝"

${POSTGRES} <<-EOSQL
-- Terminate existing connections
REVOKE CONNECT ON DATABASE ${POSTGRES_DB} FROM public;

SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = '${POSTGRES_DB}';

-- Drop database
DROP DATABASE IF EXISTS ${POSTGRES_DB}
EOSQL

echo -e "\n"
