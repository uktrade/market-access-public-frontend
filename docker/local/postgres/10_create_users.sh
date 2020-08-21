#!/usr/bin/env bash
set -e

POSTGRES="psql --username ${POSTGRES_USER}"

echo -e "╔══════════════════════════════════════════════════════╗"
echo -e "  🏗 Creating DB role 🏗                                "
echo -e "╠══════════════════════════════════════════════════════╣"
echo -e "  role: ${DB_USER}                                      "
echo -e "╚══════════════════════════════════════════════════════╝"

${POSTGRES} <<-EOSQL
CREATE USER ${DB_USER} WITH CREATEDB PASSWORD '${DB_PASS}';
EOSQL
