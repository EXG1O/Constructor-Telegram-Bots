#!/bin/bash

pip install -U pip
pip install poetry
poetry install

SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(25))")

read -p "Enter PostgreSQL database name: " POSTGRESQL_DATABASE_NAME
read -p "Enter PostgreSQL database user: " POSTGRESQL_DATABASE_USER
read -p "Enter PostgreSQL database password: " POSTGRESQL_DATABASE_PASSWORD

cat << EOF > .env
SECRET_KEY=$SECRET_KEY
DEBUG=True

FRONTEND_PATH=$PWD/frontend/dist

POSTGRESQL_DATABASE_NAME=$POSTGRESQL_DATABASE_NAME
POSTGRESQL_DATABASE_USER=$POSTGRESQL_DATABASE_USER
POSTGRESQL_DATABASE_PASSWORD=$POSTGRESQL_DATABASE_PASSWORD
EOF

python manage.py compilemessages -i env
python manage.py migrate
