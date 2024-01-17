# Packages

django
djangorestframework
django-cors-headers
django-environ
django-storages
django-cleanup
drf-spectacular
djangorestframework-simplejwt
boto3

# Commands

## Virtual environment

### Create

python -m venv venv

### Activate

venv/Scripts/activate

### Deactivate

deactivate

### Create requirements file

pip freeze > requirements.txt

### Install requirements

pip install -r requirements.txt

## Django

### Create project

django-admin startproject project

### Create app

python manage.py startapp app

### Make migrations

python manage.py makemigrations

### Migrate

python manage.py migrate

### Create super user

python manage.py createsuperuser

### Run server

python manage.py runserver

### Generate secret key

python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
