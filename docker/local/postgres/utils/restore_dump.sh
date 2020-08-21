#!/usr/bin/env bash
set -e
DUMPFILE=$1
POSTGRES="psql --username ${POSTGRES_USER}"

echo -e "╔══════════════════════════════════════════════════════╗"
echo -e "  🍩  Restoring DB                                      "
echo -e "╠══════════════════════════════════════════════════════╣"
echo -e "  database: ${POSTGRES_DB}                              "
echo -e "  dump: ${DUMPFILE}                                     "
echo -e "╚══════════════════════════════════════════════════════╝"

gunzip < /var/lib/postgresql/dumps/${DUMPFILE} | ${POSTGRES} ${POSTGRES_DB}

echo -e "\n"
