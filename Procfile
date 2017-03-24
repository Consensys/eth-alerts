web: gunicorn --pythonpath="$PWD/alerts" wsgi:application --log-file=- --access-logfile '-' --log-level info
migrate: python alerts/manage.py migrate --noinput
worker: celery -A taskapp.celery worker --loglevel info --workdir="$PWD/alerts" -c 1
scheduler: celery -A taskapp.celery beat -S djcelery.schedulers.DatabaseScheduler --loglevel info --workdir="$PWD/alerts"