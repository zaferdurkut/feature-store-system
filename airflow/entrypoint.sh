#!/bin/bash

# Initialize the Airflow database
airflow db init

# Create an admin stream if it doesn't already exist
airflow users create \
    --role Admin \
    --username airflow \
    --password airflow \
    --email airflow@airflow.com \
    --firstname airflow \
    --lastname airflow || true

# Run the Airflow scheduler and webserver
exec "$@"
