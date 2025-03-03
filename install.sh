#!/bin/bash

pip install -U pip
pip install poetry
poetry install

SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(25))")

read -p "Enter Telegram bot API-token: " TELEGRAM_BOT_TOKEN
read -p "Enter path to the 'dist' directory of the frontend: " FRONTEND_PATH
read -p "Enter PostgreSQL database name: " POSTGRESQL_DATABASE_NAME
read -p "Enter PostgreSQL database user: " POSTGRESQL_DATABASE_USER
read -p "Enter PostgreSQL database password: " POSTGRESQL_DATABASE_PASSWORD

cat << EOF > .env
SECRET_KEY=$SECRET_KEY

DEBUG=True
ENABLE_TELEGRAM_AUTH=False

TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN

FRONTEND_PATH=$FRONTEND_PATH

POSTGRESQL_DATABASE_NAME=$POSTGRESQL_DATABASE_NAME
POSTGRESQL_DATABASE_USER=$POSTGRESQL_DATABASE_USER
POSTGRESQL_DATABASE_PASSWORD=$POSTGRESQL_DATABASE_PASSWORD
EOF

python manage.py compilemessages -i env
python manage.py migrate
