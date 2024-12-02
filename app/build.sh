#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements/dev.txt

python manage.py collectstatic --no-input
python manage.py migrate
if [[ $CREATE_SUPERUSER ]];
then 
    python app/manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL"
fi