#!/bin/bash
set -e

# Initialisation de la base de données
airflow db init || echo "Database already initialized"

# Création de l'utilisateur admin (si il n'existe pas déjà)
if ! airflow users get-user -u "${_AIRFLOW_WWW_USER_USERNAME}" >/dev/null 2>&1; then
    echo "Creating admin user..."
    airflow users create \
        --username "${_AIRFLOW_WWW_USER_USERNAME}" \
        --firstname "${_AIRFLOW_WWW_USER_FIRSTNAME}" \
        --lastname "${_AIRFLOW_WWW_USER_LASTNAME}" \
        --role Admin \
        --email "${_AIRFLOW_WWW_USER_EMAIL}" \
        --password "${_AIRFLOW_WWW_USER_PASSWORD}"
else
    echo "Admin user already exists"
fi

# Démarrer Airflow
exec airflow standalone