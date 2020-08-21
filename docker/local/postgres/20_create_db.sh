#!/usr/bin/env bash
set -e

POSTGRES="psql --username ${POSTGRES_USER}"

echo -e "╔══════════════════════════════════════════════════════╗"
echo -e "  🏗 Creating DB 🏗                                     "
echo -e "╠══════════════════════════════════════════════════════╣"
echo -e "  database: ${DB_NAME}                                  "
echo -e "╚══════════════════════════════════════════════════════╝"

${POSTGRES} <<-EOSQL
CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};
EOSQL
