python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
PYTHONUNBUFFERED=1 python manage.py runserver 0.0.0.0:8000
