#!/bin/bash

set -e

DB_NAME="${DB_NAME:-labor_certification}"
DB_USER="${DB_USER:-$USER}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

# Create database (ignore error if exists)
createdb -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME 2>/dev/null || true

# Load data
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f data/labor_certification_applications_template/labor_certification_applications_full.sql

echo "Done. Connect with: psql -U $DB_USER -d $DB_NAME"
