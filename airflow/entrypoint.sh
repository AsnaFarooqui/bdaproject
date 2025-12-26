#!/bin/ bash
set -e

DB_PATH=/opt/airflow/airflow.db

echo " Checking Airflow database…"

if [ ! -f "$DB_PATH" ]; then
  echo "🟡 Initializing Airflow DB (first run)…"
  airflow db init

  echo "🟡 Creating default admin user…"
  airflow users create \
    --username admin \
    --password admin || true \ 
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email a.farooqui.26918@khi.iba.edu.pk
else
  echo "🟢 DB already exists — running migrations…"
  airflow db upgrade
fi

echo "🚀 Starting Airflow: $@"
exec airflow "$@"
