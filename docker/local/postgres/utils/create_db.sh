#!/usr/bin/env bash
set -e

POSTGRES="psql --username ${POSTGRES_USER}"

echo -e "╔══════════════════════════════════════════════════════╗"
echo -e "  🧙  ‍Creating DB                                       "
echo -e "╠══════════════════════════════════════════════════════╣"
echo -e "  database: ${POSTGRES_DB}                              "
echo -e "╚══════════════════════════════════════════════════════╝"

${POSTGRES} <<-EOSQL
CREATE DATABASE ${POSTGRES_DB} OWNER ${POSTGRES_USER};
EOSQL

echo -e "\n"
