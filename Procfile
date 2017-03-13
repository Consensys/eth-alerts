web: gunicorn --pythonpath="$PWD/dapp" wsgi:application --log-file=- --access-logfile '-' --log-level info
migrate: python dapp/manage.py migrate --noinput
worker: celery -A taskapp.celery worker --loglevel info --workdir="$PWD/dapp" -c 1
scheduler: celery -A taskapp.celery beat -S djcelery.schedulers.DatabaseScheduler --loglevel info --workdir="$PWD/dapp"