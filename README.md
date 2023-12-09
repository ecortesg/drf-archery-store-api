# Django Rest Framework Ecommerce API

## Setup

```shell
git clone https://github.com/ecortesg/drf-ecommerce-api.git
python -m venv venv
venv/Scripts/activate
(.venv) pip install -r requirements.txt
(.venv) python manage.py migrate
(.venv) python manage.py createsuperuser
(.venv) python manage.py runserver
```

## Railway

### Deployment

- Deploy on Railway from GitHub
- Set ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS
- Create a Postgres database
- Add environment variables, including the DATABASE_URL
- Install Railway Client with Node.js

```shell
npm install -g @railway/cli
```

- Configure a superuser

```shell
railway login
railway link
railway run python manage.py createsuperuser
```

### Debugging

```shell
railway logs
```

## API Reference

### Swagger UI

https://drf-ecommerce-api.up.railway.app/api/schema/swagger-ui/

### ReDoc

https://drf-ecommerce-api.up.railway.app/api/schema/redoc/
