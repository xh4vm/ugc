#!/bin/bash
set -e

clickhouse client -n <<-EOSQL
	CREATE DATABASE IF NOT EXISTS $CH_DB_NAME;
	CREATE DATABASE IF NOT EXISTS $CH_REPLICA_DB_NAME;
EOSQL