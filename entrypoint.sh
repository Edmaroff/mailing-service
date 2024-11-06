#!/bin/bash

echo "Применение миграций..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Загрузка фикстур..."
python manage.py load_fixtures

echo "Создание суперпользователя..."
python manage.py csu

echo "Запуск сервера..."
python manage.py runserver 0.0.0.0:8000
