python manage.py makemigrations

python manage.py migrate

python manage.py runserver

superuser: test test


if database does not work, try:
python manage.py migrate --run-syncdb
