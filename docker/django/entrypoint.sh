#!/usr/bin/env bash

until python manage.py migrate --settings=dados_brasil_io.settings
do
    echo "Esperando pela database..."
    sleep 2
done

python manage.py runserver 0.0.0.0:8000 --settings=dados_brasil_io.settings
